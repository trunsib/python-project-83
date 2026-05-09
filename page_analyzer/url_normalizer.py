"""Нормализация URL."""

from urllib.parse import urlparse

def normalize_url(url):
    """
    Приводит URL к нормальной форме:
    https://example.com -> https://example.com
    http://example.com/path/ -> http://example.com/path
    """
    parsed = urlparse(url)
    normalized = f"{parsed.scheme}://{parsed.netloc}"
    if parsed.path and parsed.path != '/':
        normalized = f"{normalized}{parsed.path.rstrip('/')}"
    return normalized.lower()
