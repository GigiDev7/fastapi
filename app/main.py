from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware
from .config import settings


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


models.Base.metadata.create_all(bind=engine)


app.include_router(post.router, prefix='/posts', tags=['Posts'])
app.include_router(user.router, prefix='/users', tags=['Users'])
app.include_router(auth.router, prefix='/login', tags=['Auth'])
app.include_router(vote.router, prefix='/vote', tags=['Vote'])
