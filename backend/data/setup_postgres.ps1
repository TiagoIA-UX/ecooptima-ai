# Script PowerShell para configurar banco PostgreSQL local
# 1. Cria o banco de dados ecooptima
# 2. Inicializa as tabelas do projeto

# Altere USUARIO e SENHA se necessário
$env:DATABASE_URL = "postgresql://postgres:postgres@localhost/ecooptima"

# Comando para criar o banco de dados (requer psql instalado e no PATH)
psql -U postgres -c "CREATE DATABASE ecooptima;"

# Instala dependências do backend
pip install -r ../requirements.txt

# Inicializa as tabelas
python ./init_db.py
