from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from dependencies import get_current_user
from models.tournament import Tournament
from schemas.tournament import TournamentCreate

router = APIRouter(prefix="/tournaments",tags=["Tournaments"])

def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()
@router.get("/")
def get_tournaments(db: Session = Depends(get_db)):
    return db.query(Tournament).all()
@router.post("/")
def create_tournament(tournament: TournamentCreate,db: Session = Depends(get_db),user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403,detail="Admin only")

    new_tournament = Tournament(name=tournament.name,sport=tournament.sport,start_date=tournament.start_date,venue=tournament.venue,max_teams=tournament.max_teams)
    db.add(new_tournament)
    db.commit()
    return {"message": "Tournament created successfully"}

@router.put("/{id}")
def update_tournament(id: int,updated: TournamentCreate,db: Session = Depends(get_db),user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403,detail="Admin only")

    tournament = db.query(Tournament).filter(Tournament.id == id).first()
    if not tournament:

        raise HTTPException(status_code=404,detail="Tournament not found")
    tournament.name = updated.name
    tournament.sport = updated.sport
    tournament.start_date = updated.start_date
    tournament.venue = updated.venue
    tournament.max_teams = updated.max_teams
    db.commit()

    return {"message": "Tournament updated successfully"}

@router.delete("/{id}")
def delete_tournament(id: int,db: Session = Depends(get_db),user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403,detail="Admin only")
    tournament = db.query(Tournament).filter(Tournament.id == id).first()

    if not tournament:

        raise HTTPException(status_code=404,detail="Tournament not found")
    db.delete(tournament)
    db.commit()
    return {"message": "Tournament deleted successfully"}