import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import re

url = "https://www.partnersinrhyme.com/midi/Jazz/index.shtml"

async def download_midi(url, extracted_text):
    async with ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()
            file_path = "midi_data/" + extracted_text + ".mid"
            with open(file_path, "wb") as file:
                file.write(content)
                print("Downloaded", file_path)


async def main(url):  # Pass the url as an argument
    async with ClientSession() as session:
        response = await session.get(url)
        soup = BeautifulSoup(await response.text(), 'html.parser')

        collection_content = soup.find(class_="collection-content")
        href_list = [a['href'] for a in collection_content.find_all('a')]

        tasks = []
        for url in href_list:
            match = re.search(r"/(\w+)\.shtml", url)
            if match:
                extracted_text = match.group(1)
                download_link = "https://composerconnection.com/midi1/Jazz/" + extracted_text + ".mid"
                tasks.append(asyncio.create_task(download_midi(download_link, extracted_text=extracted_text)))

        downloaded_files = await asyncio.gather(*tasks)

await main(url)  # Pass the url as an argument

