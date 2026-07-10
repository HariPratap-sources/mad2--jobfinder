from flask_restful import fields


user_fields = {
    "id": fields.Integer,
    "email": fields.String,
    "active": fields.Boolean
}

student_fields = {
    "id": fields.Integer,
    "fullname": fields.String,
    "age": fields.Integer,
    "gender": fields.String,
    "qualification": fields.String,
    "department": fields.String,
    "college_name": fields.String,
    "experience": fields.String,
    "contact_no": fields.String,
    "skill": fields.String,
    "resume": fields.String,
    "is_blacklisted": fields.Boolean
}

company_fields = {
    "id": fields.Integer,
    "company_name": fields.String,
    "Hr_contact": fields.Integer,
    "description": fields.String,
    "company_field": fields.String,
    "company_type": fields.String,
    "website": fields.String,
    "approval_status": fields.String,
    "is_blacklisted": fields.Boolean
}
request_fields = {
    "id": fields.Integer,
    "data": fields.String,
    "status": fields.String,
    "type": fields.String,
    "user_id": fields.Integer,
    "created_at": fields.DateTime,
    "updated_at": fields.DateTime
}





drive_fields = {
    "id": fields.Integer,
    "drive_name": fields.String,
    "job_title": fields.String,
    "job_desc": fields.String,
    "eligibility_criteria": fields.String,
    "salary": fields.String,
    "application_deadline": fields.DateTime,
    "status": fields.String,
    "drive_status": fields.String,
    
    "company_profile": fields.Nested(company_fields),
    "created_at": fields.DateTime,
    "updated_at": fields.DateTime
    

}

application_fields = {
    "id": fields.Integer,
    "app_status": fields.String,
    "student_id": fields.Integer,
    "drive_id": fields.Integer,

    "student_profile": fields.Nested(student_fields),
    "placement_drive": fields.Nested(drive_fields),
    "created_at": fields.DateTime,
    "updated_at": fields.DateTime

}

