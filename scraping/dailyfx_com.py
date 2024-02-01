from bs4 import BeautifulSoup
import pandas as pd
import requests

def dailyfx_com():
    resp = requests.get('https://www.dailyfx.com/sentiment')

    # print(resp.content)
    # print(resp.status_code)

    soup = BeautifulSoup(resp.content, 'html.parser')
    print(soup)