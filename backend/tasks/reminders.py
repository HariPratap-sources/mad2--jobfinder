from app import celery, create_app
from models import Student_Profile, Placement_Drive
from datetime import datetime, timedelta
from flask_mail import Message
from extensions import mail
from sqlalchemy import func

app = create_app()
@celery.task
def send_daily_reminders():
    with app.app_context():
        print("task started")
        today = datetime.now().date()
        upcoming = today + timedelta(days=4)

        drives = Placement_Drive.query.filter(
            func.date(Placement_Drive.application_deadline) >= today,
            func.date(Placement_Drive.application_deadline) <= upcoming
        ).all()

        if not drives:
            print("No upcoming drives")
            return

        students = Student_Profile.query.all()
        print("students:", students)

        for student in students:
            drive_list = ""
            for drive in drives:
                drive_list += f"\n- {drive.drive_name} ({drive.job_title}) -Last Date: {drive.application_deadline}"

            msg = Message(subject = "Placement Drive Reminder", recipients= [student.user.email], body = f"""
                        
                        Hello {student.fullname},
                        You have upcoming placement drive deadlines:
                        {drive_list}
                        Apply soon!
                        Regards,
                        Placement cell JobFinder""")
        
            mail.send(msg)
                # send email logic
            print(f"Email sent to {student.user.email}")