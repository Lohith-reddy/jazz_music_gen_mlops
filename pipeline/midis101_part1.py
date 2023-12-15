import asyncio
import pickle

import aiohttp
from bs4 import BeautifulSoup


async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()


async def extract_hrefs(session, page):
    base_url = "https://www.midis101.com/search/jazz"
    if page == 1:
        url = f"{base_url}"
    else:
        url = f"{base_url}/pg-{page}"

    html_content = await fetch_url(session, url)
    soup = BeautifulSoup(html_content, "html.parser")

    td_elements = soup.find_all("td")
    hrefs = [td.find("a")["href"] for td in td_elements if td.find("a") and td.find("a")["href"] != "javascript:;"]

    return hrefs


async def fetch_download_hrefs(url, queue):
    url = "https://www.midis101.com" + url
    async with aiohttp.ClientSession() as session:
        html_content = await fetch_url(session, url)
        soup = BeautifulSoup(html_content, "html.parser")

        elements = soup.find_all(class_="btn btn-primary btn-lg btn-block p-4")
        hrefs = [element["href"] for element in elements]

        for href in hrefs:
            print(f"Extracted {href}")
            await queue.put(href)

    return hrefs  # Return the extracted download links


async def save_links_to_pickle(download_links):
    with open("pipeline/download_links.pkl", "wb") as file:
        pickle.dump(download_links, file)


async def main():
    # Fetch and extract hrefs asynchronously for pages 1 to 21
    all_hrefs = []
    async with aiohttp.ClientSession() as session:
        tasks = [extract_hrefs(session, page) for page in range(1, 22)]
        all_hrefs_per_page = await asyncio.gather(*tasks)
        all_hrefs = [href for hrefs in all_hrefs_per_page for href in hrefs]

    # Create a queue to store hrefs
    href_queue = asyncio.Queue()

    # Enqueue URLs directly into the href_queue
    tasks = [fetch_download_hrefs(url, href_queue) for url in all_hrefs]
    download_links_per_page = await asyncio.gather(*tasks)
    download_links = [link for links in download_links_per_page for link in links]

    # Save download links to a pickle file
    await save_links_to_pickle(download_links)

    print("Download links extracted and saved to 'download_links.pkl' successfully.")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
