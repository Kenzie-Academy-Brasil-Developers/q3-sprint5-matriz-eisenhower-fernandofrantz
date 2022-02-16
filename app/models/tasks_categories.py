from sqlalchemy import Column, ForeignKey, String, Integer
from app.configs.database import db

class TasksCategoriesModel(db.Model):
    __tablename__ = "tasks_categories"

    id: int = Column(Integer, primary_key=True)
    task_id: int = Column(Integer, ForeignKey('tasks.id'), nullable=False, unique=True)
    category_id: int = Column(Integer, ForeignKey('categories.id'), nullable=False, unique=True)