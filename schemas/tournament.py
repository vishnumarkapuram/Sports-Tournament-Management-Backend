from pydantic import BaseModel
class TournamentCreate(BaseModel):
    name: str
    sport: str
    start_date: str
    venue: str
    max_teams: int