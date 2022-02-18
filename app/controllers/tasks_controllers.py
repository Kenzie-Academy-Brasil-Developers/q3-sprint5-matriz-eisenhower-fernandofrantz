from tabnanny import check
from flask import current_app, jsonify, request
from http import HTTPStatus
from app.models.categories_model import CategoryModel
from app.models.tasks_model import TasksModel
from sqlalchemy.orm.exc import UnmappedInstanceError
from app.models.exc import UrgencyImportanceOutOfRangeError
from sqlalchemy.exc import IntegrityError

def post_task():
    try:
        data = request.get_json()

        task = TasksModel(**data)

        urgency = data['urgency']
        importance = data['importance']

        if (urgency == 1 and importance == 1):
            data['classification'] = "Do It First"
            data['eisenhower_id'] = 1

        if (urgency == 2 and importance == 1):
            data['classification'] = "Schedule It"
            data['eisenhower_id'] = 2

        if (urgency == 1 and importance == 2):
            data['classification'] = "Delegate It"
            data['eisenhower_id'] = 3

        if (urgency == 2 and importance == 2):
            data['classification'] = "Delete It"
            data['eisenhower_id'] = 4

        setattr(task, 'classification', data['classification'])
        setattr(task, 'eisenhower_id', data['eisenhower_id'])

        categories = list(data['categories'])
        for category_name in categories:
            check_category = CategoryModel.query.filter(CategoryModel.name == category_name).first()
            if(check_category == None):
                check_category = {
                    "name": category_name,
                    "discription": 'automatic creation'
                }
        current_app.db.session.add(CategoryModel(**check_category))

        current_app.db.session.add(task)
        current_app.db.session.commit()

        return jsonify(task.serializer()), HTTPStatus.CREATED

    except UrgencyImportanceOutOfRangeError:
        data = request.get_json()
        print(data)

        return {
                "msg": {
                    "valid_options": {
                    "importance": [1, 2],
                    "urgency": [1, 2]
                    },
                    "recieved_options": {
                    "importance": data['importance'],
                    "urgency": data['urgency']
                    }
                }
                }, HTTPStatus.BAD_REQUEST
    
    except IntegrityError:
        return  {"msg": "task already exists!"}


def patch_task(id):
    try:
        patch_data = request.get_json()

        task_to_patch = TasksModel.query.filter(TasksModel.id == id).first()

        print(task_to_patch.__dict__)

        patching_name = patch_data.get('name')
        patching_discription = patch_data.get('discription')
        patching_duration = patch_data.get('duration')
        patching_importance = patch_data.get('importance')
        patching_urgency = patch_data.get('urgency')
        patching_categories = patch_data.get('categories')
        patching_eisenhower_id = patch_data.get('eisenhower_id')
        patching_classification = patch_data.get('classification')
        
        patching_data = {
            "name": patching_name,
            "discription": patching_discription,
            "duration": patching_duration,
            "importance": patching_importance,
            "urgency": patching_urgency,
            "categories": patching_categories,
            "classification": patching_classification,
            "eisenhower_id": patching_eisenhower_id
        }

        if(patching_importance != None and patching_urgency == None):
            importance = patch_data['importance']
            urgency = task_to_patch.__dict__['urgency']

            if (urgency == 1 and importance == 1):
                patching_data['classification'] = "Do It First"
                patching_data['eisenhower_id'] = 1

            if (urgency == 2 and importance == 1):
                patching_data['classification'] = "Schedule It"
                patching_data['eisenhower_id'] = 2

            if (urgency == 1 and importance == 2):
                patching_data['classification'] = "Delegate It"
                patching_data['eisenhower_id'] = 3

            if (urgency == 2 and importance == 2):
                patching_data['classification'] = "Delete It"
                patching_data['eisenhower_id'] = 4

            setattr(task_to_patch, 'classification', patching_data['classification'])
            setattr(task_to_patch, 'eisenhower_id', patching_data['eisenhower_id'])

        if(patching_importance == None and patching_urgency != None):
            urgency = patch_data['urgency']
            importance = task_to_patch.__dict__['importance']

            if (urgency == 1 and importance == 1):
                patching_data['classification'] = "Do It First"
                patching_data['eisenhower_id'] = 1

            if (urgency == 2 and importance == 1):
                patching_data['classification'] = "Schedule It"
                patching_data['eisenhower_id'] = 2

            if (urgency == 1 and importance == 2):
                patching_data['classification'] = "Delegate It"
                patching_data['eisenhower_id'] = 3

            if (urgency == 2 and importance == 2):
                patching_data['classification'] = "Delete It"
                patching_data['eisenhower_id'] = 4

            setattr(task_to_patch, 'classification', patching_data['classification'])
            setattr(task_to_patch, 'eisenhower_id', patching_data['eisenhower_id'])

        if(patching_importance != None and patching_urgency != None):
            urgency = patch_data['urgency']
            importance = patch_data['importance']

            if (urgency == 1 and importance == 1):
                patching_data['classification'] = "Do It First"
                patching_data['eisenhower_id'] = 1

            if (urgency == 2 and importance == 1):
                patching_data['classification'] = "Schedule It"
                patching_data['eisenhower_id'] = 2

            if (urgency == 1 and importance == 2):
                patching_data['classification'] = "Delegate It"
                patching_data['eisenhower_id'] = 3

            if (urgency == 2 and importance == 2):
                patching_data['classification'] = "Delete It"
                patching_data['eisenhower_id'] = 4

            setattr(task_to_patch, 'classification', patching_data['classification'])
            setattr(task_to_patch, 'eisenhower_id', patching_data['eisenhower_id'])

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

        return jsonify(task_to_patch.serializer()), HTTPStatus.OK

    except AttributeError: 
        return {"error": "id out of range"}
    
    except UrgencyImportanceOutOfRangeError:
        return {"error": "acceptable values for urgency and importance are [1,2]"}



def delete_task(id):
    try:
        task_to_delete = TasksModel.query.filter(TasksModel.id == id).first()

        current_app.db.session.delete(task_to_delete)
        current_app.db.session.commit()

        return '', HTTPStatus.NO_CONTENT

    except UnmappedInstanceError:
        return {"msg": "task not found!"}, HTTPStatus.NOT_FOUND
