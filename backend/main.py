import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import (
    Movie,
    CreateMovieRequest,
    CreateMovieResponse,
    UpdateMovieRequest,
    UpdateMovieResponse,
    DeleteMovieResponse,
)

movies: list[Movie] = [
    Movie(movie_id=uuid.uuid4(), name="Spider-Man", year=2002),
    Movie(movie_id=uuid.uuid4(), name="Thor: Ragnarok", year=2017),
    Movie(movie_id=uuid.uuid4(), name="Iron Man", year=2008),
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/movies")
async def get_movies() -> list[Movie]:
    """Returns a list of all movies."""
    return movies

@app.post("/movies")
async def create_movie(new_movie: CreateMovieRequest) -> CreateMovieResponse:
    """Adds a new movie to the list."""
    if any(existing_movie.name == new_movie.name for existing_movie in movies):
        raise HTTPException(status_code=400, detail="Movie with this name already exists")
    
    movie = Movie(movie_id=uuid.uuid4(), name=new_movie.name, year=new_movie.year)
    movies.append(movie)
    return CreateMovieResponse(movie_id=movie.movie_id)

@app.put("/movies/{movie_id}")
async def update_movie(movie_id: uuid.UUID, updated_movie: UpdateMovieRequest) -> UpdateMovieResponse:
    """Updates an existing movie's details or creates a new movie if it does not exist."""
    for i, movie in enumerate(movies):
        if movie.movie_id == movie_id:
            movies[i] = Movie(movie_id=movie_id, name=updated_movie.name, year=updated_movie.year)
            return UpdateMovieResponse(message="Movie updated successfully")
    
    new_movie = Movie(movie_id=movie_id, name=updated_movie.name, year=updated_movie.year)
    movies.append(new_movie)
    return UpdateMovieResponse(message="Movie created successfully")

@app.delete("/movies/{movie_id}")
async def delete_movie(movie_id: uuid.UUID) -> DeleteMovieResponse:
    global movies
    movies = [movie for movie in movies if movie.movie_id != movie_id]
    return DeleteMovieResponse(message="Movie deleted successfully")
