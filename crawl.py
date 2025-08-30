from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import requests
import aiohttp
import asyncio
from classes import StatusError, AsyncCrawler
import sys

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

def get_urls_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    links = []

    for link in soup.find_all('a'):
        if link.get('href') == "":
            continue
        if link.get('href').startswith("https://"):
            links.append(link.get('href'))
        else:
            links.append(urljoin(base_url, link.get('href')))
    return links

def get_images_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    images = []

    for image in soup.find_all('img'):
        if image.get('src') == "":
            continue
        if image.get('src').startswith("https://"):
            images.append(image.get('src'))
        else:
            images.append( base_url + image.get('src'))
    return images

def extract_page_data(html: str, page_url: str) -> dict[str: str]:
    if html == "" or page_url == "":
        raise ValueError("The extract page data function must not be called with an empty string!")
    page_data = {}
    page_data["url"] = page_url
    page_data["h1"] = get_h1_from_html(html)
    page_data["first_paragraph"] = get_first_paragraph_from_html(html)
    page_data["outgoing_links"] = get_urls_from_html(html, page_url)
    page_data["image_urls"] = get_images_from_html(html, page_url)
    return page_data

def get_html(url: str) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"}
        session = requests.session()
        session.get(url)
        response = session.get(url, headers=headers)
    except ConnectionError as ce:
        print(f"Connection error experienced when attempted to access '{url}'. Please try again. {ce}")
        sys.exit(1)
    except Exception as e:
        print(f"Unknown exception occured while attempting to access '{url}'. {e}")
        sys.exit(1)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code >= 400:
        raise StatusError(f"Error response code of {response.status_code} was returned. Please try again.")
    if not response.headers.get('content-type').startswith('text/html'):
        print(f"Excpected response content-type header to contain 'text/html', instead it contains '{response.headers.get('content-type')}'. This page will NOT be processed!")
        return '<html></html>'
        #raise HeaderError(f"Excpected response content-type header to contain 'text/html', instead it contains '{response.headers.get('content-type')}'.")
    return response.text

#Non-Async page crawler
def crawl_page(base_url: str, current_url=None, page_data=None) -> dict[str: str]:
    if base_url == "" or base_url == None:
        raise ValueError("The crawl page function must not be called with an empty string for the base url parameter!")
    if current_url is None:
        current_url = base_url
    if urlparse(base_url.lower()).hostname != urlparse(current_url.lower()).hostname:
        return
    if page_data is None:
        page_data = {}
    current_normalized = normalize_url(current_url)
    if current_normalized in page_data:
        return page_data
    current_html = get_html(current_url)
    current_data = extract_page_data(current_html, current_url)
    page_data[current_normalized] = current_data
    page_urls = get_urls_from_html(current_html, base_url)
    for url in page_urls:
        crawl_page(base_url, url, page_data)
    return page_data

async def crawl_site_async(base_url: str, base_domain: str, max_concurrency: int, page_data={}, lock=asyncio.Lock(), semaphore=asyncio.Semaphore, session=aiohttp.ClientSession()):
    crawler = AsyncCrawler()
    async with crawler:
        pass