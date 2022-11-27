

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

    def market_nav(self):
        url = "https://demo-api.ig.com/gateway/deal/marketnavigation"
        version = "1"
        body = {}

        r = self.session_manager.API_call('GET', url=url, body=body, version=version)
        if r.status_code == 200:
            print("MARKET NAV CALL SUCCESS:  ", r.content.decode("utf-8"))
        else:
            print("ERROR MARKET NAV CALL:  ", r.status_code,  r.content.decode('utf-8'))

        return
