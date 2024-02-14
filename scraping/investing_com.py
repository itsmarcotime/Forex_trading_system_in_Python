from bs4 import BeautifulSoup
import pandas as pd
import requests

data_keys = [
    'pair_name', 
    'ti_buy', 
    'ti_sell', 
    'ma_buy', 
    'ma_sell', 
    'S1', 
    'S2', 
    'S3', 
    'pivot', 
    'R1', 
    'R2', 
    'R3', 
    'percent_bullish', 
    'percent_bearish'
]

def get_data_object(text_list):
    data = {}
    for item in text_list:
        temp_item = item.split("=")
        if len(temp_item) == 2 and temp_item[0] in data_keys:
            data[temp_item[0]] = temp_item[1]

    if 'pair_name' in data:
        data['pair_name'] = data['pair_name'].replace("/", "_")

    return data

def investing_com():

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    params = dict(
        action = 'get_studies',
        pair_ID = 7,
        time_frame = 3600
    )

    resp = requests.get("https://www.investing.com/common/technical_studies/technical_studies_data.php", params=params, headers=headers)

    #print(resp.content)
    print(resp.status_code)

    text = resp.content.decode("utf-8")

    index_start = text.index("pair_name=")
    index_end = text.index("*;*quote_link")

    data_string = text[index_start:index_end]

    print(get_data_object(data_string.split('*;*')))