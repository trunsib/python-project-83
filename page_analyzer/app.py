import os
from datetime import datetime
from urllib.parse import urlparse

import psycopg
import validators
import requests
from psycopg.rows import dict_row
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


def get_connection():
    return psycopg.connect(os.getenv('DATABASE_URL'), row_factory=dict_row)



@app.route('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def add_url():
    url = request.form.get('url')

    if not validators.url(url) or len(url) > 255:
        flash('Invalid URL', 'danger')
        return render_template('index.html'), 422

    parsed = urlparse(url)
    normalized_url = f'{parsed.scheme}://{parsed.netloc}'

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT id FROM urls WHERE name = %s',
                (normalized_url,)
            )
            existing = cur.fetchone()

            if existing:
                flash('URL already exists', 'info')
                return redirect(url_for('show_url', id=existing['id']))

            cur.execute(
                '''
                INSERT INTO urls (name, created_at)
                VALUES (%s, %s)
                RETURNING id
                ''',
                (normalized_url, datetime.utcnow())
            )
            url_id = cur.fetchone()['id']

    flash('URL added successfully', 'success')
    return redirect(url_for('show_url', id=url_id))


@app.get('/urls')
def urls():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                '''
                SELECT
                    urls.id,
                    urls.name,
                    urls.created_at,
                    MAX(url_checks.created_at) AS last_check,
                    (SELECT status_code 
                     FROM url_checks 
                     WHERE url_id = urls.id 
                     ORDER BY created_at DESC 
                     LIMIT 1) AS last_status
                FROM urls
                LEFT JOIN url_checks ON urls.id = url_checks.url_id
                GROUP BY urls.id
                ORDER BY urls.id DESC
                '''
            )
            urls = cur.fetchall()
    return render_template('urls.html', urls=urls)


@app.get('/urls/<int:id>')
def show_url(id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM urls WHERE id = %s', (id,))
            url = cur.fetchone()

            cur.execute(
                '''
                SELECT id, created_at, status_code, h1, title, description
                FROM url_checks
                WHERE url_id = %s
                ORDER BY id DESC
                ''',
                (id,)
            )
            checks = cur.fetchall()

    return render_template('url.html', url=url, checks=checks)


@app.post('/urls/<int:id>/checks')
def run_check(id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT name FROM urls WHERE id = %s', (id,))
            row = cur.fetchone()
            if not row:
                flash('URL не найден', 'danger')
                return redirect(url_for('urls'))
            url_to_check = row['name']

    try:
        response = requests.get(url_to_check, timeout=10)
        response.raise_for_status()
        status_code = response.status_code
    except (requests.RequestException, requests.Timeout):
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('show_url', id=id))

    soup = BeautifulSoup(response.text, 'html.parser')
    h1_tag = soup.find('h1')
    title_tag = soup.find('title')
    description_tag = soup.find('meta', attrs={'name': 'description'})

    h1_text = h1_tag.get_text(strip=True) if h1_tag else None
    title_text = title_tag.get_text(strip=True) if title_tag else None
    description_text = description_tag['content'].strip() if description_tag else None

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                '''
                INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ''',
                (id, status_code, h1_text, title_text, description_text, datetime.utcnow())
            )
            conn.commit()

    flash('Проверка успешно выполнена', 'success')
    return redirect(url_for('show_url', id=id))
