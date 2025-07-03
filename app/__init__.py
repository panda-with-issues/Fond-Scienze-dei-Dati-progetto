import os
from flask import Flask

from . import database

def create_app():
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_mapping(
    SECRET_KEY='dev',
    SQLALCHEMY_ECHO=True,
    SQLALCHEMY_DATABASE_URI='sqlite:///app.sqlite'
  )

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
  
  return app