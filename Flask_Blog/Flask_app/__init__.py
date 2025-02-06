from flask import Flask  
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from Flask_app.config import Config




db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

mail = Mail()


def create_app(config_class=Config):
   
   app = Flask(__name__,template_folder='templates',static_folder='static')
   app.config.from_object(Config)
   db.init_app(app)
   app.app_context().push()
   bcrypt.init_app(app)
   login_manager.init_app(app)
   mail.init_app(app)

   from Flask_app.users.routes import users
   from Flask_app.posts.routes import posts
   from Flask_app.main.routes import main
   from Flask_app.errors.handlers import errors

   app.register_blueprint(users)
   app.register_blueprint(posts)
   app.register_blueprint(main)
   app.register_blueprint(errors)
   return app