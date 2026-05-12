from page_analyzer.db import get_connection


def find_url_by_name(name: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT id FROM urls WHERE name = %s',
                (name,)
            )
            return cur.fetchone()


def insert_url(name: str, created_at):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                '''
                INSERT INTO urls (name, created_at)
                VALUES (%s, %s)
                RETURNING id
                ''',
                (name, created_at)
            )
            url_id = cur.fetchone()['id']
            conn.commit()
            return url_id


def get_urls():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                '''
                SELECT
                    urls.id,
                    urls.name,
                    urls.created_at,
                    (
                        SELECT status_code
                        FROM url_checks
                        WHERE url_id = urls.id
                        ORDER BY created_at DESC
                        LIMIT 1
                    ) AS last_status,
                    MAX(url_checks.created_at) AS last_check
                FROM urls
                LEFT JOIN url_checks
                    ON urls.id = url_checks.url_id
                GROUP BY urls.id
                ORDER BY urls.id DESC
                '''
            )
            return cur.fetchall()


def get_url_by_id(url_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT * FROM urls WHERE id = %s',
                (url_id,)
            )
            return cur.fetchone()


def get_url_checks(url_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                '''
                SELECT
                    id,
                    status_code,
                    h1,
                    title,
                    description,
                    created_at
                FROM url_checks
                WHERE url_id = %s
                ORDER BY id DESC
                ''',
                (url_id,)
            )
            return cur.fetchall()


def insert_check(url_id, status_code, h1, title, description, created_at):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                '''
                INSERT INTO url_checks
                (
                    url_id,
                    status_code,
                    h1,
                    title,
                    description,
                    created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ''',
                (url_id, status_code, h1, title, description, created_at)
            )
            conn.commit()