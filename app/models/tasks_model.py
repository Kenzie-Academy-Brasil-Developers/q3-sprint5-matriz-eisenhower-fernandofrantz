from dataclasses import dataclass
from sre_constants import CATEGORY_UNI_LINEBREAK
from sqlalchemy import Column, String, Integer, ForeignKey
from app.configs.database import db
from app.models.exc import UrgencyImportanceOutOfRangeError
from sqlalchemy.orm import validates

class TasksModel(db.Model):
    __tablename__ = "tasks"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, unique=True, nullable=False)
    discription: str = Column(String, nullable=False)
    duration:  int = Column(Integer, nullable=False)
    importance: int = Column(Integer, nullable=False)
    urgency: int = Column(Integer, nullable=False)
    classification: str = Column(String)
    categories: str = Column(String, nullable=False)
    eisenhower_id:  int = Column(Integer, ForeignKey('eisenhowers.id'))

    def serializer(self):

        return {
            "id": self.id,
            "name": self.name,
            "discription": self.discription,
            "duration": self.duration,
            "classification": self.classification,
            "categories": self.categories,
        }
    
    @validates("importance", "urgency")
    def validate_fields(self, key, value):

        if(
            key == "urgency" and value > 2 or 
            key == "urgency" and value < 1 or
            key == "importance" and value > 2 or
            key == "importance" and value < 1
        ):
            raise UrgencyImportanceOutOfRangeError()

        return value
