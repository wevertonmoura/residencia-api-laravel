#!/usr/bin/env bash

# --- INÍCIO DA CORREÇÃO ---

# 1. Navega para a pasta do projeto Laravel
cd /var/www/app/src

# 2. Verifica se a pasta 'vendor' (bibliotecas) está em falta
#    Isto acontece porque o nosso docker-compose.yaml otimizado
#    cria um volume rápido (mas vazio) para esta pasta.
if [ ! -f "vendor/autoload.php" ]; then
    echo "Pasta 'vendor' não encontrada. A executar 'composer install'..."
    # 3. Instala as dependências do Laravel DENTRO do volume rápido
    #    (Isto corrige o erro 'Failed to fetch' e 'autoload.php')
    composer install --no-interaction --no-progress --no-suggest
else
    echo "Pasta 'vendor' encontrada. A ignorar 'composer install'."
fi

# 4. Define as permissões corretas para o servidor web (www-data)
#    Isto corrige os erros de "tela branca" (Erro 500)
echo "A aplicar permissões para 'storage' e 'bootstrap/cache'..."
chown -R www-data:www-data storage bootstrap/cache
chmod -R 775 storage
chmod -R 775 bootstrap/cache

# 5. Limpa/Cria o cache de configuração (para garantir que o cors.php é lido)
echo "A criar o cache de configuração do Laravel..."
php artisan config:cache

# --- FIM DA CORREÇÃO ---


# 6. Comandos originais para iniciar os serviços
echo "Iniciando Nginx..."
service nginx start

echo "Iniciando PHP-FPM..."
php-fpm