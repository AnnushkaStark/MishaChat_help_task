from email_validator import validate_email
from pydantic import BaseModel, EmailStr, Field, validator


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6)

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    @validator("email")
    def email_check(cls, v: EmailStr) -> EmailStr:
        email_info = validate_email(v, check_deliverability=True)
        email = email_info.normalized
        return email


class UserCreateDB(UserBase):
    pass


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    username: str
