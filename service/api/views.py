from typing import List

from fastapi import APIRouter, FastAPI, Request
from pydantic import BaseModel

from service.api.exceptions import BadAuthorizationError, ModelNotFoundError, UserNotFoundError
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
)
async def get_reco(
    request: Request,
    model_name: str,
    user_id: int,
    token: str,
) -> RecoResponse:
    app_logger.info(f"Request for model: {model_name}, user_id: {user_id}")

    k_recs = request.app.state.k_recs
    auth_token = request.app.state.auth_token
    known_models = request.app.state.known_models

    if user_id > 10**9:
        raise UserNotFoundError(error_message=f"User {user_id} not found")

    if auth_token != token:
        raise BadAuthorizationError(error_message="Bad auth token")

    reco = known_models.get(
        model_name, error=ModelNotFoundError(error_message=f"Model {model_name} not found")
    ).get_reco(user_id, k_recs)

    return RecoResponse(user_id=user_id, items=reco)


def add_views(app: FastAPI) -> None:
    app.include_router(router)
