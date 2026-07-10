from flask import request, jsonify
import os
from werkzeug.utils import secure_filename
from flask_restful import Resource, marshal, reqparse
from services import UserService
from services import StudentService
from services import Placement_driveService
from services import ApplicationService
from flask_restful import marshal
from .marshal_fields import drive_fields, company_fields, application_fields, student_fields
from flask_security.decorators import roles_required 
from flask_security import current_user
from flask import send_from_directory
from tasks.export import export_applications
from flask import send_file


parser = reqparse.RequestParser()
parser.add_argument("fullname", type= str)
parser.add_argument("age", type= int)
parser.add_argument("gender", type = str)

parser.add_argument("qualification", type = str)

parser.add_argument("department", type = str)

parser.add_argument("college_name", type = str)
parser.add_argument("experience", type = str)
parser.add_argument("contact_no", type = str)
parser.add_argument("skill")
parser.add_argument("user_id", type = int)


marshal_fields = student_fields
service = StudentService

class StudentDashboardResource(Resource):

    @roles_required("student")
    def get(self, id):
        student = service.get_by_id(id)

        
        return marshal(student ,marshal_fields),200
        

    @roles_required("student")
    def put(self):
        student = current_user.student_profile
        
        
        data = request.form.to_dict()

        resume_file = request.files.get("resume")

        if resume_file and resume_file.filename != "":
            #Delete ole resume
            if student.resume:
                filepath = os.path.join("uploads/resumes", student.resume)
                if os.path.exists(filepath):
                    os.remove(filepath)

            #Save new resume

            filename = secure_filename(resume_file.filename)
            unique_name = f"{student.id}_{filename}"
            new_filepath = os.path.join("uploads/resumes", unique_name)

            resume_file.save(new_filepath)

            data["resume"] = unique_name #store filename in DB


            
        data["id"] = student.id

        
        student = service.update(data)
            
        return marshal(student, marshal_fields), 200
    

    @roles_required("student")
    def patch(self, id):
        student = service.get_by_id(id)
        if not student:
            return {"message": "not found"}, 404

        data = request.get_json()
        data["id"] = id
        
        if (current_user.has_role("student")):

            student = service.update(data)
            return marshal(student, marshal_fields), 200

class StudentDashboardListResource(Resource):
    
    @roles_required("student")
    def get(self):

        
        student = current_user.student_profile
        companies = UserService.get_approve_companies("approved")
        
        applications = ApplicationService.get_student_applications(student.id)
    
        return {
            "companies": marshal(companies, company_fields),
            
            "applications":marshal(applications, application_fields),
        }
    

class StudentCompanyResource(Resource): 
    @roles_required("student")
    def get(self, id):

        company = UserService.get_company_by_id(id)

        drives = Placement_driveService.get_company_drives(id)

        return {
            "company": marshal(company, company_fields),
            "drives": marshal(drives, drive_fields)
        }, 200
    

class StudentApplicationHistory(Resource):
    @roles_required("student")
    def get(self):
        student = current_user.student_profile

        applications = ApplicationService.get_student_applications(student.id)
        return {
            "student": {
                "fullname": student.fullname,
                "qualification": student.qualification
            },
            "applications": marshal(applications, application_fields)
        }, 200


class ExportCSV(Resource):
    @roles_required("student")
    def post(self):
        student = current_user.student_profile
        task = export_applications.delay(student.id)
        return {
            "message": "Export started",
            "task_id": task.id,
            "student_id": student.id
        }, 202


class DownloadCSV(Resource):
    @roles_required("student")
    def get(self):
        student = current_user.student_profile

        filename = f"exports/student_{student.id}.csv"
        if not os.path.exists(filename):
            return {"message": "CSV file not generated yet"}, 404

        return send_file(filename, as_attachment = True, download_name= f"student_{student.id}.csv")

   
def get_resume(filename):
    
    return send_from_directory("uploads/resumes", filename)
