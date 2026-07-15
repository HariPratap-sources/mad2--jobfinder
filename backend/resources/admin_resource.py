from flask import request
from flask_restful import Resource
from services import UserService
from services import Placement_driveService
from services import ApplicationService, RequestService
from flask_restful import marshal
from resources.marshal_fields import user_fields, drive_fields, company_fields, application_fields, student_fields, request_fields
from flask_security.decorators import roles_required 
from extensions import cache


class AdminDashboardResource(Resource):

    @roles_required("admin")
    def get(self):

        companies = UserService.get_companies()
        students = UserService.get_students()
        drives = Placement_driveService.get_all()
        applications = ApplicationService.get_all()
        requests = RequestService.get_all()

        stats = {
            "total_company": len(companies),
            "total_student": len(students),
            "total_drive": len(drives),
            "total_application": len(applications)
        }

        return {
            "stats": stats,
            "companies": marshal(companies, company_fields),
            "students": marshal(students, student_fields),
            "drives": marshal(drives, drive_fields),
            "applications": marshal(applications, application_fields),
            "requests": marshal(requests, request_fields)
        }
    
class AdminSearchResource(Resource):

    @roles_required("admin")
    def get(self):
        query = request.args.get("q", "").strip()
        search_type = request.args.get("type", "")

        if not query:
            return {"students": [], "companies": []}, 200

        results = UserService.search_users(query, search_type)

        return results, 200

@roles_required("admin")    
def approve_company(id):

    company = UserService.approve(id)
    return marshal(company, company_fields)

@roles_required("admin")    
def reject_company(id):

    company = UserService.reject(id)
    return marshal(company, company_fields)

@roles_required("admin")
def company_block(id):

    company = UserService.toggle_company_block(id)

    if not company:
        return {"message": "company not found"}, 404

    return marshal(company, company_fields), 200



@roles_required("admin")
def student_block(id):
 
    # print("BLOCK API CALLED", id)

    student = UserService.toggle_student_block(id)

    if not student:
        return {"message": "student not found"}, 404

    return marshal(student, student_fields), 200

@roles_required("admin")
def approve_request(id):

    request = RequestService.approve_request(id)
    cache.clear()
    return marshal(request, request_fields), 200


@roles_required("admin")
def reject_request(id):

    request = RequestService.reject_request(id)

    return marshal(request, request_fields), 200


