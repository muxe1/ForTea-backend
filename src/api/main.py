from core.routers import o2auth, photos, posts, users, user, comments
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError


app = FastAPI(title='TeaFor API', description='API for TeaFor')


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    ...

app.include_router(o2auth.router, prefix="/auth", tags=["Authorizations"])
app.include_router(user.router, prefix="/user", tags=["Current user"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(comments.router, prefix="/comments", tags=["Comments"])
app.include_router(photos.router, prefix="/photos", tags=["Photos"])
