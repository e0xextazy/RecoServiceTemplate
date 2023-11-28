from typing import List

from fastapi import APIRouter, FastAPI, Request
from pydantic import BaseModel

from service.api.exceptions import ModelNotFoundError, UserNotFoundError
from service.log import app_logger


class RecoResponse(BaseModel):
    user_id: int
    items: List[int]


router = APIRouter()


@router.get(
    path="/health",
    tags=["Health"],
)
async def health() -> str:
    return "I am alive"


@router.get(
    path="/reco/{model_name}/{user_id}",
    tags=["Recommendations"],
    response_model=RecoResponse,
    responses={
        404: {
            "description": "User or Model not found",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "error_key": "model_not_found",
                            "error_message": "Model {model_name} not found",
                            "error_loc": "null",
                        },
                        {
                            "error_key": "user_not_found",
                            "error_message": "User {iser_id} not found",
                            "error_loc": "null",
                        },
                    ]
                }
            },
        },
        401: {
            "description": "Bad authorization",
            "content": {
                "application/json": {
                    "example": {
                        "error_key": "bad_authorization",
                        "error_message": "Bad auth token",
                        "error_loc": "null",
                    }
                }
            },
        },
        422: {
            "description": "The server was unable to process the request because it contains invalid data",
            "content": {
                "application/json": {
                    "example": {
                        "error_key": "missing",
                        "error_message": "Field required",
                        "error_loc": ["query", "token"],
                    }
                }
            },
        },
    },
)
async def get_reco(
    request: Request,
    model_name: str,
    user_id: int,
) -> RecoResponse:
    app_logger.info(f"Request for model: {model_name}, user_id: {user_id}")

    k_recs = request.app.state.k_recs
    known_models = request.app.state.known_models

    if user_id > 10**9:
        raise UserNotFoundError(error_message=f"User {user_id} not found")

    reco = known_models.get(
        model_name, error=ModelNotFoundError(error_message=f"Model {model_name} not found")
    ).get_reco(str(user_id), k_recs)

    if len(reco) < 10:
        reco = known_models["popular_model"].get_reco(str(user_id), k_recs)

    return RecoResponse(user_id=user_id, items=reco)


def add_views(app: FastAPI) -> None:
    app.include_router(router)
