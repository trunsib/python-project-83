import os
import validators
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash

from page_analyzer.url_normalizer import normalize_url
from page_analyzer.parser import parse_metadata
from page_analyzer.db import (
    init_db, add_url, get_url_by_name, get_all_urls,
    get_url_by_id, get_checks_for_url, add_check
)

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/urls', methods=['POST'])
def add_new_url():
    raw_url = request.form.get('url', '').strip()
    if not raw_url:
        flash('URL не может быть пустым', 'danger')
        return render_template('index.html'), 422
    
    normalized = normalize_url(raw_url)
    
    existing = get_url_by_name(normalized)
    if existing:
        flash('Страница уже существует', 'info')
        return redirect(url_for('show_url', url_id=existing['id']))
    
    url_id = add_url(normalized)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_url', url_id=url_id))

@app.route('/urls')
def list_urls():
    urls = get_all_urls()
    return render_template('urls.html', urls=urls)

@app.route('/urls/<int:url_id>')
def show_url(url_id):
    url = get_url_by_id(url_id)
    if not url:
        return 'Страница не найдена', 404
    checks = get_checks_for_url(url_id)
    return render_template('url.html', url=url, checks=checks)

@app.route('/urls/<int:url_id>/checks', methods=['POST'])
def check_url(url_id):
    url = get_url_by_id(url_id)
    if not url:
        return 'Страница не найдена', 404
    
    try:
        response = requests.get(url['name'], timeout=10)
        response.raise_for_status()
        status_code = response.status_code
        h1, title, description = parse_metadata(response.text)
        add_check(url_id, status_code, title, description, h1)
        flash('Страница успешно проверена', 'success')
    except requests.RequestException:
        flash('Ошибка при проверке страницы', 'danger')
    
    return redirect(url_for('show_url', url_id=url_id))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
