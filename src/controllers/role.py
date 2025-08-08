from flask import Blueprint, request
from src.app import Role, db
from http import HTTPStatus
from flask_jwt_extended import jwt_required
from src.utils import requires_role

app = Blueprint('role', __name__, url_prefix='/roles')

@app.route('/', methods=['POST'])
@jwt_required()
@requires_role('admin')
def create_role():
   data = request.json
   role = Role(name = data['name'])
   db.session.add(role)
   db.session.commit()
   return {'message': 'Role created'}, HTTPStatus.CREATED