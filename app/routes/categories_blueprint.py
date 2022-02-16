from flask import Blueprint
from app.controllers.categories_controller import post_category, patch_category, delete_category, get_all

bp_category = Blueprint("bp_category", __name__, url_prefix="/api")

bp_category.get("/category")(get_all)
bp_category.post("/category")(post_category)
bp_category.patch("/category/<int:id>")(patch_category)
bp_category.delete("/category/<int:id>")(delete_category)
