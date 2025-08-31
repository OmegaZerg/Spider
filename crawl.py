from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import aiohttp
import asyncio
from typing import Union
#Non-Async version dependancies:
# import requests
# import sys

class AsyncCrawler():
    def __init__(self, base_url: str,):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = 3
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url: str):
        async with self.lock:
            if normalized_url in self.page_data:
                return False
            else:
                return True
        
    async def get_html(self, url: str) -> Union[str, None]:
        try:
            async with self.session.get(url) as resp:
                assert resp.status == 200
                content_type = resp.headers.get('content-type', '')
                if 'text/html' not in content_type:
                    print(f"Excpected response content-type header to contain 'text/html' for url {url}, instead it contains '{content_type}'. This page will NOT be processed!")
                    return None
                return await resp.text()
        except ConnectionError as ce:
            print(f"Connection error experienced when attempting to access '{url}'. Please try again. {ce}")
            return None
        except Exception as e:
            print(f"Unknown exception occured while attempting to access '{url}'. {e}")
            return None

    async def crawl_page(self, current_url: str) -> None:
        if current_url == "" or current_url == None:
            raise ValueError("The crawl page method must not be called with an empty string for the current url parameter!")
        if urlparse(current_url).netloc != self.base_domain:
            return
        current_normalized = normalize_url(current_url)
        is_new = await self.add_page_visit(current_normalized)
        if not is_new:
            return
        async with self.semaphore:
            print(f"Crawling {current_url} \nActive: {self.max_concurrency - self.semaphore._value}")
            current_html = await self.get_html(current_url)
            if current_html is None:
                return
            current_data = extract_page_data(current_html, current_url)
            print(f"Current data: {current_data}")
            async with self.lock:
                self.page_data[current_normalized] = current_data
            page_urls = get_urls_from_html(current_html, self.base_url)
        background_tasks = set()
        for url in page_urls:
            task = asyncio.create_task(self.crawl_page(url))
            background_tasks.add(task)
        if len(background_tasks) > 0:
            await asyncio.gather(*background_tasks)
    
    async def crawl(self) -> dict[str: str]:
        await self.crawl_page(self.base_url)
        return self.page_data

def normalize_url(url: str) -> str:
    if url == "" or url == None:
        raise ValueError("The normalize url function must not be called with an empty string!")
    parsed_url = urlparse(url.lower())
    return parsed_url.hostname + parsed_url.path.rstrip("/") if parsed_url.hostname != None else parsed_url.path.rstrip("/")

def get_h1_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    if soup.h1 == None:
        return ""
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

#Non-Async page crawler
# def get_html(url: str) -> str:
#     try:
#         headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"}
#         session = requests.session()
#         session.get(url)
#         response = session.get(url, headers=headers)
#     except ConnectionError as ce:
#         print(f"Connection error experienced when attempted to access '{url}'. Please try again. {ce}")
#         sys.exit(1)
#     except Exception as e:
#         print(f"Unknown exception occured while attempting to access '{url}'. {e}")
#         sys.exit(1)
#     print(f"Status Code: {response.status_code}")
    
#     if response.status_code >= 400:
#         raise StatusError(f"Error response code of {response.status_code} was returned. Please try again.")
#     if not response.headers.get('content-type').startswith('text/html'):
#         print(f"Excpected response content-type header to contain 'text/html', instead it contains '{response.headers.get('content-type')}'. This page will NOT be processed!")
#         return '<html></html>'
#         #raise HeaderError(f"Excpected response content-type header to contain 'text/html', instead it contains '{response.headers.get('content-type')}'.")
#     return response.text

#Non-Async page crawler
# def crawl_page(base_url: str, current_url=None, page_data=None) -> dict[str: str]:
#     if base_url == "" or base_url == None:
#         raise ValueError("The crawl page function must not be called with an empty string for the base url parameter!")
#     if current_url is None:
#         current_url = base_url
#     if urlparse(base_url.lower()).hostname != urlparse(current_url.lower()).hostname:
#         return
#     if page_data is None:
#         page_data = {}
#     current_normalized = normalize_url(current_url)
#     if current_normalized in page_data:
#         return page_data
#     current_html = get_html(current_url)
#     current_data = extract_page_data(current_html, current_url)
#     page_data[current_normalized] = current_data
#     page_urls = get_urls_from_html(current_html, base_url)
#     for url in page_urls:
#         crawl_page(base_url, url, page_data)
#     return page_data

async def crawl_site_async(base_url: str):
    async with AsyncCrawler(base_url) as crawler:
        return await crawler.crawl()