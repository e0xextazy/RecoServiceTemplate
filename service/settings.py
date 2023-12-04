from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False)


class LogConfig(Config):
    model_config = SettingsConfigDict(case_sensitive=False, env_prefix="log_")
    level: str = "INFO"
    datetime_format: str = "%Y-%m-%d %H:%M:%S"


class ServiceConfig(Config):
    service_name: str = "reco_service"
    k_recs: int = 10
    auth_token: str = "AUTH_TOKEN_123"

    log_config: LogConfig


class ModelsConfig(Config):
    # Popular
    popular_by_user_path: str = "service/static_data/popular_model.json"
    general_popular_path: str = "service/static_data/general_popular.pkl"

    # UserKNN
    tfidf_userknn_model_path: str = "service/static_data/tfidf_20_model.json"

    # LightFM_nmslib
    index_path: str = "service/static_data/light_fm"
    ext_u_id2int_u_id_path: str = "service/static_data/ext_u_id2int_u_id.pkl"
    int_i_id2ext_i_id_path: str = "service/static_data/int_i_id2ext_i_id.pkl"
    int_u_id2vec_path: str = "service/static_data/int_u_id2vec.pkl"


def get_config() -> ServiceConfig:
    return ServiceConfig(
        log_config=LogConfig(),
    )
