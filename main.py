from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import auth
from routers import tournaments
from routers import teams

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Sports Tournament Manager", version="0.0.1")
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tournaments.router)
app.include_router(teams.router)

@app.get("/")
def home():
    return {"message": "Sports Tournament Manager API"}