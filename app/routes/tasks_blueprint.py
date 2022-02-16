from unittest.mock import patch
from flask import Blueprint
from app.controllers.tasks_controllers import post_task, patch_task, delete_task

bp_task = Blueprint("bp_task", __name__, url_prefix="/api")

bp_task.post("/tasks")(post_task)
bp_task.patch("/tasks/<int:id>")(patch_task)
bp_task.delete("/tasks/<int:id>")(delete_task)

