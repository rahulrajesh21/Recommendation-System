from models.movie import MovieData, MovieSearchResult
from services.consine_simlarity import consine_simlarity
from services.embedding_service import EmbeddingService
from db.db import MovieDatabase

# Notice: NO "from main import db, session" here!


async def find_similar_movies(
    text: str, 
    db: MovieDatabase, 
    session: EmbeddingService,  # <--- 1. Accepts session from route
    top_k: int = 3
) -> list[MovieSearchResult]:
    movies = db.get_movies()
    text_embedding = await session.embed_text(text)

    scored_movies: list[MovieSearchResult] = []

    for movie in movies:
        score = consine_simlarity(text_embedding, movie.embedding)
        # 2. Construct MovieSearchResult directly (no **movie crash)
        scored_movies.append(
            MovieSearchResult(
                title=movie.title,
                description=movie.description,
                imageUrl=movie.imageUrl,
                similarity_score=round(score, 4)
            )
        )

    scored_movies.sort(key=lambda x: x.similarity_score, reverse=True)
    return scored_movies[:top_k]


def find_movie_by_title(title: str, db: MovieDatabase) -> MovieData | None:
    movies = db.get_movies()
    clean_title = title.strip().lower()
    for movie in movies:
        if movie.title.strip().lower() == clean_title:
            return movie
    return None


def find_similar_movies_by_title(
    title: str, 
    db: MovieDatabase, 
    top_k: int = 3
) -> list[MovieSearchResult]:
    movie = find_movie_by_title(title, db)
    if movie is None:
        return []

    movies = db.get_movies()
    scored_movies: list[MovieSearchResult] = []
    
    for other_movie in movies:
        # Skip the movie itself
        if movie.title.strip().lower() == other_movie.title.strip().lower():
            continue

        score = consine_simlarity(movie.embedding, other_movie.embedding)
        
        # 3. Append other_movie (the recommendation), NOT movie
        scored_movies.append(
            MovieSearchResult(
                title=other_movie.title,
                description=other_movie.description,
                imageUrl=other_movie.imageUrl,
                similarity_score=round(score, 4)
            )
        )

    scored_movies.sort(key=lambda x: x.similarity_score, reverse=True)
    return scored_movies[:top_k]