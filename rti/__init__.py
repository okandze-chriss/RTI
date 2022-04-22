from email import errors

import babel
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_dropzone import Dropzone
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from rti.config import Config

db = SQLAlchemy(session_options={"autoflush": False})
bcrypt = Bcrypt()
loginManager = LoginManager()
loginManager.login_view = 'security.login'
loginManager.login_message_category = 'info'
mail = Mail()

dropzone = Dropzone()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    loginManager.init_app(app)
    mail.init_app(app)
    dropzone.init_app(app)

    from rti.security.routes import security
    from rti.dashboard.routes import dashboard
    # from rti.impression.routes import impression
    from rti.errors.handlers import errors

    app.register_blueprint(security)
    app.register_blueprint(dashboard)
    # app.register_blueprint(impression)
    app.register_blueprint(errors)

    @app.template_filter()
    def format_datetime(value, formatdate='medium'):
        if value is None:
            return '-'
        if formatdate == 'full':
            formatdate = "EEEE, d. MMMM y 'at' HH:mm"
        elif formatdate == 'medium':
            formatdate = "dd.MM.yyyy"
        elif formatdate == 'dateheure':
            formatdate = "yyyy-MM-dd HH:mm"
        elif formatdate == 'heure':
            formatdate = "HH:mm"
        elif formatdate == 'heureChat':
            formatdate = "HH:mm | dd/MM"
        elif formatdate == 'typedate':
            formatdate = "yyyy.MM.dd"
        elif formatdate == 'jour':
            formatdate = "dd"
        elif formatdate == 'mois':
            formatdate = "MM"
        elif formatdate == 'annee':
            formatdate = "yyyy"
        return babel.dates.format_datetime(value, formatdate)

    return app
