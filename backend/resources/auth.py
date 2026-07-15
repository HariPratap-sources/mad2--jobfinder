from flask import Blueprint, request, jsonify
from flask_security.utils import verify_password, hash_password
from models import User, db, Student_Profile, Company_Profile
from flask import current_app
import os
from werkzeug.utils import secure_filename



auth_bp =  Blueprint("auth", __name__, url_prefix= "/api/auth")

@auth_bp.route("/login", methods = ["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "invalid input"}), 400
    
    user = User.query.filter_by(email = email).first()

    if not user:
        return jsonify({"message": "user not found"}), 404

    if not verify_password(password, user.password):
        return jsonify({"message": "wrong password"}), 400
    if user.roles:
        role = user.roles[0].name
    else:
        role = None

    # Company checks

    if role == "company":
        company = user.company_profile

        if not company:
            return jsonify({"message": "Company profile not found"}), 404
        
        if company.approval_status == "pending":
            return jsonify({"message": "Your company account not approved yet"}), 403
        
        if company.approval_status == "rejected":
            return jsonify({"message": "Your company account rejected by admin"}), 403

        if company.is_blacklisted:
            return jsonify({"message": "Your company is blacklisted by admin"}), 403
        
    if role == "student":

        student = user.student_profile

        if not student:
            return jsonify({"message": "Your profile not found"}), 404
        
        if student.is_blacklisted:
            return jsonify({"message": "You are blacklisted by admin"}), 403


    return jsonify({"id": user.id, "email": user.email, "role" : role, "token": user.get_auth_token()}), 200



@auth_bp.route("/register", methods = ["GET", "POST"])
def register():
    print("FORM:", request.form)
    print("FILES:", request.files)

    data = request.form

    print("Email:", data.get("email"))
    print("Password:", data.get("password"))
    print("Role:", data.get("role"))
    # data = request.form

    file = request.files.get("resume")

    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    datastore = current_app.datastore


    if not email or not password or role not in ["company", "student"]:
        return jsonify({"message": "invalid inputs"}), 400
    
    if User.query.filter_by(email = email).first():
        return jsonify({"message": "User already exists"}), 400
    
    try:

        if role == "company":
            active = False
        else:
            active = True


        user = datastore.create_user(email = email, password = hash_password(password), active = active)
        db.session.flush()

        if role == "student":
            resume_path = None
            if file and file.filename != "":
                filename = secure_filename(file.filename)
                unique_name = f"{user.id}_{filename}"
                filepath = os.path.join("uploads/resumes", unique_name)
                file.save(filepath)
                resume_path = unique_name
            new_student = Student_Profile(user_id=user.id, fullname=data.get("full_name"), age=data.get("age"), gender=data.get("gender"), qualification=data.get("qualification"), department=data.get("department"), college_name=data.get("college_name"), contact_no=data.get("mobile_no"), skill=data.get("skill"), experience=data.get("experience"), resume = resume_path)
            db.session.add(new_student)

        elif role == "company":
            new_company = Company_Profile(user_id = user.id,company_name=data.get("company_name"), Hr_contact=data.get("hr_contact"), description=data.get("description"), company_type=data.get("company_type"), company_field=data.get("company_field"), website=data.get("website"), approval_status="pending")
            db.session.add(new_company)
        
        role_obj = datastore.find_role(role)
        datastore.add_role_to_user(user, role_obj)
        
        db.session.commit() 

        return jsonify({
            "id": user.id,
            "email": user.email
        }), 201

    except Exception as e:
        db.session.rollback()
        print("ERROR:", e)
        return jsonify({"message": str(e)}), 500
    