from pydantic import BaseModel
class TeamCreate(BaseModel):
    tournament_id: int
    team_name: str
    captain_name: str