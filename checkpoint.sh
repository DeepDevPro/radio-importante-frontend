#!/bin/bash

# Cores para mensagens
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
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

# Função para exibir mensagens de aviso
warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Função para criar um novo checkpoint
create_checkpoint() {
    local tag_name=$1
    local message=$2

    echo "🔖 Criando novo checkpoint: $tag_name"
    
    # Verificar se há alterações não commitadas
    if [[ $(git status -s) ]]; then
        read -p "Existem alterações não commitadas. Deseja fazer commit? (s/n): " choice
        if [[ $choice == "s" ]]; then
            git add .
            git commit -m "Checkpoint: $message" || error "Falha ao fazer commit"
            git push origin main || error "Falha ao fazer push"
            success "Alterações commitadas e enviadas com sucesso!"
        else
            error "Por favor, faça commit das alterações antes de criar um checkpoint"
        fi
    fi

    # Criar tag
    git tag -a "$tag_name" -m "$message" || error "Falha ao criar tag"
    git push origin "$tag_name" || error "Falha ao enviar tag"
    
    # Backup do Nginx
    ssh root@138.197.27.40 "cp /etc/nginx/sites-available/api /etc/nginx/sites-available/api.$tag_name" || error "Falha ao criar backup do Nginx"
    
    success "Checkpoint '$tag_name' criado com sucesso!"
}

# Função para restaurar um checkpoint
restore_checkpoint() {
    local tag_name=$1
    
    echo "⏮️  Restaurando para checkpoint: $tag_name"
    
    # Verificar se a tag existe
    if ! git tag | grep -q "^$tag_name\$"; then
        error "Tag '$tag_name' não encontrada"
    fi
    
    # Verificar se há alterações não salvas
    if [[ $(git status -s) ]]; then
        warning "Você tem alterações não salvas que serão perdidas!"
        read -p "Deseja continuar? (s/n): " choice
        if [[ $choice != "s" ]]; then
            error "Operação cancelada pelo usuário"
        fi
    fi
    
    # Restaurar código
    git checkout "$tag_name" || error "Falha ao restaurar código"
    
    # Restaurar Nginx
    ssh root@138.197.27.40 "cp /etc/nginx/sites-available/api.$tag_name /etc/nginx/sites-available/api && systemctl restart nginx" || error "Falha ao restaurar Nginx"
    
    # Reiniciar serviço backend
    ssh root@138.197.27.40 "systemctl restart radio-importante.service" || error "Falha ao reiniciar backend"
    
    success "Sistema restaurado para o checkpoint '$tag_name'!"
}

# Função para listar checkpoints
list_checkpoints() {
    echo "📋 Checkpoints disponíveis:"
    echo "----------------------------"
    git tag -n || error "Falha ao listar tags"
}

# Menu principal
case "$1" in
    "create")
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo "Uso: $0 create <tag_name> <message>"
            echo "Exemplo: $0 create v1.1-stable \"Login e upload funcionando\""
            exit 1
        fi
        create_checkpoint "$2" "$3"
        ;;
    "restore")
        if [ -z "$2" ]; then
            echo "Uso: $0 restore <tag_name>"
            echo "Exemplo: $0 restore v1.0-stable"
            exit 1
        fi
        restore_checkpoint "$2"
        ;;
    "list")
        list_checkpoints
        ;;
    *)
        echo "Uso: $0 <comando> [argumentos]"
        echo "Comandos:"
        echo "  create <tag_name> <message>  - Criar novo checkpoint"
        echo "  restore <tag_name>           - Restaurar para um checkpoint"
        echo "  list                         - Listar checkpoints disponíveis"
        echo ""
        echo "Exemplos:"
        echo "  $0 create v1.1-stable \"Login e upload funcionando\""
        echo "  $0 restore v1.0-stable"
        echo "  $0 list"
        ;;
esac 