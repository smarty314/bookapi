from pydantic import BaseSettings, BaseModel


class Settings(BaseSettings):
    app_name: str = "API Demo"
    app_description: str = "API implemented with FastAPI"
    app_version: str = "1.0.0"
    # oauth_jwt_issuer: str = "https://dev-01515259.okta.com/oauth2/default"
    # oauth_jwt_audience: str = "api://apidemo314"
    # oauth_docs_client_id: str = "0oa46byk14IilF1KD5d7"


settings = Settings(
    # oauth_docs_client_id="",
)
