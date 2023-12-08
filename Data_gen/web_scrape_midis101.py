import os
import asyncio
from bs4 import BeautifulSoup
import aiohttp

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
    hrefs = [td.find("a")["href"] for td in td_elements if td.find("a") and td.find("a")["href"] != 'javascript:;']

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

async def download_midi(url, session):
    url = "https://www.midis101.com" + url
    # Extract the filename from the URL
    filename = url.split("/")[-1]

    # Check if the file already exists in the directory
    if os.path.exists(f"midi_data/{filename}"):
        print(f"Skipping {filename} (already exists)")
        return

    async with session.get(url) as response:
        # Save the MIDI file to the "data" folder
        with open(f"midi_data/{filename}", "wb") as file:
            # Iterate over the response content asynchronously
            async for chunk in response.content.iter_any():
                file.write(chunk)

        print(f"Downloaded {filename}")

async def main():
    # Fetch and extract hrefs asynchronously for pages 1 to 21
    all_hrefs = []
    async with aiohttp.ClientSession() as session:
        tasks = [extract_hrefs(session, page) for page in range(1, 22)]
        all_hrefs_per_page = await asyncio.gather(*tasks)
        all_hrefs = [href for hrefs in all_hrefs_per_page for href in hrefs]

    # Create the "data" folder if it doesn't exist
    if not os.path.exists("midi_data"):
        os.makedirs("midi_data")

    # Create a queue to store hrefs
    href_queue = asyncio.Queue()

    # Enqueue URLs directly into the href_queue
    tasks = [fetch_download_hrefs(url, href_queue) for url in all_hrefs]
    await asyncio.gather(*tasks)

    # Create a list to store download tasks
    download_tasks = []

    # Download MIDI files from the URLs in href_queue
    async with aiohttp.ClientSession() as session:
        while not href_queue.empty():
            href = await href_queue.get()
            url = "https://www.midis101.com" + href
            download_tasks.append(download_midi(url, session))

    # Concurrently download MIDI files
    await asyncio.gather(*download_tasks)

    print("MIDI files downloaded successfully.")

await main()
