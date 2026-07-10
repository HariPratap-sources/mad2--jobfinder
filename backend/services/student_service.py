from models import db, Student_Profile
from flask_security import current_user
from services.service_error import ServiceError
from extensions import cache



class StudentService():

    @staticmethod
    
    def get_all():
        return Student_Profile.query.all()
     
    @staticmethod
   
    def get_by_id(id):
        print("DB HIT (student by id)")
        student = Student_Profile.query.get(id)
        if not student:
            raise ServiceError("student not found")
        return student
    
    @staticmethod
    def update(data):
        
        """{'id': 1, 'fullname': 'ram', .... }"""
        student = Student_Profile.query.get(data["id"])
        if not student:
            raise ServiceError("not found")
        if student.user_id != current_user.id:
            raise ServiceError("Unauthorized")
        
        # need checks if key is present in model

        allowed_fields = [
        "fullname", "age", "gender", "qualification",
        "department", "college_name", "experience",
        "contact_no", "skill", "resume"]

        for key in allowed_fields:
            if key in data and data[key] is not None:

                setattr(student, key, data[key])
    
        db.session.commit()
        return student
    
    
    @staticmethod
    def create(data):
        # need checks if key is present in model(data validation check)

        student = Student_Profile(**data)
        
        db.session.add(student)
        db.session.commit()

        
        return student
    
