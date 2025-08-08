from flask import Blueprint, request
from src.app import Post, db
from http import HTTPStatus
from sqlalchemy import inspect
from datetime import datetime
from zoneinfo import ZoneInfo

app = Blueprint('post', __name__, url_prefix='/posts')


# MÉTODOS OPERAÇÕES CRUD

# Método de criação (CREATE)
def _create_post():
   data = request.json
   # created = datetime.strptime(data['created'], '%Y-%m-%d %H:%M:%S')
   #post = Post(title=data['title'], body=data['body'], created=created, author_id=data['author_id'])
   post = Post(title=data['title'], body=data['body'], author_id=data['author_id'])
   db.session.add(post)
   db.session.commit()

# Método de leitura (READ)
def _list_posts():
   query = db.select(Post)
   posts = db.session.execute(query).scalars()
   return [serialize_post(post) for post in posts]

def serialize_post(post):
   return {
      'id': post.id,
      'title': post.title,
      'body': post.body,
      'created': post.created,
      'author_id': post.author_id
   }

# Método de leitura (READ) 
@app.route('/<int:post_id>')
@app.route('/<int:post_id>')
def get_post_by_id(post_id):
   post = db.get_or_404(Post, post_id)
   
   return {'id':post.id,'title':post.title, 'body':post.body, 'created':post.created, 'author_id': post.author_id}


###### SE EU QUISER RETORNAR COMO HORÁRIO DE BRASÍLIA!!
# def get_post_by_id(post_id):
#    post = db.get_or_404(Post, post_id)
#    created_brasilia = post.created.astimezone(ZoneInfo('America/Sao_Paulo'))
#    return {'id':post.id,'title':post.title, 'body':post.body, 'created':created_brasilia.isoformat(), 'author_id': post.author_id}

# def serialize_post(post):
#    return {
#       'id': post.id,
#       'title': post.title,
#       'body': post.body,
#       'created': post.created.astimezone(ZoneInfo('America/Sao_Paulo')).isoformat(),
#       'author_id': post.author_id
#    }

# Método que chama o C ou o R do CRUD
@app.route('/', methods=['GET', 'POST'])
def list_or_create_post():
   if request.method == 'POST':
      _create_post()
      return {'message':'Post created!'}, HTTPStatus.CREATED
   else:
      return {'posts': _list_posts()}

# Método de atualização (UPDATE)
@app.route('/<int:post_id>', methods=['PATCH'])
def update_post_by_id(post_id):
   user = db.get_or_404(Post, post_id)
   data = request.json
   
   # PRECISA INFORMAR TODOS OS ATRIBUTOS (UMA CARALHADA DE IF ELIF ELSE)
   # if 'username' in data:
   #    user.username = data['username']
   #    db.session.commit()
   
   # MAPEIA TODOS OS ATRIBUTOS
   mapper = inspect(Post)
   for column in mapper.attrs:
      if column.key in data:
         setattr(user, column.key, data[column.key])
   db.session.commit()
   
   return {'id':user.id,'username':user.username}

# Método de deleção (DELETE)
@app.route('/<int:post_id>', methods=['DELETE'])
def detete_post_by_id(post_id):
   post = db.get_or_404(Post, post_id)
   db.session.delete(post)
   db.session.commit()
   return '', HTTPStatus.NO_CONTENT