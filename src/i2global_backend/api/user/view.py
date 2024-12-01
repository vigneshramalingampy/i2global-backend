from fastapi import APIRouter, HTTPException

from src.i2global_backend.api.auth.jwt_authenticator import (
    authenticate_user,
    sign_up_user,
    generate_tokens,
)
from src.i2global_backend.api.auth.jwt_token_generator import (
    verify_token,
)
from src.i2global_backend.api.database.database import User
from src.i2global_backend.api.user.schema import (
    UserResponse,
    UserSignUpRequest,
    UserLoginRequest,
    TokenResponse,
    LogoutRequest,
)

user_router = APIRouter(prefix="/user",tags=["user"])

@user_router.post("/signin", response_model= UserResponse)
async def user_signin(user_data: UserSignUpRequest):
    existing_user = await User.find_one(User.user_email == user_data.user_email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    user = await sign_up_user(user_data)
    return UserResponse(
        user_id=str(user.user_id),
        user_name=user.user_name,
        user_email=user.user_email,
        mobile_number=user.mobile_number,
    )


@user_router.post("/login", response_model= TokenResponse)
async def user_login(user_data: UserLoginRequest):
    user = await authenticate_user(user_data.user_email, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    tokens = await generate_tokens(user)
    return TokenResponse(**tokens)


@user_router.post("/logout")
async def logout_user(token : LogoutRequest):
    payload = verify_token(token.refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token.")

    user = await User.find_one(User.user_id == payload["sub"])
    if not user or token.refresh_token not in user.refresh_tokens:
        raise HTTPException(status_code=401, detail="Invalid refresh token.")

    user.refresh_tokens.remove(token.refresh_token)
    await user.save()
    return {"message": "Logged out successfully"}