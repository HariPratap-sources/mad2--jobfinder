from models import db, Application, Student_Profile
from flask_security import current_user
from services.service_error import ServiceError
from extensions import cache
model = Application

class ApplicationService():
    @staticmethod
    def get_all():
        return model.query.all()
     
    @staticmethod
    def get_by_id(id):
        application = model.query.get(id)
        if not application:
            raise ServiceError("not found")
        #allow admin
        if current_user.has_role("admin"):
            return application

        # allow company (only their data)
        if current_user.has_role("company"):
            if not current_user.company_profile:
                raise ServiceError("Company profile missing")
            
        if application.placement_drive.company_id != current_user.company_profile.id:
            raise ServiceError("Unauthorized access")
        return application
    
    @staticmethod
    def get_applied_app(status):
        return Application.query.filter_by(app_status = status).all()
    
    @staticmethod
    def get_student_applications(student_id):
        
        return Application.query.filter_by(student_id=student_id).all()
    

    @staticmethod
    def get_application_status(drive_id):
        student = current_user.student_profile

        if not student:
            return None

        application = Application.query.filter_by(student_id = student.id, drive_id = drive_id).first()

        if application:
            return application.app_status
        
        return None
    
    @staticmethod
    def get_drive_applications(drive_id):
        applications = Application.query.filter_by(drive_id = drive_id).all()

        if not applications:
            raise ServiceError("No application found for this drive")
        
        result = []

        for app in applications:
            result.append({
                "id": app.id,
                "job_title": app.placement_drive.job_title,
                "student_name": app.student_profile.fullname,
                "application_date": app.created_at
            })

        return result




    @staticmethod
    def create(data):
        # need checks if key is present in model(data validation check)
        student = current_user.student_profile

        exist_app = Application.query.filter_by(student_id = student.id, drive_id = data["drive_id"]).first()

        if exist_app:
            raise ServiceError("Aleardy applied for this drive")
        
        new_app = Application(student_id = student.id, drive_id = data["drive_id"], app_status = "applied")

        db.session.add(new_app)
        db.session.commit()
        return new_app




    @staticmethod
    def delete(id):
        application = model.query.get(id)
        if not application:
            raise ServiceError("not found")
        db.session.delete(application)
        db.session.commit()
        return {"message": f"application with {id} deleted successfully"}


    @staticmethod
    def update(application_id, status):
        # """{'id': 1, 'drive_name': 'drive1', .... }"""
        application = model.query.get(application_id)
        if not application:
            raise ServiceError("Application not found")
        
        allowed_status = ["applied", "shortlisted", "selected", "rejected"]

        if status not in allowed_status:
            raise ServiceError("Invalid Status")
        
        
        application.app_status = status
        db.session.commit()
        return application


             