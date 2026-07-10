from resources.auth import auth_bp
from flask_restful import Api
from flask import Blueprint


from .placement_drive_resource import PlacementDriveListResource, PlacementDriveResource, complete_drive
from .application_resource import ApplicationResource, ApplicationListResource, drive_application

from .user_resource import UserListResource, UserResource, approve_user

from .admin_resource import AdminDashboardResource, AdminSearchResource, approve_company, company_block, student_block, approve_request, reject_request, reject_company

from .company_resource import CompanyDashboardResource
from .student_resource import StudentDashboardResource, StudentCompanyResource, StudentDashboardListResource, StudentApplicationHistory, ExportCSV, DownloadCSV, get_resume

api_bp = Blueprint("api", __name__, url_prefix= "/api")

api = Api(api_bp)

api.add_resource(PlacementDriveResource, "/drive/<int:id>")
api.add_resource(PlacementDriveListResource, "/drive")

api.add_resource(ApplicationResource, "/application/<int:id>")

api.add_resource(ApplicationListResource, "/application")

api.add_resource(UserResource, "/user/<int:id>" )
api.add_resource(UserListResource, "/user")


api_bp.add_url_rule("/user/<int:id>/approve", view_func= approve_user, methods = ["PATCH"])



api.add_resource(AdminDashboardResource, "/admin/dashboard")
api.add_resource(AdminSearchResource, "/admin/search")
api_bp.add_url_rule("/company/<int:id>/approve", view_func=approve_company, methods = ["PATCH"])
api_bp.add_url_rule("/company/<int:id>/reject", view_func=reject_company, methods = ["PATCH"])
api_bp.add_url_rule("/company/<int:id>/block", view_func=company_block, methods = ["PATCH"])
api_bp.add_url_rule("/student/<int:id>/block", view_func=student_block, methods = ["PATCH"])

api_bp.add_url_rule("/request/<int:id>/approve", view_func=approve_request, methods = ["POST"])
api_bp.add_url_rule("/request/<int:id>/reject", view_func=reject_request, methods = ["POST"])

api.add_resource(CompanyDashboardResource, "/company/dashboard")
api_bp.add_url_rule("/company/complete_drive/<int:id>", view_func= complete_drive, methods = ["POST"])
api_bp.add_url_rule("/company/drive/<int:id>/application", view_func = drive_application, methods = ["GET"] )
api.add_resource(StudentDashboardListResource, "/student/dashboard")
api.add_resource(StudentDashboardResource, "/student/dashboard")
api.add_resource(StudentCompanyResource, "/student/company/<int:id>")
api.add_resource(StudentApplicationHistory, "/student/history")
api.add_resource(ExportCSV, "/student/export")
api.add_resource(DownloadCSV, "/student/download")

api_bp.add_url_rule("/resume/<filename>", view_func= get_resume, methods = ["GET"])