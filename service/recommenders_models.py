import json
import pickle
from typing import List

import nmslib

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


class nmslib_model:
    def __init__(
        self, index_path: str, ext_u_id2int_u_id_path: str, int_i_id2ext_i_id_path: str, int_u_id2vec_path: str
    ) -> None:
        with open(ext_u_id2int_u_id_path, "rb") as file:
            self.ext_u_id2int_u_id = pickle.load(file)

        with open(int_i_id2ext_i_id_path, "rb") as file:
            self.int_i_id2ext_i_id = pickle.load(file)

        with open(int_u_id2vec_path, "rb") as file:
            self.int_u_id2vec = pickle.load(file)

        self.model = nmslib.init(method="hnsw", space="negdotprod", data_type=nmslib.DataType.DENSE_VECTOR)
        nmslib.loadIndex(self.model, index_path)

    def get_reco(self, user_id: int, k_recs: int) -> List[int]:
        int_u_id = self.ext_u_id2int_u_id.get(user_id, None)
        if int_u_id:
            u_vec = self.int_u_id2vec[int_u_id]
            int_recos = list(self.model.knnQuery(u_vec, k=k_recs)[0])
            ext_recos = [self.int_i_id2ext_i_id[rec] for rec in int_recos]
        else:
            ext_recos = []

        return ext_recos


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
        "lightfm_nmslib_model": nmslib_model(
            models_cfg.index_path,
            models_cfg.ext_u_id2int_u_id_path,
            models_cfg.int_i_id2ext_i_id_path,
            models_cfg.int_u_id2vec_path,
        ),
        "dssm_nmslib_model": nmslib_model(
            models_cfg.dssm_index_path,
            models_cfg.dssm_ext_u_id2int_u_id_path,
            models_cfg.dssm_int_i_id2ext_i_id_path,
            models_cfg.dssm_int_u_id2vec_path,
        ),
    }
)
