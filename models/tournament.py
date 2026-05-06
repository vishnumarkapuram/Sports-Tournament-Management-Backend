from sqlalchemy import Column, Integer, String
from database import Base
class Tournament(Base):
    __tablename__ = "tournaments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sport = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    venue = Column(String, nullable=False)
    max_teams = Column(Integer, nullable=False)