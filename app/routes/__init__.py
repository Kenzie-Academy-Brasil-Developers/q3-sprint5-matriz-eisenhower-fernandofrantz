from flask import Flask
from app.routes.categories_blueprint import bp_category
from app.routes.tasks_blueprint import bp_task


def init_app(app: Flask):
    app.register_blueprint(bp_category)
    app.register_blueprint(bp_task)