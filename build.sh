#!/usr/bin/env bash
set -e

# Загружаем переменные окружения из .env
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Устанавливаем uv, если его нет
if ! command -v uv >/dev/null 2>&1; then
  echo "Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  source $HOME/.local/bin/env
fi

# Устанавливаем зависимости проекта через Makefile
echo "Installing project dependencies..."
make install

# Создаём базу данных и таблицы
if [ -f database.sql ]; then
  echo "Setting up database..."
  psql -a -d $DATABASE_URL -f database.sql
else
  echo "database.sql not found!"
fi

echo "Build complete!"
