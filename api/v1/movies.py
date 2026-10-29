from fastapi import APIRouter, HTTPException, Request, status
from services.similar_movies import find_similar_movies, find_similar_movies_by_title

# Notice: NO "from main import db"! This completely eliminates the circular import.

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/search")
async def search(query: str, request: Request):  # <--- 1. Declare request: Request here
    # 2. Grab db and session from app.state
    db = request.app.state.db
    session = request.app.state.session

    # 3. Call service with query, db, and session
    movies = await find_similar_movies(query, db, session)

    return {
        "movies": [movie.model_dump() for movie in movies]
    }


@router.get("/")
def get_movies(request: Request):  # <--- Add request: Request
    db = request.app.state.db
    movies = db.get_movies()
    return {
        "movies": [movie.model_dump(exclude={"embedding"}) for movie in movies]
    }


@router.get("/{title}/similar")  # <--- Added leading slash "/"
def movie_suggestion(title: str, request: Request):  # <--- Add request: Request
    db = request.app.state.db
    movies = find_similar_movies_by_title(title, db)

    if not movies:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie '{title}' not found in catalog"
        )

    return {
        "movies": [movie.model_dump() for movie in movies]
    }