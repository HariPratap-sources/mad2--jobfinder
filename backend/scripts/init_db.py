from app import app
from models import db 
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import hash_password




with app.app_context():
    db.drop_all() #delete all data
    db.create_all() #create fresh tables
    datastore : SQLAlchemyUserDatastore = app.datastore


    admin_role = datastore.find_or_create_role("admin")
    company_role = datastore.find_or_create_role("company")
    student_role = datastore.find_or_create_role("student")


    if not datastore.find_user(email = "admin@gmail.com"):
        datastore.create_user(email = "admin@gmail.com", password = hash_password("pass"))


    if not datastore.find_user(email = "xyz@gmail.com"):
        datastore.create_user(email = "xyz@gmail.com", password = hash_password("pass"))


    if not datastore.find_user(email = "raj@gmail.com"):
        datastore.create_user(email = "raj@gmail.com", password = hash_password("pass"))

    
    try:
        db.session.commit() 
        print("Create successfully")

    except:
        db.session.rollback()
        print("Error while creating")

    admin01 = datastore.find_user(email = "admin@gmail.com")
    company01 = datastore.find_user(email = "xyz@gmail.com")
    student = datastore.find_user(email = "raj@gmail.com")

    admin_role = datastore.find_role("admin")
    company_role = datastore.find_role("company")
    student_role = datastore.find_role("student")

    datastore.add_role_to_user(admin01, admin_role)
    datastore.add_role_to_user(company01, company_role)
    datastore.add_role_to_user(student, student_role)


    try:
        db.session.commit()
        print("Added roles")

    except:
        db.session.rollback()
        print("Error adding roles")
