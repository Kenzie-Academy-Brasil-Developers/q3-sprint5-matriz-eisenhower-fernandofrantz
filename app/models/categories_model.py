from sqlalchemy import Column, String, Integer
from app.configs.database import db

class CategoryModel(db.Model):
    __tablename__ = "categories"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, unique=True, nullable=False)
    discription: str = Column(String, nullable=False)

    def serializer(self):
        return {
            "id": self.id,
            "name": self.name,
            "discription": self.discription
        }