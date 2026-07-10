from models import db, Request
from services.service_error import ServiceError
from services import Placement_driveService
from datetime import datetime

REQUEST_HANDLERS = {
    "post drive": lambda data: Placement_driveService.create(data),

    "put drive": lambda data: Placement_driveService.update(data),

    "delete drive": lambda data: Placement_driveService.delete(data["id"]),

    "complete drive": lambda data: Placement_driveService.complete_drive(data["id"]),
}


model = Request

class RequestService():
    @staticmethod
    def get_all():
        return model.query.all()
     
    @staticmethod
    def get_by_id(id):
        request = model.query.get(id)
        if not request:
            raise ServiceError("not found")
        return request
    

    @staticmethod
    def create(data):
        # need checks if key is present in model(data validation check)

        request = model(**data)
        db.session.add(request)
        db.session.commit()
        return request




    @staticmethod
    def delete(id):
        request = model.query.get(id)
        if not request:
            raise ServiceError("not found")
        db.session.delete(request)
        db.session.commit()
        return {"message": "application with {id} deleted successfully"}


    @staticmethod
    def update(data):
        # """{'id': 1, 'drive_name': 'drive1', .... }"""
        request = model.query.get(data["id"])
        if not request:
            raise ServiceError("not found")
        
        # need checks if key is present in model
        for key in data:
            setattr(request, key, data[key])
    
        db.session.commit()
        return request
    

    @staticmethod
    def approve_request(id):

        request = Request.query.get(id)

        if not request:
            raise ServiceError("request not found")

        handler = REQUEST_HANDLERS.get(request.type)

        if not handler:
            raise ServiceError("Invalid request type")

        # make a copy of data
        data = dict(request.data)

        if not data.get("company_id"):
            data["company_id"] = request.user_id

        deadline = data.get("application_deadline")
        if deadline and isinstance(deadline, str):
            data["application_deadline"] = datetime.fromisoformat(data["application_deadline"])


        if not data.get("company_id"):
            raise ServiceError("company_id missing")

        data["status"] = "approved"
        handler(data)
        # print(request.data)

        request.status = "approved"

        db.session.commit()

        return request
    
    @staticmethod
    def reject_request(id):

        request = Request.query.get(id)

        if not request:
            raise ServiceError("request not found")

        request.status = "rejected"

        db.session.commit()

        return request
    @staticmethod
    def get_by_drive_and_type(drive_id, req_type):
        return Request.query.filter(
        Request.type == req_type,
        Request.data["id"].as_integer() == drive_id).order_by(Request.id.desc()).first()



                