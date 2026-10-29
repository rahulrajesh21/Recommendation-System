import json
import pathlib
from models.movie import MovieData
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from services.embedding_service import EmbeddingService
from fastapi import Depends
from dataclasses import dataclass,field

file_path = pathlib.Path(__file__).resolve().parent / 'movies.json'


@dataclass
class MovieDatabase:
    embedding_service:EmbeddingService
    movies:list[MovieData] = field(default_factory=list)

    async def load_movies(self):
        movies = json.loads(file_path.read_text(encoding='utf-8'))
        for movie in movies:
            embedding = await self.embedding_service.embed_text(movie['description'])
            self.movies.append(MovieData(**movie, embedding=embedding))
        return {"size":len(self.movies),"Embedding Size":len(self.movies[0].embedding)}

    def get_movies(self)->list[MovieData]:
        return self.movies


