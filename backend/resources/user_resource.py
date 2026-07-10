from flask import request, jsonify
from flask_restful import Resource, marshal, fields, marshal_with, reqparse
from services import UserService
from .resource_utils import validate_date
from .marshal_fields import user_fields
from flask_security import current_user
from flask_security.decorators import roles_required




parser = reqparse.RequestParser()
parser.add_argument("email", type= str)

marshal_fields = user_fields
service = UserService







"""/api/drive/:id"""
class UserResource(Resource):
    
    def get(self, id):
       
        if (current_user.has_role("company") or current_user.has_role("student")) and current_user.id != id:
             return {'message': "not authorized"}, 401
        user = service.get_by_id(id)

        return marshal(user, marshal_fields), 200

    # admin/ (company/student) own data
    def put(self, id):
        if (current_user.has_role("company") or current_user.has_role("student")) and current_user.id != id:
             return {'message': "not authorized"}, 401
        user = service.get_by_id(id)
        if not user:
            return {"message", "not found"}, 404
        args = parser.parse_args()
        args["id"] = id
        user = service.update(args)
        return marshal(user, marshal_fields)

    def patch(self, id):
        if (current_user.has_role("company") or current_user.has_role("student")) and current_user.id != id:
             return {'message': "not authorized"}, 401
        user = service.get_by_id(id)
        if not user:
            return {"message", "not found"}, 404

        data = request.get_json()
        data["id"] = id
        user = service.update(data)
        return marshal(user, marshal_fields), 200


    def delete(self, id):
        if (current_user.has_role("company") or current_user.has_role("student")) and current_user.id != id:
             return {'message': "not authorized"}, 401
        user = service.get_by_id(id)
        if not user:
            return {"message", "not found"}, 404
        
        message = service.delete(id)
        return message, 200
    

    
               
           

    
"""/api/drive -> get, post"""
class UserListResource(Resource):
    # only admin
    @roles_required("admin")
    def get(self):
        
        user = service.get_all()

        return marshal(user, marshal_fields), 200
   

# /user/<int:id>/approve (only admin can do)
@roles_required("admin")
def approve_user(id):
    user = UserService.update({"active": True, "id": id})
    return marshal(user, user_fields)


