from app import celery, create_app
from models import Placement_Drive, Application
from datetime import datetime
from flask_mail import Message
from extensions import mail
from sqlalchemy import func
import os
import csv

app =create_app()

@celery.task
def generate_monthly_report():
    with app.app_context():

        print("Generating monthly report...")

        #Current month range
        now = datetime.now()
        start_date = datetime(now.year, now.month, 1)

        # total drives
        drives = Placement_Drive.query.filter(Placement_Drive.created_at >= start_date).count()

        # total applications

        applications = Application.query.filter(Application.created_at >= start_date).count()

        # total selected
        selected_student = Application.query.filter(Application.app_status == "selected", Application.created_at >= start_date).count()

        folder = "monthly_reports"
        os.makedirs(folder, exist_ok= True)

        filename = f"{folder}/report_{now.strftime('%Y_%m')}.csv"

        with open(filename, "w", newline = "", encoding = "utf-8") as file:

            writer = csv.writer(file)

            # Header
            writer.writerow(["Metric", "Value"])
            writer.writerow(["Total Drives", drives])
            writer.writerow(["Total Applied", applications])
            writer.writerow(["Total Selected", selected_student])

        # admin_email = "admin04@gmail.com"
        msg = Message(subject = "Monthly Placement Report", sender = "pratap.30m@gmail.com", recipients= ["haripratap04@gmail.com"], body = f"""

Monthly Placement Report
Month: {now.strftime('%B %Y')}
Please find attached monthly report.

""")
        #attach file
        with open(filename, "rb") as f:
            msg.attach(f"report_{now.strftime('%Y_%m')}.csv","text/csv", f.read())
        print("Before sending mail")


        mail.send(msg)
        print("After sending mail")

        # send to admin email
        print("Monthly report generated & sent")