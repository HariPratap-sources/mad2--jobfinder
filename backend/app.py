from flask import Flask
from config import LocalDevelopmentConfig
from dotenv import load_dotenv
from resources import auth_bp, api_bp
from flask_cors import CORS
from celery_worker import make_celery
from extensions import cache, mail

celery = None


def create_app():


    app = Flask(__name__)
        
   
    # config
    
    app.config.from_object(LocalDevelopmentConfig)
    app.config["broker_url"] = "redis://localhost:6379/0"
    app.config["result_backend"] = "redis://localhost:6379/0"
    app.config["CACHE_TYPE"] = "RedisCache"
    app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/1"
    app.config["CELERY_TIMEZONE"] = "Asia/Kolkata"
    app.config["CELERY_ENABLE_UTC"] = False
    #Init cache here
    cache.init_app(app)

    mail.init_app(app)
    # Init celery after config

    global celery
    celery = make_celery(app)
    celery.conf.timezone = "Asia/Kolkata"
    celery.conf.enable_utc = False
    app.celery = celery

    # Import tasks AFTER celery init
    from tasks import reminders, reports, export


    # Connection for flask with flask-sqlalchemy
    from models import db, User, Role
    db.init_app(app)

    # Enable CORS
    CORS(app, origins= ["http://localhost:5173", "http://127.0.0.1:5173"])

    # flask_security stuff
    from flask_security.datastore import SQLAlchemyUserDatastore
    from extensions import security
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, datastore = datastore, )
    # register_blueprint = False
    app.datastore = datastore

    # register blueprint
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    # flask restful
    # api.init_app(app)
    
    # Celery beat schedule

    from celery.schedules import crontab

    celery.conf.beat_schedule = {
        "daily-reminder": {
            "task": "tasks.reminders.send_daily_reminders",
            "schedule": crontab(hour=19,minute= 50),
        },
        "monthly-report": {
            "task": "tasks.reports.generate_monthly_report",
            "schedule": crontab(day_of_month= 1, hour= 6, minute= 0),
        },
    }
 
    #Cache
    

    # for trial
    with app.app_context():
        db.create_all()
    return app



app = create_app()


if __name__ == "__main__":
    app.run()