

class Trade:
    def __init__(self, session_manger):
        self.session_manager = session_manger

    def create_position(self, size, ccy, epic, direction):
        url = "https://demo-api.ig.com/gateway/deal/positions/otc"
        version = "1"

        body = {
            "epic": epic,
            "expiry": "-",
            "direction": direction,
            "size": size,
            "orderType": "MARKET",
            # "timeInForce": "null",
            # "level": "null",
            "guaranteedStop": "false",
            # "stopLevel": "null",
            # "stopDistance": "null",
            "trailingStop": "false",
            # "trailingStopIncrement": "null",
            "forceOpen": "false",
            # "limitLevel": "null",
            # "limitDistance": "null",
            # "quoteId": "null",
            "currencyCode": ccy
        }

        r = self.session_manager.API_call('POST', url=url, body=body, version=version)

        if r.status_code == 200:
            print("SUCCESS CREATING POSITION:  ", r.content.decode('utf-8'))

        else:
            print("ERROR CREATING POSITION:  ",r.status_code,  r.content.decode('utf-8'))
            return

        return
