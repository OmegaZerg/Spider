import sys
import asyncio
from crawl import crawl_site_async

async def main():
    print("Hello from spider!")
    if len(sys.argv) < 4:
        print("Missing argument. Usage: python main.py <Website URL> <Maximum number of concurrent tasks> <Maximum number of pages to crawl>")
        sys.exit(1)
    if len(sys.argv) > 4:
        print("Too many arguments provided")
        sys.exit(1)

    base_url, max_concurrency, max_pages = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    if not base_url.startswith("https://") and not base_url.startswith("http://"):
        print("Website provided must start with either 'https://' or 'http://'. Please provide the full link.")
        sys.exit(1)
    if not sys.argv[2].isdigit():
        print("Max_concurrency must be an integer")
        sys.exit(1)
    if not sys.argv[3].isdigit():
        print("Max_pages must be an integer")
        sys.exit(1)
    
    print(f"Starting crawl of: {base_url}")

    # #Non-Async page crawler
    # page_data = crawl_page(sys.argv[1])
    # print(f"Pages Found: {len(page_data)}")
    # print(f"Spider Report for the url '{sys.argv[1]}':")
    # for url, data in page_data.items():
    #     print(f"{url}:")
    #     print(data)

    #Async Crawler:
    page_data = await crawl_site_async(base_url, max_concurrency, max_pages)
    for url, data in page_data.items():
        # print(f"Found {len(page['outgoing_links'])} outgoing links on {page['url']}")
        # print(f"Links: {page}")
        print(f"{url}:")
        print(data)


if __name__ == "__main__":
    asyncio.run(main())
