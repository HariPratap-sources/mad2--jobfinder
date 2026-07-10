from flask import request, jsonify
from flask_restful import Resource, marshal, fields, marshal_with, reqparse
from services import ApplicationService
from .resource_utils import validate_date
from .marshal_fields import application_fields
from flask_security import current_user
from services import ServiceError
from flask_security.decorators import roles_required





parser = reqparse.RequestParser()
parser.add_argument("app_status", type= str)
parser.add_argument("student_id")
parser.add_argument("drive_id")

marshal_fields = application_fields
service = ApplicationService



"""/api/drive/:id"""
class ApplicationResource(Resource):
    # @marshal_with(marshal_fields) either decorator or return function

    def get(self, id):
        application = service.get_by_id(id)

        return marshal(application, marshal_fields), 200

    @roles_required("company")
    def put(self, id):
        data = request.get_json()
        if not data or "status" not in data:
            return {"message": "Status is required"}, 400
        
        try:
            application = service.update(application_id = id, status = data["status"])
            return marshal(application, marshal_fields), 200
        
        except ServiceError as e:
            return {"message": str(e)}, 400
        

    def patch(self, id):
        application = service.get_by_id(id)
        if not application:
            return {"message": "Application not found"}, 404

        data = request.get_json()
        data["id"] = id
        application = service.update(data)
        return marshal(application, marshal_fields), 200
           

    
"""/api/drive -> get, post"""
class ApplicationListResource(Resource):
    def get(self):
        application = service.get_all()

        return marshal(application, marshal_fields), 200
    
    def post(self):
        args = parser.parse_args()

        try:
            application = service.create(args)
            return marshal(application, marshal_fields), 200
        
        except ServiceError as e:
            return {"message": str(e)}, 400 
        



@roles_required("company")
def drive_application(id):
    application = ApplicationService.get_drive_applications(id)
    return {"application": application}
            
        
