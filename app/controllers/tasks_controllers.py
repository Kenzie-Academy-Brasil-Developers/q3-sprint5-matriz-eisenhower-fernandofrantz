from flask import current_app, jsonify, request
from http import HTTPStatus
from app.models.tasks_model import TasksModel
from sqlalchemy.orm.exc import UnmappedInstanceError

def post_task():
    data = request.get_json()

    task = TasksModel(**data)

    current_app.db.session.add(task)
    current_app.db.session.commit()

    return jsonify(task.serializer()), HTTPStatus.CREATED

def patch_task(id):
    try:
        patch_data = request.get_json()

        task_to_patch = TasksModel.query.filter(TasksModel.id == id).first()

        patching_name = patch_data.get('name')
        patching_discription = patch_data.get('discription')
        patching_duration = patch_data.get('duration')
        patching_importance = patch_data.get('importance')
        patching_urgency = patch_data.get('urgency')
        patching_categories = patch_data.get('categories')
        patching_eisenhower_id = patch_data.get('eisenhower_id')
        
        patching_data = {
            "name": patching_name,
            "discription": patching_discription,
            "duration": patching_duration,
            "importance": patching_importance,
            "urgency": patching_urgency,
            "categories": patching_categories,
            "eisenhower_id": patching_eisenhower_id,
        }

        if(
            patching_discription == None and 
            patching_name == None and 
            patching_duration == None and 
            patching_importance == None and 
            patching_urgency == None and 
            patching_categories == None and 
            patching_eisenhower_id == None
            ):
            return {"wrong keys": "only accept keys: name and discription"}

        for key, value in patching_data.items():
                if(value != None):
                    setattr(task_to_patch, key, value)
                    current_app.db.session.add(task_to_patch)
                    current_app.db.session.commit()

        return '', HTTPStatus.OK
    except AttributeError: 
        return {"error": "id out of range"}

def delete_task(id):
    try:
        task_to_delete = TasksModel.query.filter(TasksModel.id == id).first()

        current_app.db.session.delete(task_to_delete)
        current_app.db.session.commit()

        return '', HTTPStatus.NO_CONTENT

    except UnmappedInstanceError:
        return {"msg": "task not found!"}, HTTPStatus.NOT_FOUND
        
def get_all():
    pass
