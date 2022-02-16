from dataclasses import dataclass
from sqlalchemy import Column, String, Integer, ForeignKey
from app.configs.database import db

class TasksModel(db.Model):
    __tablename__ = "tasks"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, nullable=False)
    discription: str = Column(String, nullable=False)
    duration:  int = Column(Integer, nullable=False)
    importance:  int = Column(Integer, nullable=False)
    urgency:  int = Column(Integer, nullable=False)
    categories: str = Column(String, nullable=False)
    eisenhower_id:  int = Column(Integer, ForeignKey('eisenhowers.id'), nullable=False, unique=True)

    def serializer(self):
        return {
            "id": self.id,
            "name": self.name,
            "discription": self.discription,
            "duration": self.duration,
            "importance": self.importance,
            "urgency": self.urgency,
            "categories": self.categories,
            "eisenhower_id": self.eisenhower_id
        }