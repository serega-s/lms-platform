from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import tables
from .api import router
from .database import engine


tables.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='LMS Platform API',
    description='Backend for new built LMS',
    version='1.0.0',
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)