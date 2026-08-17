"""
Scrapes brand URL and collects relevant data like brand title, content from the website, and products/services
"""

import requests
from bs4 import BeautifulSoup

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

def scrape_brand_site(url: str, max_chars: int = 6000) -> dict:
    """Best-effort scrape of a brand's homepage."""
    
    result = {"url": url, "title": None, "meta_description": None, "text": "", "error": None}

    try:
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        if soup.title:
            result["title"] = soup.title.get_text(strip=True)

        meta = soup.find("meta", attrs={"name": "description"})
        if meta and meta.get("content"):
            result["meta_description"] = meta["content"].strip()

        for tag in soup(["script", "style", "noscript", "svg"]):
            tag.decompose()

        result["text"] = " ".join(soup.get_text(separator=" ").split())[:max_chars]

    except requests.RequestException as exc:
        result["error"] = f"Could not reach the brand URL: {exc}"

    return result

# Function to look for competitors on another search engine

def search_competitors(query: str, max_results: int = 5) -> list[dict]:
    """Lightweight, free competitor search — no API key needed. Currently weak but can be improved by using other API keys"""
    try:
        from ddgs import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return [{"title": r.get("title"), "href": r.get("href"), "body": r.get("body")} for r in results]
    except Exception:
        return []  # nice-to-have only, never blocks the pipeline