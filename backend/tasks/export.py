from celery_app import celery
from models import Application, Placement_Drive, Company_Profile
import pandas as pd
import os
import csv
from flask import jsonify

@celery.task
def export_applications(student_id):

    applications = Application.query.filter_by(student_id = student_id).all()

    folder = "exports"
    os.makedirs(folder, exist_ok= True)

    filename = f"{folder}/student_{student_id}.csv"

    with open(filename, "w", newline = "", encoding = "utf-8") as file:

        writer = csv.writer(file)

        # Header
        writer.writerow(["Student ID", "Company", "Drive", "Status", "Date"])

    # data = []
        for app in applications:
            writer.writerow([student_id, app.placement_drive.company_profile.company_name, app.placement_drive.drive_name, app.app_status, str(app.created_at)])

    return {"message": "CSV exported successfully",
                            "file": filename}