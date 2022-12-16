import uuid

class Trader:
    def __init__(self, session_manger):
        self.session_manager = session_manger

    def create_position(self, size, ccy, market, direction, uuid) -> object:
        url = "https://demo-api.ig.com/gateway/deal/positions/otc"
        version = "1"

        body = {
            "currencyCode": ccy,
            "dealReference": uuid,
            "direction": direction,
            "epic": market['epic'],
            "expiry": market['expiry'],
            "forceOpen": "false",
            "guaranteedStop": "false",
            "size": size,
            "orderType": "MARKET",
        }

        r = self.session_manager.API_call('POST', url=url, body=body, version=version)
        print("ATTEMPITNG ORDER: ", uuid)
        if r.status_code == 200:
            print("SUCCESS CREATING POSITION:  ", r.status_code, r.headers, r.content.decode('utf-8'))

        else:
            print("ERROR CREATING POSITION:  ",r.status_code,  r.content.decode('utf-8'))
            return

        return
