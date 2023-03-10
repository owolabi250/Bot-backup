from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager
from web_flask.config import config
from datetime import timedelta
import models 

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = models.storage.view()
login_manager = LoginManager()

def create_app(config_name):
    from .main import Main as main_blueprint
    app = Flask(__name__)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)
    app.config['SECRET_KEY'] = 'the ragged priest'
    app.register_blueprint(main_blueprint)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'Main.login'
    login_manager.login_message_category = 'info'
    moment.init_app(app)
    # attach routes and custom error pages here
    return app
