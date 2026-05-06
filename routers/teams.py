from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from dependencies import get_current_user
from models.team import Team
from schemas.team import TeamCreate

router = APIRouter(prefix="/teams",tags=["Teams"])

def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_all_teams(db: Session = Depends(get_db),user=Depends(get_current_user)):

    if user["role"] != "admin":
        raise HTTPException(status_code=403,detail="Admin only")

    return db.query(Team).all()
@router.get("/me")
def my_teams(db: Session = Depends(get_db),user=Depends(get_current_user)):

    return db.query(Team).filter(Team.registered_by == user["user_id"]).all()

@router.post("/")
def register_team(team: TeamCreate,db: Session = Depends(get_db),user=Depends(get_current_user)):

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
    team.team_name = updated.team_name
    team.captain_name = updated.captain_name
    db.commit()
    return {"message": "Team updated successfully"}

@router.delete("/{id}")
def delete_team(id: int,db: Session = Depends(get_db),user=Depends(get_current_user)):

    if user["role"] != "admin":
        raise HTTPException(status_code=403,detail="Admin only")
    team = db.query(Team).filter(Team.id == id).first()
    if not team:
        raise HTTPException(status_code=404,detail="Team not found")
    db.delete(team)
    db.commit()
    return {"message": "Team deleted successfully"}