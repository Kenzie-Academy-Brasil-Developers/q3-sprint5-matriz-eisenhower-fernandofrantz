import imp
from flask import current_app, jsonify, request
from http import HTTPStatus
from app.models.categories_model import CategoryModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

def post_category():
    try:
        data = request.get_json()

        category = CategoryModel(**data)

        current_app.db.session.add(category)
        current_app.db.session.commit()

        return jsonify(category.serializer()), HTTPStatus.CREATED

    except IntegrityError:
        return {"msg": "category already exists!"}

def patch_category(id):
    try:
        patch_data = request.get_json()

        category_to_patch = CategoryModel.query.filter(CategoryModel.id == id).first()

        patching_name = patch_data.get('name')
        patching_discription = patch_data.get('discription')

        patching_data = {}
        if(patching_discription == None and patching_name == None):
            return {"wrong keys": "only accept keys: name and discription"}
        elif(patching_discription == None and patching_name != None):
            patching_data = {
                "name": patching_name
            }
        elif(patching_discription != None and patching_name == None):
            patching_data = {
                "discription": patching_discription
            }
        else:
            patching_data = {
                "name": patching_name,
                "discription": patching_discription
            }

        for key, value in patching_data.items():
                setattr(category_to_patch, key, value)

        current_app.db.session.add(category_to_patch)
        current_app.db.session.commit()

        return '', HTTPStatus.OK

    except AttributeError:
        return {"msg": "category not found!"}, HTTPStatus.NOT_FOUND

def delete_category(id):
    try:
        category_to_delete = CategoryModel.query.filter(CategoryModel.id == id).first()

        current_app.db.session.delete(category_to_delete)
        current_app.db.session.commit()

        return '', HTTPStatus.NO_CONTENT

    except UnmappedInstanceError:
        return {"msg": "category not found!"}, HTTPStatus.NOT_FOUND
        
def get_all():
    pass