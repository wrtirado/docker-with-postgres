from pydantic import BaseModel


class RequestCodeRequest(BaseModel):
    email: str


class VerifyCodeRequest(BaseModel):
    email: str
    auth_code: str
