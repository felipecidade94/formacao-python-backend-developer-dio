import contextlib
from flask import Flask, current_app
from flask_migrate import Migrate
import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_jwt_extended import JWTManager
from datetime import datetime
import click
import os


class Base(DeclarativeBase):
   pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
jwt = JWTManager()
class Role(db.Model):
   id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
   name: Mapped[str] = mapped_column(sa.String, nullable=False)
   users: Mapped[list['User']] = relationship('User', back_populates='role')

   def __repr__(self) -> str:
      return f'Role(id={self.id!r}, name={self.name!r})'

class User(db.Model):
   id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
   username: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
   password: Mapped[str] = mapped_column(sa.String, nullable=False)
   role_id: Mapped[int] = mapped_column(sa.ForeignKey('role.id'), nullable=False)
   role: Mapped['Role'] = relationship(back_populates='users')
   active: Mapped['str'] = mapped_column(sa.String, nullable=True)
   posts: Mapped[list['Post']] = relationship('Post', back_populates='author')

   def __repr__(self) -> str:
      return f'User(id={self.id!r}, username={self.username!r})'

class Post(db.Model):
   id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
   title: Mapped[str] = mapped_column(sa.String, nullable=False)
   body: Mapped[str] = mapped_column(sa.Text, nullable=False)  # Melhor usar Text para posts
   created: Mapped[datetime] = mapped_column(sa.DateTime, server_default=sa.func.now(), nullable=False)
   author_id: Mapped[int] = mapped_column(sa.ForeignKey('user.id', name='fk_post_author_id'), nullable=False)
   author: Mapped['User'] = relationship('User', back_populates='posts')  # Novo relacionamento

   def __repr__(self) -> str:
      return f'Post(id={self.id!r}, title={self.title!r}, author_id={self.author_id!r})'

@click.command('init-db')
def init_db_command():
   global db
   with current_app.app_context():
      db.create_all()
   click.echo('Initialized the database')

def create_app(test_config = None):
   app = Flask(__name__, instance_relative_config=True)
   app.config.from_mapping(
      SECRET_KEY = 'dev',
      SQLALCHEMY_DATABASE_URI ='sqlite:///blog.db',
      JWT_SECRET_KEY = 'super-secret',
   )

   if test_config is None:
      app.config.from_pyfile('config.py', silent=True)
   else:
      app.config.from_mapping(test_config)

   with contextlib.suppress(OSError):
      os.makedirs(app.instance_path)
      
   app.cli.add_command(init_db_command)
   db.init_app(app)
   migrate.init_app(app, db)
   jwt.init_app(app)
   # @app.route('/hello_world')
   # def hello_world():
   #    return '<h1>Hello, World!</h1>'

   from src.controllers import post, user, auth, role

   app.register_blueprint(user.app)
   app.register_blueprint(post.app)
   app.register_blueprint(auth.app)
   app.register_blueprint(role.app)
   return app