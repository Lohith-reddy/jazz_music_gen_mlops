import os
import requests
import pickle

def download_midi(url, session):
    url = "https://www.midis101.com" + url
    # Extract the filename from the URL
    filename = url.split("/")[-1] + ".mid"
    print(f"Downloading {url}")
    # Check if the file already exists in the directory
    if os.path.isfile(f"midi_data/{filename}"):
        print(f"Skipping {filename} (already exists)")
        return

    with session.get(url) as response:
        # Save the MIDI file to the "data" folder
        with open(f"midi_data/{filename}", "wb") as file:
            file.write(response.content)

        print(f"Downloaded {filename}")

def load_links_from_pickle():
    with open("pipeline/download_links.pkl", "rb") as file:
        download_links = pickle.load(file)
    return download_links

def main():
    # Load download links from the pickle file
    download_links = load_links_from_pickle()

    # Create the "data" folder if it doesn't exist
    if not os.path.exists("midi_data"):
        os.makedirs("midi_data")

    # Download MIDI files from the URLs in download_links
    with requests.Session() as session:
        for url in download_links:
            download_midi(url, session)

    print("MIDI files downloaded successfully.")

if __name__ == "__main__":
    main()
