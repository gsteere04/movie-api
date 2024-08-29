from pydantic import BaseModel
import uuid

class Movie(BaseModel):
    movie_id: uuid.UUID
    name: str
    year: int

class CreateMovieRequest(BaseModel):
    name: str
    year: int

class CreateMovieResponse(BaseModel):
    movie_id: uuid.UUID

class UpdateMovieRequest(BaseModel):
    name: str
    year: int

class UpdateMovieResponse(BaseModel):
    message: str

class DeleteMovieResponse(BaseModel):
    message: str
