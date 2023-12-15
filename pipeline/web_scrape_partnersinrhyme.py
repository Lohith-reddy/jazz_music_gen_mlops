import asyncio
import re

from aiohttp import ClientSession
from bs4 import BeautifulSoup


async def download_midi(url, extracted_text):
    async with ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()
            file_path = midi_data_path + "/" + extracted_text + ".mid"
            with open(file_path, "wb") as file:
                file.write(content)
                print("Downloaded", file_path)


async def main(url):  # Pass the url as an argument
    async with ClientSession() as session:
        response = await session.get(url)
        soup = BeautifulSoup(await response.text(), "html.parser")

        collection_content = soup.find(class_="collection-content")
        href_list = [a["href"] for a in collection_content.find_all("a")]

        tasks = []
        for url in href_list:
            match = re.search(r"/(\w+)\.shtml", url)
            if match:
                extracted_text = match.group(1)
                download_link = "https://composerconnection.com/midi1/Jazz/" + extracted_text + ".mid"
                tasks.append(asyncio.create_task(download_midi(download_link, extracted_text=extracted_text)))

        downloaded_files = await asyncio.gather(*tasks)


if __name__ == "__main__":
    midi_data_path = "midi_data"
    url = "https://www.partnersinrhyme.com/midi/Jazz/index.shtml"
    loop = asyncio.get_event_loop()

    # Run the main function using the event loop
    loop.run_until_complete(main(url))
    # await main(url)  # Pass the url as an argument
