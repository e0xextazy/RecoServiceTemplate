import json
from typing import List


class SimpleModel:
    def get_reco(self, user_id: int, k_recs: int) -> List[int]:
        return list(range(k_recs))


class PopularModel:
    def __init__(self, path: str = "service/static_data/popular_model.json") -> None:
        with open(path, "r", encoding="utf8") as file:
            self.model = json.load(file)
        self.general_popular = [10440, 15297, 9728, 13865, 4151, 3734, 2657, 4880, 142, 6809]

    def get_reco(self, user_id: int, k_recs: int) -> List[int]:
        return self.model.get(user_id, self.general_popular)


class TFiDFModel:
    def __init__(self, path: str = "service/static_data/tfidf_20_model.json") -> None:
        with open(path, "r", encoding="utf8") as file:
            self.model = json.load(file)

    def get_reco(self, user_id: int, k_recs: int) -> List[int]:
        return self.model.get(user_id, [])


class ModelsDict(dict):
    def get(self, key, default=None, error=None):
        res = super().get(key, default)
        if res is None:
            raise error

        return res


KNOWN_MODELS = ModelsDict({"simple_model": SimpleModel(), "popular_model": PopularModel(), "tfidf_model": TFiDFModel()})
