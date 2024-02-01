from bs4 import BeautifulSoup
import pandas as pd
import requests

def dailyfx_com():
    resp = requests.get('https://www.dailyfx.com/sentiment')

    # print(resp.content)
    # print(resp.status_code)

    soup = BeautifulSoup(resp.content, 'html.parser')
    # print(soup)

    rows = soup.select('.dfx-technicalSentimentCard')

    for r in rows:
        card = r.select_one('.dfx-technicalSentimentCard__pairAndSignal')
        print(card.select_one('a').get_text().replace('/', '_').strip(), end=' ')
        print(card.select_one('span').get_text(), end=' ')
        change_values = r.select('.dfx-technicalSentimentCard__changeValue')
        print(change_values[0].get_text())
        print(change_values[1].get_text())
        print(change_values[3].get_text())
        print(change_values[4].get_text())
        print()