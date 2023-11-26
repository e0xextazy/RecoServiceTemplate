from typing import List


class SimpleModel:
    def get_reco(self, user_id: int, k_recs: int) -> List[int]:
        return list(range(k_recs))


class ModelsDict(dict):
    def get(self, key, default=None, error=None):
        res = super().get(key, default)
        if res is None:
            raise error

        return res


KNOWN_MODELS = ModelsDict({"simple_model": SimpleModel()})
