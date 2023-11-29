import json
import pickle
from typing import List

from .settings import ModelsConfig

models_cfg = ModelsConfig()


def keystoint(x):
    return {int(k): v for k, v in x.items()}


class SimpleModel:
    def get_reco(self, user_id: int, k_recs: int) -> List[int]:
        return list(range(k_recs))


class PopularModel:
    def __init__(self, pop_by_user_path: str, gen_pop_path: str) -> None:
        with open(pop_by_user_path, "r", encoding="utf8") as file:
            self.model = json.load(file, object_hook=keystoint)
        with open(gen_pop_path, "rb") as file:
            self.general_popular = pickle.load(file)

    def get_reco(self, user_id: int, k_recs: int) -> List[int]:
        return self.model.get(user_id, self.general_popular)


class TFiDFUserKNNModel:
    def __init__(self, path: str) -> None:
        with open(path, "r", encoding="utf8") as file:
            self.model = json.load(file, object_hook=keystoint)

    def get_reco(self, user_id: int, k_recs: int) -> List[int]:
        return self.model.get(user_id, [])


class ModelsDict(dict):
    def get(self, key, default=None, error=None):
        res = super().get(key, default)
        if res is None:
            raise error

        return res


KNOWN_MODELS = ModelsDict(
    {
        "simple_model": SimpleModel(),
        "popular_model": PopularModel(models_cfg.popular_by_user_path, models_cfg.general_popular_path),
        "tfidf_userknn_model": TFiDFUserKNNModel(models_cfg.tfidf_userknn_model_path),
    }
)
