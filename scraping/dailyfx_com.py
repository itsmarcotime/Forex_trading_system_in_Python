from bs4 import BeautifulSoup
import pandas as pd
import requests

def dailyfx_com():
    resp = requests.get('https://www.dailyfx.com/sentiment')

    soup = BeautifulSoup(resp.content, 'html.parser')

    rows = soup.select('.dfx-technicalSentimentCard')

    pair_data = []

    for r in rows:
        card = r.select_one('.dfx-technicalSentimentCard__pairAndSignal')
        change_values = r.select('.dfx-technicalSentimentCard__changeValue')
        pair_data.append(dict(
            pair = card.select_one('a').get_text().replace('/', '_'),
            sentiment = card.select_one('span').get_text(),
            longs_d = change_values[0].get_text(),
            shorts_d = change_values[1].get_text(),
            longs_w = change_values[3].get_text(),
            shorts_w = change_values[4].get_text(),
        ))

    return pd.DataFrame.from_dict(pair_data)
        