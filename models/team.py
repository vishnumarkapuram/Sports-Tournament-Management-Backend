from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer,ForeignKey("tournaments.id"),nullable=False)
    registered_by = Column(Integer,ForeignKey("users.id"),nullable=False)
    team_name = Column(String,nullable=False,unique=True)
    captain_name = Column(String,nullable=False)
    status = Column(String,default="Pending")