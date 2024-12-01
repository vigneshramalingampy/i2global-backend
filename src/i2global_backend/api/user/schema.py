from pydantic import BaseModel, EmailStr, Field

class UserSignUpRequest(BaseModel):
    user_name: str
    user_email: EmailStr
    mobile_number: str = Field(min_length=10, max_length=10)
    password: str = Field(min_length=8)

class UserLoginRequest(BaseModel):
    user_email: EmailStr
    password: str

class UserResponse(BaseModel):
    user_id: str
    user_name: str
    user_email: EmailStr
    mobile_number: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str

class LogoutRequest(BaseModel):
    refresh_token: str