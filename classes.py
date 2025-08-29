import aiohttp
import asyncio
import sys
from crawl import urlparse, normalize_url, get_html, extract_page_data, get_urls_from_html

class StatusError(Exception):
    pass
class HeaderError(Exception):
    pass

class AsyncCrawler():
    def __init__(self, 
                 base_url: str, 
                 base_domain: str, 
                 page_data: dict[str: str], 
                 lock: asyncio.Lock, 
                 max_concurrency: int, 
                 semaphore: asyncio.Semaphore, 
                 session: aiohttp.ClientSession):
        self.base_url = base_url
        self.base_domain = base_domain
        self.page_data = page_data
        self.lock = lock
        self.max_concurrency = max_concurrency
        self.semaphore = semaphore
        self.session = session
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url: str):
        async with self.lock:
            return normalized_url in self.page_data
        
    async def get_html(self, url: str):
        try:
            async with self.session.get(url) as resp:
                assert resp.status == 200
                return await resp.text
        except ConnectionError as ce:
            print(f"Connection error experienced when attempted to access '{url}'. Please try again. {ce}")
            sys.exit(1)
        except Exception as e:
            print(f"Unknown exception occured while attempting to access '{url}'. {e}")
            sys.exit(1)

    #TODO: Left off here
    async def crawl_page(base_url: str, current_url=None, page_data=None):
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