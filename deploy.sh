#!/bin/bash

# Cores para mensagens
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Função para exibir mensagens de sucesso
success() {
    echo -e "${GREEN}✔ $1${NC}"
}

# Função para exibir mensagens de erro
error() {
    echo -e "${RED}✘ $1${NC}"
    exit 1
}

echo "🚀 Iniciando processo de deploy..."

# Verificar se há alterações não commitadas
echo "📝 Verificando alterações..."
if [[ $(git status -s) ]]; then
    read -p "Existem alterações não commitadas. Deseja fazer commit? (s/n): " choice
    if [[ $choice == "s" ]]; then
        read -p "Digite a mensagem do commit: " commit_message
        git add .
        git commit -m "$commit_message" || error "Falha ao fazer commit"
        git push origin main || error "Falha ao fazer push"
        success "Alterações commitadas e enviadas com sucesso!"
    else
        error "Por favor, faça commit das alterações antes do deploy"
    fi
fi

# Build do frontend
echo "🛠️  Gerando build do frontend..."
npm run build || error "Falha ao gerar build do frontend"
success "Build do frontend concluído!"

# Deploy do frontend
echo "📤 Enviando arquivos do frontend para o servidor..."
rsync -avz --delete dist/ root@138.197.27.40:/var/www/radio-importante-frontend/ || error "Falha ao enviar frontend"
success "Frontend atualizado no servidor!"

# Deploy do backend
echo "📤 Enviando arquivos do backend para o servidor..."
rsync -avz --exclude '__pycache__' --exclude 'venv' backend/ root@138.197.27.40:/var/www/radio-importante-backend/ || error "Falha ao enviar backend"
success "Backend atualizado no servidor!"

# Reiniciar serviço
echo "🔄 Reiniciando serviço no servidor..."
ssh root@138.197.27.40 'systemctl restart radio-importante.service' || error "Falha ao reiniciar serviço"
success "Serviço reiniciado com sucesso!"

echo "✨ Deploy concluído com sucesso! ✨" 