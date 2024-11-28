from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import router as index_router
from src.routes.auth import router as auth_router
from src.routes.users import router as users_router

app = FastAPI()
origins = ["http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(index_router, tags=["Index"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
