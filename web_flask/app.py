import os
from . import create_app
from flask_migrate import Migrate


"""
    This is the entry point of the application.
    It creates the application instance and runs it.
"""
app = create_app('default')
#migrate = Migrate(app, db)

@app.route('/test')
def make_shell_context():
    return dict(db=db)
