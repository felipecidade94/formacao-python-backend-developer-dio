from flask import Flask

def create_app(test_config = None):
   app = Flask(__name__, instance_relative_config=True)
   app.config.from_mapping(
      SECRET_KEY = 'dev',
      DATABASE = 'diobank.db',
   )
   
   if test_config is None:
      app.config.from_pyfile('config.py', silent=True)
   else:
      app.config.from_mapping(test_config)
   
   from . import db_teste
   db_teste.init_app(app)
   
   # @app.route('/hello_world')
   # def hello_world():
   #    return '<h1>Hello, World!</h1>'
   
   return app