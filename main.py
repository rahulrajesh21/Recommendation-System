from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.db import MovieDatabase
from services.embedding_service import EmbeddingService
from api.v1 import movies
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs natively inside Uvicorn's active event loop during startup!
    print("Computing embeddings and loading catalog...")
    session = EmbeddingService()
    db = MovieDatabase(session)
    
    # Properly awaited inside the running loop!
    result = await db.load_movies()
    print("Movies loaded successfully:", result)

    app.state.session = session
    app.state.db = db
    yield


app = FastAPI(title="Movie Recommendation System", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    movies.router,
    prefix="/api/v1"
)