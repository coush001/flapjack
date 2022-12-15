import json
import pandas as pd
import datetime
pd.set_option('display.max_columns', None)

class Admin:
    def __init__(self, session_manger):
        self.session_manager = session_manger

    def get_history(self):
        url = "https://demo-api.ig.com/gateway/deal/history/activity"
        version = "2"
        body = {}
        r = self.session_manager.API_call('GET', url=url, body=body, version=version)
        if r.status_code == 200:
            print("HISTORY CALL SUCCESS:  ", r.content.decode("utf-8"))
        else:
            print("ERROR GETTING HISTORY:  ", r.status_code,  r.content.decode('utf-8'))

    def market_nodes(self):
        """ Top level market node information"""
        url = "https://demo-api.ig.com/gateway/deal/marketnavigation"
        version = "1"
        body = {}

        r = self.session_manager.API_call('GET', url=url, body=body, version=version)
        if r.status_code == 200:
            print("MARKET NAV CALL SUCCESS:  ", r.content.decode("utf-8"))
        else:
            print("ERROR MARKET NAV CALL:  ", r.status_code,  r.content.decode('utf-8'))

        return

    def search_market(self, searchterm, instrumentType="SHARES", marketstatus="TRADEABLE", expiry=False):
        url = "https://demo-api.ig.com/gateway/deal/markets?searchTerm="+searchterm
        version = "1"
        body = {}

        r = self.session_manager.API_call('GET', url=url, body=body, version=version)

        if r.status_code == 200:
            markets = pd.DataFrame(json.loads(r.content.decode("utf-8"))["markets"])
            print("MARKET SEARCH SUCCESS:", markets)
        else:
            print("ERROR MARKET SEARCH CALL:  ", r.status_code,  r.content.decode('utf-8'))

        return markets.loc[(markets.instrumentType == instrumentType) & (markets.marketStatus == marketstatus)]


    def get_positions(self):
        url = "https://demo-api.ig.com/gateway/deal/positions"
        version = "2"
        body = {}
        r = self.session_manager.API_call("GET", url=url, body=body, version=version)
        if r.status_code == 200:
            print("POSITION CALL SUCCESS:  ")
            positions = json.loads(r.content.decode("utf-8"))['positions']
            for i in positions: print("   ", i)
        else:
            print("ERROR ON POSITION CALL:  ", r.status_code,  r.content.decode('utf-8'))

        return positions

    def get_transactions(self, maxSpanSeconds=720000):
        url = "https://demo-api.ig.com/gateway/deal/history/transactions"
        version = "2"
        body = {"maxSpanSeconds": str(maxSpanSeconds),
                "from": str(datetime.datetime.today() - datetime.timedelta(days=7))}
        r = self.session_manager.API_call("GET", url=url, body=body, version=version)
        if r.status_code == 200:
            print("TRANSACTION CALL SUCCESS:  ", r.content.decode("utf-8"))
            transactions = json.loads(r.content.decode("utf-8"))['transactions']
            for i in transactions: print("   ", i)
        else:
            print("ERROR ON TRANSACTION CALL:  ", r.status_code,  r.content.decode('utf-8'))

        return transactions