from fastapi import FastAPI

from src.i2global_backend.api.notes.view import notes_router
from src.i2global_backend.api.user.view import user_router
from src.i2global_backend.lifespan import lifespan
from src.i2global_backend.middleware.CustomMiddleware import AuthorizationMiddleware


def create_application() -> FastAPI:
	_app = FastAPI(
		title="i2global - backend",
		description="This API is for interacting with the i2global-backend. See docs for more information.",
		lifespan=lifespan,
	)
	return _app


app = create_application()
app.include_router(user_router)
app.include_router(notes_router)

app.add_middleware(AuthorizationMiddleware)