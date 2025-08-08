from flask import Flask, request, url_for

app = Flask(__name__)

@app.route('/olamundo')
def hello_world():
   # a = 3
   # nome
   return '<h1>Hello, world</h1>'

# @app.route('/bemvindo/<usuario>/<int:idade>/<float:altura>', methods=['POST','GET'])
# def wellcome(usuario, idade, altura):
#    if request.method == 'GET':
#       return f'<h1>Bem vindo, {usuario}. Você tem {idade} anos. Sua altura é {altura} m</h1>'
#    else:
#       return f'<h1>Tchau, {usuario}. Você tem {idade} anos. Sua altura é {altura} m</h1>'
   
@app.route('/bemvindo/<usuario>/<int:idade>/<float:altura>', methods=['POST','GET']) # Se retornar um dicionário, o flask converte para JSON.
def wellcome(usuario, idade, altura):
   return {'usuario': usuario,
         'idade': idade,
         'altura':altura,}

with app.test_request_context():
   print(url_for('hello_world'))
   print(url_for('wellcome', usuario='Felipe', idade=30, altura=1.79,))
   print(url_for('hello_world'))