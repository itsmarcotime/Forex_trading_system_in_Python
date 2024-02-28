from bs4 import BeautifulSoup
import cloudscraper

def get_article(card):
    return dict(
        headline = card.get_text(),
        link = 'https://www.reuters.com' + card.get('href')
    )

def bloomberg_com():
    s = cloudscraper.create_scraper()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    resp = s.get("https://www.reuters.com/business/finance/", headers=headers)

    soup = BeautifulSoup(resp.content, 'html.parser')

    links = []

    cards = soup.select('[class^="media-story-card__hub__"]')
    for card in cards:
        ca = card.find('a', {'data-tested': 'Heading'})
        links.append(get_article(ca))
    return links

