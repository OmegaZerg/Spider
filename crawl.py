from urllib.parse import urlparse
from bs4 import BeautifulSoup

def normalize_url(url: str) -> str:
    if url == "" or url == None:
        raise ValueError("The normalize url function must not be called with an empty string!")
    parsed_url = urlparse(url.lower())
    return parsed_url.hostname + parsed_url.path.rstrip("/") if parsed_url.hostname != None else parsed_url.path.rstrip("/")

def get_h1_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    if soup.h1 == None:
        return ""
    #print(f"Soup P: {soup.p}")
    #print(f"Soup P Contents: {soup.p.string}")
    #print(f"Soup h1: {soup.find('h1')}")
    #print(f"Soup h1 full: {soup.h1}")
    #print(f"Soup h1 contents: {soup.h1.string}")
    return soup.h1.get_text(strip=True) if soup.h1.string != None else ""

def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    paragraphs = soup.find_all('p')
    if len(paragraphs) < 1:
        return ""
    main_html = soup.find("main")
    if main_html is None:
        return paragraphs[0].get_text()
    return main_html.p.get_text(strip=True) if main_html.p.get_text() !="" else paragraphs[0].get_text()