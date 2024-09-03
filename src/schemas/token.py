from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str


class TokenAccessRefresh(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenVerify(BaseModel):
    is_valid: bool


class TokenPayload(BaseModel):
    username: str
    password: str