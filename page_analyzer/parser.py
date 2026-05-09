"""Парсинг HTML-страниц."""

from bs4 import BeautifulSoup

def parse_metadata(html_content):
    """
    Извлекает title и description из HTML.
    Returns: (title, description)
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    title = soup.title.string.strip() if soup.title else ''
    
    description_tag = soup.find('meta', attrs={'name': 'description'})
    description = description_tag.get('content', '').strip() if description_tag else ''
    
    return title, description
