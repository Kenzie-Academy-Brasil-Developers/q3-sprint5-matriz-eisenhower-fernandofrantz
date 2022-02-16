from sqlalchemy import Column, String, Integer
from app.configs.database import db

class EisenhowersModel(db.Model):
    __tablename__ = "eisenhowers"

    id: int = Column(Integer, primary_key=True)
    type: str = Column(String(100), nullable=False)