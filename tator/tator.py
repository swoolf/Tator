# all the imports
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, make_response
from dataBase import *
from webfuncs import web_funcs
 
app = Flask(__name__) # create the application instance :)
app.register_blueprint(web_funcs)
#app.register_blueprint(dataBase_funcs)

app.config.from_object(__name__) # load config from this file , tator.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'tator.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('TATOR_SETTINGS', silent=True)

@app.cli.command('initdb')
def initdb_command():
        """Initializes the database."""
        init_db()
        print('Initialized the database.')
       
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
        