from models import db, User, Student_Profile, Company_Profile, Application
from services.service_error import ServiceError
from extensions import cache
from sqlalchemy import or_

model = User


class UserService():
    @staticmethod
    def get_all():
        return model.query.all()
    
    @staticmethod
    def get_companies():
        return Company_Profile.query.all()
    
    @staticmethod
    @cache.cached(timeout=120)
    def get_approve_companies(status):
        return Company_Profile.query.filter_by(approval_status = status).all()
    
    @staticmethod
    
    def get_students():
        return Student_Profile.query.all()
    
    @staticmethod
    def approve(id):
        company = Company_Profile.query.get(id)
        company.approval_status = "approved"
        company.user.active = not company.user.active

        db.session.commit()
        
        return company
    
    @staticmethod
    def reject(id):
        company = Company_Profile.query.get(id)
        company.approval_status = "rejected"
        db.session.commit()
        return company
    
    @staticmethod
    def toggle_company_block(id):

        company = Company_Profile.query.get(id)

        if not company:
            return None

        company.is_blacklisted = not company.is_blacklisted

        db.session.commit()

        return company
    
    @staticmethod
    def toggle_student_block(id):

        student = Student_Profile.query.get(id)

        if not student:
            return None

        student.is_blacklisted = not student.is_blacklisted

        db.session.commit()
        

        return student
    
    @staticmethod
    
    def get_company_by_id(id):
        company = Company_Profile.query.get(id)
        if not company:
            raise ServiceError("company not found")
        return company
    
    

     
    @staticmethod
    def get_by_id(id):
        application = model.query.get(id)
        if not application:
            raise ServiceError("not found")
        return application
    

    @staticmethod
    def create(data):
        # need checks if key is present in model(data validation check)

        application = model(**data)
        db.session.add(application)
        db.session.commit()

        return application




    @staticmethod
    def delete(id):
        application = model.query.get(id)
        if not application:
            raise ServiceError("not found")
        db.session.delete(application)
        db.session.commit()
        return {"message": "application with {id} deleted successfully"}


    @staticmethod
    def update(data):
        # """{'id': 1, 'drive_name': 'drive1', .... }"""
        application = model.query.get(data["id"])
        if not application:
            raise ServiceError("not found")
        
        
        # need checks if key is present in model
        for key in data:
            setattr(application, key, data[key])
    
        db.session.commit()
        
        return application





    @staticmethod
    def search_users(query, search_type):
        search = f"%{query}%"

        student_results = []
        company_results = []

        if search_type == "student":
            # Students
            students = Student_Profile.query.filter(or_(
                    Student_Profile.fullname.ilike(search),
                    Student_Profile.qualification.ilike(search))).all()
            

            for s in students:
                student_results.append({
                    "type": "student",
                    "id": s.id,
                    "name": s.fullname,
                    "qualification": s.qualification,
                    "gender": s.gender,
                    "department": s.department,
                    "college_name": s.college_name,
                    "experience": s.experience,
                    "contact_no": s.contact_no,
                    "skill": s.skill,})
                
        elif search_type == "company":

            companies = Company_Profile.query.filter(
                Company_Profile.company_name.ilike(search)
            ).all()

            for c in companies:
                company_results.append({
                    "type": "company",
                    "id": c.id,
                    "company_name": c.company_name,
                    "Hr_contact": c.Hr_contact,
                    "description": c.description,
                    "company_type": c.company_type,
                    "website": c.website,
                    "company_field": c.company_field})
                
        return {"students": student_results,
                "companies": company_results}



             