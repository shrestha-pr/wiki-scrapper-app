import random

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
}
MAX_SCRAPE_COUNT = 10

def scrape_wiki_article(url, scrape_count=0):
    response = requests.get(
        url=url, headers=HEADERS
    )

    soup = BeautifulSoup(response.content, "html.parser")

    title = soup.find(id="firstHeading")
    print(title.text)

    #Get all the links
    all_links = soup.find(id="bodyContent").find_all("a")
    random.shuffle(all_links)
    link_to_scrape = 0

    for link in all_links:
        # We are only interested in other wiki articles
        if not link['href'].startswith("/wiki/") or link['href'].find("gif") != -1 or link['href'].find("svg") != -1:
            continue

        # use this link to scrape
        link_to_scrape = link
        break

    # print(link_to_scrape['href'])
    try:
        if scrape_count < MAX_SCRAPE_COUNT:
            scrape_wiki_article("https://en.wikipedia.org" + link_to_scrape['href'], scrape_count+1)
    except Exception as e:
        print(f"An error occurred: {e},  {link_to_scrape}")

scrape_wiki_article(url="https://en.wikipedia.org/wiki/Web_scraping")
