from passlib.hash import bcrypt
from src.i2global_backend.api.database.database import User
from .jwt_token_generator import create_access_token, create_refresh_token


async def hash_password(password: str) -> str:
    return bcrypt.hash(password)

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.verify(plain_password, hashed_password)

async def sign_up_user(data):
    hashed_password = await hash_password(data.password)
    user = User(
        user_name=data.user_name,
        user_email=data.user_email,
        mobile_number=data.mobile_number,
        password=hashed_password,
    )
    await user.insert()
    return user

async def authenticate_user(user_email: str, password: str):
    user = await User.find_one(User.user_email == user_email)
    if user and await verify_password(password, user.password):
        return user
    return None

async def generate_tokens(user: User):
    access_token = create_access_token({"sub": user.user_email})
    refresh_token = create_refresh_token({"sub": user.user_email})

    # Add refresh token to the user's list in the database
    user.refresh_tokens.append(refresh_token)
    await user.save()

    return {"access_token": access_token, "refresh_token": refresh_token}

