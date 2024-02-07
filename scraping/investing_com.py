from bs4 import BeautifulSoup
import pandas as pd
import requests

def investing_com():

    headers = {
        "User-Agent": ""
    }

    params = dict(
        action = 'get_studies',
        pair_ID = 7,
        time_frame = 3600
    )

    resp = requests.get("https://www.investing.com/common/technical_studies/technical_studies_data.php", params=params, headers=headers)

    print(resp.content)
    print(resp.status_code)