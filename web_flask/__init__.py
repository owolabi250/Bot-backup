from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from web_flask.config import config
import models 

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = models.storage.view()

def create_app(config_name):
    from .main import Main as main_blueprint
    app = Flask(__name__)
    app.register_blueprint(main_blueprint)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    # attach routes and custom error pages here
    return app
