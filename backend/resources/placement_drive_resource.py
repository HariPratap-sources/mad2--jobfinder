from flask import request, jsonify
from flask_restful import Resource, marshal, fields, marshal_with, reqparse
from services import Placement_driveService, RequestService, ApplicationService
from .resource_utils import validate_date
from .marshal_fields import drive_fields
from flask_security import current_user
from flask_security.decorators import roles_required
from datetime import datetime
from extensions import cache




parser = reqparse.RequestParser()
parser.add_argument("drive_name", type= str)
parser.add_argument("job_title")
parser.add_argument("job_desc")

parser.add_argument("eligibility_criteria")

parser.add_argument("salary")

parser.add_argument("application_deadline", type = validate_date)
parser.add_argument("company_id")

marshal_fields = drive_fields
service = Placement_driveService



"""/api/drive/:id"""
class PlacementDriveResource(Resource):
    # @marshal_with(marshal_fields) either decorator or return function
    @cache.cached(timeout=60, key_prefix= lambda: f"drive_{request.view_args['id']}_user_{current_user.id}")
    def get(self, id):
        drive = service.get_by_id(id)

        if (current_user.has_role("admin")):

            return marshal(drive,marshal_fields),200
        

        status = ApplicationService.get_application_status(id)

        return {"drive":marshal(drive, marshal_fields), "app_status": status}, 200
    
    @roles_required("company")
    def put(self, id):
        drive = service.get_by_id(id)
        if not drive:
            return {"message": "not found"}, 404
        args = parser.parse_args()
        args["company_id"] = current_user.company_profile.id
        args["id"] = id

        
        if args.get("application_deadline"):
            args["application_deadline"] = args["application_deadline"].isoformat()

        if (current_user.has_role("company")):
            RequestService.create({"data": dict(args), "status": "created", "type": "put drive", "user_id": current_user.id})
            return {"message": "request for service, wait admin to approve"}, 200

        drive = service.update(args)
        cache.clear()
        return marshal(drive, marshal_fields)
    



    @roles_required("company")
    def patch(self, id):
        drive = service.get_by_id(id)
        if not drive:
            return {"message": "not found"}, 404

        data = request.get_json()
        data["id"] = id
        data["company_id"] = current_user.company_profile.id
        
        if data.get("application_deadline"):
            data["application_deadline"] = data["application_deadline"].isoformat()

        if (current_user.has_role("company")):
            RequestService.create({"data": data, "status": "created", "type": "patch drive", "user_id": current_user.company_profile.id})
            return {"message": "request for service, wait admin to approve"}, 200


        drive = service.update(data)
        cache.clear()
        return marshal(drive, marshal_fields), 200

    @roles_required("company")
    def delete(self, id):
        drive = service.get_by_id(id)
        if not drive:
            return {"message": "not found"}, 404
        # Check existing request first
        exist_request = RequestService.get_by_drive_and_type(id, "delete drive")
        if exist_request:

            if exist_request.status == "created":
                return {"message": "Request already pending"}, 400
            
            if exist_request.status == "approved":
                return {"message": "Already approved"}, 400
            
        if (current_user.has_role("company")):
            RequestService.create({"data": {"id": id}, "status": "created", "type": "delete drive", "user_id": current_user.company_profile.id})
            return {"message": "request for service, wait admin to approve"}, 200

        
        message = service.delete(id)
        cache.clear()
        return message, 200
    

    
               
           

    
"""/api/drive -> get, post"""
class PlacementDriveListResource(Resource):
    def get(self):
        drive = service.get_all()

        return marshal(drive, marshal_fields), 200
    
    @roles_required("company")
    def post(self):
        
        args = parser.parse_args()
        if args.get("application_deadline"):
            args["application_deadline"] = args["application_deadline"].isoformat()
        args["company_id"] = current_user.company_profile.id

          
        if (current_user.has_role("company")):


            RequestService.create({"data": dict(args), "status": "created", "type": "post drive", "user_id": current_user.company_profile.id})
            return {"message": "request for service, wait admin to approve"}, 200


        drive = service.create(args)
        cache.clear()
        return marshal(drive, marshal_fields), 200


@roles_required("company")
def complete_drive(id):
    drive = Placement_driveService.complete_drive(id)
    return {"message": "Drive mark as completed", "drive_id": drive.id}, 200