from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

mail = Mail(app)

login = LoginManager(app)
login.login_view = 'login' # Specify what page to load for NON-authenticated Users
login.login_message = "You must login to make this change"
login.login_message_category = "danger"


from . import routes, models