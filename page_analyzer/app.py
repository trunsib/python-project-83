import os
from datetime import datetime

import requests
import validators
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from page_analyzer.db import (
    find_url_by_name,
    get_url_by_id,
    get_url_checks,
    get_urls,
    insert_check,
    insert_url,
)
from page_analyzer.parser import parse_html
from page_analyzer.url_normalizer import normalize_url


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'dev'


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def add_url():
    url = request.form.get('url')

    if not validators.url(url) or len(url) > 255:
        flash('Некорректный URL', 'danger')
        return render_template('index.html'), 422

    normalized_url = normalize_url(url)

    existing = find_url_by_name(normalized_url)

    if existing:
        flash('Страница уже существует', 'info')
        return redirect(url_for('show_url', id=existing['id']))

    url_id = insert_url(normalized_url, datetime.utcnow())

    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_url', id=url_id))


@app.get('/urls')
def urls():
    urls_list = get_urls()
    return render_template('urls.html', urls=urls_list)


@app.get('/urls/<int:id>')
def show_url(id):
    url = get_url_by_id(id)

    if not url:
        flash('URL не найден', 'danger')
        return redirect(url_for('urls'))

    checks = get_url_checks(id)

    return render_template('url.html', url=url, checks=checks)


@app.post('/urls/<int:id>/checks')
def run_check(id):
    url_row = get_url_by_id(id)

    if not url_row:
        flash('URL не найден', 'danger')
        return redirect(url_for('urls'))

    url_to_check = url_row['name']

    try:
        response = requests.get(url_to_check, timeout=10)
        status_code = response.status_code

        if status_code >= 400:
            raise requests.RequestException()

        html = response.text

    except requests.RequestException:
        status_code = None
        html = ''

    parsed = parse_html(html)

    insert_check(
        id,
        status_code,
        parsed['h1'],
        parsed['title'],
        parsed['description'],
        datetime.utcnow(),
    )

    flash(
        'Произошла ошибка при проверке'
        if status_code is None
        else 'Страница успешно проверена',
        'danger' if status_code is None else 'success'
    )

    return redirect(url_for('show_url', id=id))


if __name__ == '__main__':
    app.run()
