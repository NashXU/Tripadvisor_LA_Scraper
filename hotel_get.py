# Import Packages
import pandas as pd
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")
import requests
from bs4 import BeautifulSoup
import random
import logging
import http.client
http.client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}

# URL of the TripAdvisor page listing hotels in LA city
firstPage_url = "https://www.tripadvisor.com/Hotels-g32655-Los_Angeles_California-Hotels.html"
urls = [firstPage_url]+['https://www.tripadvisor.com/Hotels-g32655-oa'+str(i*30)+'-Los_Angeles_California-Hotels.html' for i in range(1,32)]

# Scraping Data
hotels,links = [],[]
for url in tqdm(urls):
    # Send a GET request to the URL and retrieve the HTML content
    response = requests.get(url, headers=headers)
    html_content = response.text
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Find all hotel names on the page
    hotel_tags = soup.select("div.listing_title > a")
    
    # Extract the hotel names from the tags
    hotels.extend([tag.text for tag in hotel_tags])
    links.extend(['https://www.tripadvisor.com/'+tag.get("href") for tag in hotel_tags])

# Random Select Data
data = pd.DataFrame(zip(hotels,links),columns=['hotels','links'])
data = data[data.hotels.str.contains('. ')] # exclude ads
data = data.drop_duplicates()
data = data.sample(frac=0.1, random_state=0) # random select
