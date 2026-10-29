from pydantic import BaseModel,Field, ConfigDict



class MovieData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    title:str
    description:str
    imageUrl:str = Field(validation_alias='image')
    embedding:list[float]

class MovieSearchResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    title: str
    description: str
    imageUrl: str = Field(validation_alias='image')
    similarity_score: float