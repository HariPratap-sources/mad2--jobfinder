import random
import uuid
from datetime import datetime, timedelta, timezone
from flask_security.utils import hash_password
from faker import Faker
from app import app

from models import db, User, Role, UserRoles, Student_Profile, Company_Profile, Placement_Drive, Application


fake = Faker("en_IN")


# --------------------------------------------------
# Utility: Random past datetime (for time series)
# --------------------------------------------------
# def random_past_datetime(months=12):
#     now = datetime.now(timezone.utc)
#     return now - timedelta(days=random.randint(0, 30 * months))


# --------------------------------------------------
# Main Seeder
# --------------------------------------------------
def seed_database():
    
    with app.app_context():
        print("Clearing old data... ")
        db.drop_all()     # Remove if you don’t want reset
        db.create_all()
   

        # -------------------------
        # Create Roles
        # -------------------------
        print("Seeding database...")
        roles= {"admin": Role(name="admin"), "company": Role(name="company"), "student": Role(name="student")}

        db.session.add_all(roles.values())
        db.session.commit()

        # -------------------------
        # Create Admin
        # -------------------------
        admin_user = User(
            email="admin04@gmail.com",
            password= hash_password("pass"),
            fs_uniquifier=str(uuid.uuid4()),
            active=True
        )
        

        db.session.add(admin_user)
        db.session.commit()

        db.session.add(UserRoles(user_id=admin_user.id, role_id=roles["admin"].id))
        db.session.commit()

        # -------------------------
        # Create 10 Companies
        # -------------------------
        print("👔 Creating company users...")
        indian_companies = [
            "Infosys", "TCS", "Wipro", "Zoho",
            "Freshworks", "HCL Technologies",
            "Tech Mahindra", "Razorpay",
            "Paytm", "Swiggy"
        ]

        companies = []

        for i in range(10):

            company_user = User(
                email=f"company{i+1}@example.com",
                password= hash_password("pass"),
                fs_uniquifier=str(uuid.uuid4()),
                active=True  
            )

            db.session.add(company_user)
            db.session.flush()

            db.session.add(UserRoles(user_id=company_user.id, role_id=roles["company"].id))

            company_profile = Company_Profile(
                company_name=indian_companies[i],
                Hr_contact=int(fake.msisdn()[:10]),
                description = fake.paragraph(),
                company_type = random.choice(["MNC", "startup", "Service", "Unicorn"]),
                company_field = random.choice(["Automobiles", "Software", "Finance", "Analyst"]),
                website=f"https://www.{indian_companies[i].lower().replace(' ', '')}.com",
                approval_status=random.choice(["approved", "pending"]),
                is_blacklisted=False,
                user_id=company_user.id  
            )

            db.session.add(company_profile)
            companies.append(company_user)

        db.session.commit()

        # -------------------------
        # 4️⃣ Create 50 Students
        # -------------------------
        print("🧑‍🤝‍🧑 Creating student users...")
        students = []

        qualifications = ["B.Tech", "M.Tech", "B.Sc", "MCA", "MBA"]
        departments = ["CSE", "IT", "ECE", "Mechanical", "Civil"]
        college_names = ["IITM", "IITB", "IITC", "IITBHU"]

        for i in range(50):

            student_user = User(
                email=fake.unique.email(),
                password= hash_password("student123"),
                fs_uniquifier=str(uuid.uuid4()),
                active=True  
            )

            db.session.add(student_user)
            db.session.flush()

            db.session.add(UserRoles(user_id=student_user.id, role_id=roles["student"].id))

            student_profile = Student_Profile(
                fullname=fake.name(),
                age =  random.randint(18, 60),
                gender=random.choice(["Male", "Female"]),
                qualification=random.choice(qualifications),
                department=random.choice(departments),
                college_name = random.choice(college_names),
                experience=random.randint(0, 3),
                contact_no=int(fake.msisdn()[:10]),
                skill=", ".join(fake.words(3)),
                resume="resume.pdf",
                is_blacklisted=False,
                is_active=True,
                user_id=student_user.id  
            )

            db.session.add(student_profile)
            students.append(student_user)

        db.session.commit()

        # -------------------------
        # 5️⃣ Create Placement Drives
        # -------------------------
        drives = []

        job_titles = [
            "Software Engineer",
            "Data Analyst",
            "Backend Developer",
            "ML Engineer",
            "QA Engineer"
        ]
        drive_names = [
            "Drive1", "Drive2", "Drive3", "Drive4", "Drive5"
        ]

        for company in companies:
            for _ in range(random.randint(2, 4)):

                drive = Placement_Drive(
                    drive_name = random.choice(drive_names), 
                    job_title=random.choice(job_titles),
                    job_desc=fake.paragraph(),
                    eligibility_criteria="Minimum 60% in academics",
                    salary=random.choice(["3LPA", "12LPA", "15k", "16k"]),
                    application_deadline=fake.date_between(
                        start_date="today",
                        end_date="+60d"
                    ),
                    status=random.choice(["approved", "pending"]),
                    drive_status = random.choice(["not_complete", "completed"]),
                    company_id=company.id
                )

                db.session.add(drive)
                drives.append(drive)

        db.session.commit()

        # -------------------------
        # 6️⃣ Create Applications
        # -------------------------
        for student in students:

            selected_drives = random.sample(
                drives,
                k=random.randint(1, 5)
            )

            for drive in selected_drives:
                application = Application(
                    student_id=student.id,
                    drive_id=drive.id,
                    app_status=random.choice(["applied", "shortlisted", "selected", "rejected"]) 
                )

                db.session.add(application)

        db.session.commit()

        print("Database seeded successfully.")


# --------------------------------------------------
# Run inside app context
# --------------------------------------------------
if __name__ == "__main__":
    seed_database()