#!/bin/bash

# Atualizar o sistema
apt update
apt upgrade -y

# Instalar nginx e outras dependências
apt install -y nginx certbot python3-certbot-nginx

# Configurar diretório da aplicação
mkdir -p /var/www/radio-importante
chown -R www-data:www-data /var/www/radio-importante

# Copiar arquivos da aplicação
cp -r dist/* /var/www/radio-importante/dist/

# Configurar nginx
cp nginx.conf /etc/nginx/sites-available/radio-importante
ln -s /etc/nginx/sites-available/radio-importante /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default

# Reiniciar nginx
systemctl restart nginx

echo "Deploy concluído! Agora você pode:"
echo "1. Configurar seu domínio para apontar para o IP do Droplet"
echo "2. Rodar: certbot --nginx -d seu-dominio.com" 