from api.oanda_api import oanda_api


if __name__ == '__main__':
    api = oanda_api()

    data = api.get_account_summary()
    print(data)