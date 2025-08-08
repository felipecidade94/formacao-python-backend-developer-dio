# COMANDOS FLASK

**Rodar a aplicação**
flask --app src.app run --debug

**Cria o banco**
flask --app src.app init-db

**Criar arquivo de migração**
flask --app src.app db init

**Cria migração**
flask --app src.app db migrate -m "Criação inicial com role_id"

**Atualiza o banco**
flask --app src.app db upgrade
