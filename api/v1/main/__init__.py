from flask import Blueprint
main_app = Blueprint('main_app', __name__, url_prefix='/api/v1/')
from api.v1.main.index import *
from api.v1.main.tasks import *
from api.v1.main.help import *
