FROM php:8.3-cli

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    libpq-dev \
    libonig-dev \
    libxml2-dev \
    && docker-php-ext-install pdo pdo_mysql mbstring \
    && apt-get clean

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html

COPY . .

RUN mkdir -p bootstrap/cache storage/logs storage/framework/cache \
    storage/framework/sessions storage/framework/views \
    && chmod -R 775 bootstrap/cache storage

RUN composer install --no-dev --optimize-autoloader

EXPOSE 8000

CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=8000"]