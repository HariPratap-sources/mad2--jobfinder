from flask_restful import Resource
from services import UserService
from services import Placement_driveService
from services import ApplicationService
from flask_restful import marshal
from resources.marshal_fields import drive_fields
from flask_security.decorators import roles_required 


class CompanyDashboardResource(Resource):
    @roles_required("company")

    def get(self):


        approve_drives = Placement_driveService.get_by_status("approved", "approved", "not_complete")

        completed_drives = Placement_driveService.get_by_drive_status("approved","completed", "approved")

        return {
            "approve_drives": marshal(approve_drives, drive_fields),
            "completed_drives": marshal(completed_drives, drive_fields)
        }
    