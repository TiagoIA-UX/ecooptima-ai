# Script PowerShell para inicializar repositório Git e fazer push inicial
# Substitua 'URL_DO_REPOSITORIO' pela URL do seu repositório no GitHub

cd $PSScriptRoot

git init

git add .

git commit -m "Initial commit EcoOptima AI"


# URL do repositório GitHub
git remote add origin https://github.com/TiagoIA-UX/ecooptima-ai.git

git branch -M main
git push -u origin main
