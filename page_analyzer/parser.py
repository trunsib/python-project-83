"""Парсинг HTML-страниц."""

from bs4 import BeautifulSoup

def parse_metadata(html_content):
    """
    Извлекает h1, title и description из HTML.
    Returns: (h1, title, description)
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # H1
    h1_tag = soup.find('h1')
    h1 = h1_tag.get_text(strip=True) if h1_tag else ''
    
    # Title
    title = soup.title.string.strip() if soup.title else ''
    
    # Meta description
    description_tag = soup.find('meta', attrs={'name': 'description'})
    description = description_tag.get('content', '').strip() if description_tag else ''
    
    return h1, title, description
