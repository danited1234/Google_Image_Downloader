import requests
import shutil
from bs4 import BeautifulSoup

def get_and_download_images(query):
    words = query.split()

    # Check if there are at least 3 words
    if len(words) >= 2:
        # Insert plus sign between the second and third words
        words.insert(1, '+')
        # Join the words back into a single string
        query = ''.join(words)

    google_images = f'https://www.google.com/search?q={query}&tbm=isch'
    response = requests.get(google_images)
    source_code = BeautifulSoup(response.text,'html.parser')
    img_tags = source_code.find_all('img')
    image_urls = [fix_url(img['src']) for img in img_tags]
    download_images(image_urls,query)

    # Extract link texts
    a_tags = source_code.find_all('a', class_='TwVfHd')
    link_texts = [a.get_text(strip=True) for a in a_tags]

    for text in link_texts:
        new_query = f"{query}+{text}"
        google_images = f"https://www.google.com/search?q={new_query}&tbm=isch"
        response = requests.get(google_images)
        source_code = BeautifulSoup(response.text, 'html.parser')
        img_tags = source_code.find_all('img')
        image_urls = [fix_url(img['src']) for img in img_tags]
        download_images(image_urls,new_query)

def download_images(image_urls,query):
    for i, image_url in enumerate(image_urls):
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(f'image_{query}{i}.jpg', 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
            print(f"Image {query} {i} downloaded successfully")
        else:
            print(f"Failed to download image {i}")

def fix_url(url):
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'https://www.google.com' + url
    return url

if __name__=='__main__':
    query = input("Enter A Query: ")
    get_and_download_images(query)
