from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.movie_parser import parse_input_list
from app.tmdb_API import search_movie, get_movie_details
from app.recommendations import get_combined_recommendations
from pydantic import BaseModel

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://web-production-93d43.up.railway.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    with open("static/index.html") as f:
        return f.read()
    
class MovieListRequest(BaseModel):
    users: list[str]

@app.post("/recommendations")
def recommend_movies(data: MovieListRequest):
    user_lists = []
    all_titles = []

    for user_input in data.users:
        titles = parse_input_list(user_input)
        user_lists.append(set(titles))
        all_titles.extend(titles)

    movie_ids = [search_movie(title) for title in all_titles]
    movie_ids = list(set(filter(None, movie_ids)))

    overlap_titles = set.intersection(*user_lists) if len(user_lists) > 1 else set()  

    recommended_ids = get_combined_recommendations(movie_ids)

    recommended = [get_movie_details(mid) for mid in recommended_ids[:10]]

    overlap_ids = [search_movie(title) for title in overlap_titles]
    overlap = [get_movie_details(mid) for mid in overlap_ids if mid]

    return {
            "overlap": overlap,
            "recommendations": recommended
        }