from bs4 import BeautifulSoup
import pandas as pd
import requests

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

    split_data_str = data_string.split('*;*')

    [print(x) for x in split_data_str]