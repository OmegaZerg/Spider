import sys
import asyncio
from crawl import crawl_site_async

async def main():
    print("Hello from spider!")
    if len(sys.argv) < 2:
        print("No website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("Too many arguments provided")
        sys.exit(1)
    if not sys.argv[1].startswith("https://") and not sys.argv[1].startswith("http://"):
        print("Website provided must start with either 'https://' or 'http://'. Please provide the full link.")
        sys.exit(1)
    print(f"Starting crawl of: {sys.argv[1]}")

    # #Non-Async page crawler
    # page_data = crawl_page(sys.argv[1])
    # print(f"Pages Found: {len(page_data)}")
    # print(f"Spider Report for the url '{sys.argv[1]}':")
    # for url, data in page_data.items():
    #     print(f"{url}:")
    #     print(data)

    #Async Crawler:
    page_data = await crawl_site_async(sys.argv[1])
    for page in page_data.values():
        print(f"Found {len(page['outgoing_links'])} outgoing links on {page['url']}")
        print(f"Links: {page}")


if __name__ == "__main__":
    asyncio.run(main())
