from pydantic import BaseModel, EmailStr


class RequestCodeRequest(BaseModel):
    email: EmailStr


class VerifyCodeRequest(BaseModel):
    email: EmailStr
    auth_code: str
