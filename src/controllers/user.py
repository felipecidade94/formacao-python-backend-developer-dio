from flask import Blueprint, request
from src.app import User, db
from http import HTTPStatus
from sqlalchemy import inspect
from flask_jwt_extended import jwt_required
from src.utils import requires_role

app = Blueprint('user', __name__, url_prefix='/users')


# MÉTODOS OPERAÇÕES CRUD

# Método de criação (CREATE)
@jwt_required()
@requires_role('admin')
def _create_user():
   data = request.json
   user = User(username=data['username'],
               password=data['password'],
               role_id=data['role_id'],
               )
   db.session.add(user)
   db.session.commit()

# Método de leitura (READ)
@jwt_required()
@requires_role('admin')
def _list_users():
   query = db.select(User)
   users = db.session.execute(query).scalars()
   return [ {'id':user.id,
            'username':user.username, 
            'role': {'id': user.role.id, 
            'name': user.role.name,
            'active': user.active,
            },
            } for user in users
            ]

# Método de leitura (READ)
@app.route('/<int:user_id>')
@jwt_required()
@requires_role('admin')
def get_user_by_id(user_id):
   user = db.get_or_404(User, user_id)
   return {'id':user.id,'username':user.username}

# Método que chama o C ou o R do CRUD
@app.route('/', methods=['GET', 'POST'])
@jwt_required()
@requires_role('admin')
def list_or_create_user():
   
   if request.method == 'POST':
      _create_user()
      return {'message':'User created!'}, HTTPStatus.CREATED
   else:
      return {'users': _list_users()}

# Método de atualização (UPDATE)
@app.route('/<int:user_id>', methods=['PATCH'])
@jwt_required()
@requires_role('admin')
def update_user_by_id(user_id):
   user = db.get_or_404(User, user_id)
   data = request.json
   
   # PRECISA INFORMAR TODOS OS ATRIBUTOS (UMA CARALHADA DE IF ELIF ELSE)
   # if 'username' in data:
   #    user.username = data['username']
   #    db.session.commit()
   
   # MAPEIA TODOS OS ATRIBUTOS
   mapper = inspect(User)
   for column in mapper.attrs:
      if column.key in data:
         setattr(user, column.key, data[column.key])
   db.session.commit()
   
   return {'id':user.id,'username':user.username}

# Método de deleção (DELETE)
@app.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@requires_role('admin')
def detete_user_by_id(user_id):
   user = db.get_or_404(User, user_id)
   db.session.delete(user)
   db.session.commit()
   return '', HTTPStatus.NO_CONTENT