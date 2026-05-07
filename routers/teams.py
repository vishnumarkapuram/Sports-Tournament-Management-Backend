from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user
from models.team import Team
from models.user import User
from schemas.team import TeamCreate

router = APIRouter(prefix="/teams",tags=["Teams"])

@router.get("/")
def get_all_teams(db: Session = Depends(get_db),user=Depends(get_current_user)):

    if user["role"] != "admin":
        raise HTTPException(status_code=403,detail="Only admins can view all the teams")
    results = db.query(Team, User.username).join(User, Team.registered_by == User.id).all()
    
    return [
        {
            "id": team.id,
            "team_name": team.team_name,
            "status": team.status,
            "captain_name": team.captain_name,
            "tournament_id": team.tournament_id,
            "registered_by": username
        }
        for team, username in results
    ]
@router.get("/me")
def my_teams(db: Session = Depends(get_db),user=Depends(get_current_user)):
    results = db.query(Team, User.username).join(User, Team.registered_by == User.id).filter(Team.registered_by == user["user_id"]).all()

    return [
        {
            "id": team.id,
            "team_name": team.team_name,
            "status": team.status,
            "captain_name": team.captain_name,
            "tournament_id": team.tournament_id,
            "registered_by": username
        }
        for team, username in results
    ]

@router.post("/")
def register_team(team: TeamCreate,db: Session = Depends(get_db),user=Depends(get_current_user)):

    existing_team = db.query(Team).filter(Team.team_name == team.team_name).first()
    if existing_team:
        raise HTTPException(status_code=400, detail="Team name already exists")

    new_team = Team(tournament_id=team.tournament_id,registered_by=user["user_id"],team_name=team.team_name,captain_name=team.captain_name)
    db.add(new_team)
    db.commit()

    return {"message": "Team registered successfully"}
@router.put("/{id}")
def update_team(id: int,updated: TeamCreate,db: Session = Depends(get_db),user=Depends(get_current_user)):

    team = db.query(Team).filter(Team.id == id).first()

    if not team:

        raise HTTPException(status_code=404,detail="Team not found")
    if (user["role"] != "admin"and team.registered_by != user["user_id"]):

        raise HTTPException(status_code=403,detail="Not authorized")

    if updated.team_name != team.team_name:
        existing_team = db.query(Team).filter(Team.team_name == updated.team_name).first()
        if existing_team:
            raise HTTPException(status_code=400, detail="Team name already exists")

    team.team_name = updated.team_name
    team.captain_name = updated.captain_name
    db.commit()
    return {"message": "Team updated successfully"}

@router.delete("/{id}")
def delete_team(id: int,db: Session = Depends(get_db),user=Depends(get_current_user)):

    if user["role"] != "admin":
        raise HTTPException(status_code=403,detail="Only admins can delete teams")
    team = db.query(Team).filter(Team.id == id).first()
    if not team:
        raise HTTPException(status_code=404,detail="Team not found")
    db.delete(team)
    db.commit()
    return {"message": "Team deleted successfully"}