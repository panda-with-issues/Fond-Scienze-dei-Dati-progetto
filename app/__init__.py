import os
from flask import Flask

from . import database, auth

def create_app():
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  
  app.config.from_pyfile('config.py', silent=True)

  # ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  db = database.init_db(app)

  # a simple page that says hello
  @app.route('/hello')
  def hello():
    return 'Hello, World!'
  
  app.register_blueprint(auth.bp)
  
  return app