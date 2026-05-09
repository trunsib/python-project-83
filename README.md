### Hexlet tests and linter status:
[![Actions Status](https://github.com/trunsib/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/trunsib/python-project-83/actions)

[![SonarQube Cloud](https://sonarcloud.io/images/project_badges/sonarcloud-light.svg)](https://sonarcloud.io/summary/new_code?id=trunsib_python-project-83)

Page Analyzer — это веб-приложение для анализа сайтов.  
Оно позволяет сохранять URL-адреса, выполнять проверки доступности сайтов и получать базовую SEO-информацию со страниц.

https://python-project-83-hb0c.onrender.com/

# Page Analyzer

Анализатор веб-страниц — сервис для проверки SEO-метаданных (заголовок и описание) указанных URL.

## Возможности

- Добавление URL для анализа
- Автоматическая нормализация URL
- Извлечение title и meta description
- Сохранение истории проверок
- Отображение всех проверенных страниц

## Технологии

- Python 3.12+
- Flask
- BeautifulSoup4
- Requests
- SQLite3
- uv (менеджер зависимостей)

## Установка и запуск

```bash
# Клонирование репозитория
git clone https://github.com/trunsib/python-project-83.git
cd python-project-83

# Установка зависимостей через uv
uv sync

# Инициализация базы данных (автоматически при первом запуске)
# Настройка переменных окружения
echo "SECRET_KEY=your-secret-key-here" > .env

# Запуск приложения
uv run flask --app page_analyzer.app run

# Или для разработки с автоперезагрузкой
uv run python -m page_analyzer.app