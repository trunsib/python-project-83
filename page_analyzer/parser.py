from bs4 import BeautifulSoup


def truncate(text: str | None, limit: int = 60) -> str | None:
    if not text:
        return text

    text = " ".join(text.strip().split())

    if len(text) > limit:
        return text[:limit] + "..."

    return text


def parse_html(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    h1_tag = soup.find("h1")
    title_tag = soup.find("title")
    description_tag = soup.find("meta", attrs={"name": "description"})

    h1 = truncate(h1_tag.get_text(strip=True)) if h1_tag else None
    title = truncate(title_tag.get_text(strip=True)) if title_tag else None
    description = None

    if description_tag and description_tag.get("content"):
        description = truncate(description_tag.get("content").strip())

    return {
        "h1": h1,
        "title": title,
        "description": description,
    }
