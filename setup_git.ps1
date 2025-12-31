# Script PowerShell para inicializar repositório Git e fazer push inicial
# Substitua 'URL_DO_REPOSITORIO' pela URL do seu repositório no GitHub

cd $PSScriptRoot

git init

git add .

git commit -m "Initial commit EcoOptima AI"

# ATENÇÃO: Altere a linha abaixo para a URL do seu repositório no GitHub
# Exemplo: https://github.com/seuusuario/ecooptima-ai.git
git remote add origin URL_DO_REPOSITORIO

git branch -M main
git push -u origin main
