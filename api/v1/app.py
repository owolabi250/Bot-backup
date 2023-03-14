#!usr/bin/python3

from api.v1.main import main_app
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from flasgger import Swagger
from werkzeug.exceptions import HTTPException
import os
import models


app = Flask(__name__)
swagger = Swagger(app)

app.url_map.strict_slashes = False
cors = CORS(app, resources={r"/api/v1/*": {"origin": "*"}})

app.register_blueprint(main_app)
app.config['SECRET_KEY'] = "TheRaggedPriest"

host = os.getenv('HBNB_API_HOST', '127.0.0.1')
port = os.getenv('HBNB_API_PORT', '5000')


@app.teardown_appcontext
def teardown_db(exception):
    models.storage.close()


@app.errorhandler(400)
def handle_400(exception):
    """
        handles 400 errros, in the event that global error handler fails
    """
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)

@app.errorhandler(404)
def handle_404(exception):
    """
        handles 404 errors, in the event that global error handler fails
    """
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)

@app.errorhandler(Exception)
def global_error_handler(err):
    """
        Global Route to handle All Error Status Codes
    """
    if isinstance(err, HTTPException):
        if type(err).__name__ == 'NotFound':
            err.description = "Not found"
        message = {'error': err.description}
        code = err.code
    else:
        message = {'error': err}
        code = 500
    return make_response(jsonify(message), code)


def setup_global_errors():
    """
        This updates HTTPException Class with custom error function
    """
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, global_error_handler)



if __name__ == '__main__':
    """
      MAIN Flask App
    """
 # initializes global error handling
    setup_global_errors()
    # start Flask app
    app.run(host=host, port= port)

