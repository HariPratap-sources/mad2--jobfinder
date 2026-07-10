from models import db, Placement_Drive, Company_Profile
from services.service_error import ServiceError
from flask_security import current_user
from extensions import cache



class Placement_driveService():


    @staticmethod
    def get_all():
        return Placement_Drive.query.all()
     
    @staticmethod
    def get_by_id(id):
        drive = Placement_Drive.query.get(id)
        if not drive:
            raise ServiceError("not found")
        return drive
    

    @staticmethod
    def get_by_status(status, approve_status, drive_status):

        company = current_user.company_profile

        drive = Placement_Drive.query.join(Company_Profile).filter(Placement_Drive.status == status, Placement_Drive.drive_status == drive_status, Company_Profile.approval_status == approve_status, Placement_Drive.company_id == company.id).all()


        return drive
    
    @staticmethod
    def get_by_drive_status(status, drive_status, approve_status):

        company = current_user.company_profile

        drive = Placement_Drive.query.join(Company_Profile).filter(Placement_Drive.status == status, Placement_Drive.drive_status == drive_status, Company_Profile.approval_status == approve_status, Placement_Drive.company_id == company.id).all()
        
        return drive
    

    @staticmethod
    
    def get_company_drives(company_id, status="approved", drive_status="not_complete"):
        print("DB HIT")
        return Placement_Drive.query.join(Company_Profile).filter(
        Placement_Drive.company_id == company_id,
        Placement_Drive.status == status,
        Placement_Drive.drive_status == drive_status,
        Company_Profile.approval_status == "approved").all()
    




    @staticmethod
    def create(data):
        # need checks if key is present in model(data validation check)

        drive = Placement_Drive(**data)
        
        db.session.add(drive)
        db.session.commit()
        return drive




    @staticmethod
    def delete(id):
        drive = Placement_Drive.query.get(id)
        if not drive:
            raise ServiceError("not found")
        db.session.delete(drive)
        db.session.commit()
        return {"message": "drive with {id} deleted successfully"}


    @staticmethod
    def update(data):
        """{'id': 1, 'drive_name': 'drive1', .... }"""
        drive = Placement_Drive.query.get(data["id"])
        if not drive:
            raise ServiceError("not found")
        
        # need checks if key is present in model
        for key in data:
            setattr(drive, key, data[key])
    
        db.session.commit()
        return drive
    
    @staticmethod
    def complete_drive(id):

        company = current_user.company_profile

        drive = Placement_Drive.query.filter_by(id=id, company_id = company.id).first()

        if not drive:
            raise ServiceError("Drive not found")

        drive.drive_status = "completed"

        db.session.commit()

        return drive

             