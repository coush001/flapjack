import reprlib

from dotenv import load_dotenv
import json
import os
import requests
import datetime
from epic_mapping import epicMapping


class SessionManager:

    def __init__(self):
        load_dotenv()
        self.username = os.environ.get("IG_USERNAME")
        self.password = os.environ.get("IG_PASSWORD")
        self.apiKey = os.environ.get("IG_API_KEY")
        self.last_connected = False
        print("SESSION MANAGER INITIALISED: ENV variables= ", self.username, self.password, self.apiKey)

    def get_session(self):
        with open('sessiontokens.json', 'r') as f:
            headers = json.load(f)
        return headers

    def session_details(self):
        url = "https://demo-api.ig.com/gateway/deal/session"
        self.headers = self.get_session()
        version = "1"

        r = self.API_call(method="GET", url=url, body={}, version=version)
        if r.status_code == 200:
            print("SUCCESSS GETTING SESSION: ", r.content.decode('utf-8'))
        else:
            print("FAILED SESSION RETRIEVAL: ", r.content.decode('utf-8'))
        return r

    def login(self):
        url = "https://demo-api.ig.com/gateway/deal/session"

        if self.session_details().status_code == 200:
            print("SESSION ALREADY RUNNING")
            return

        else:
            headers = {
                "Content-Type": "application/json; charset=UTF-8",
                "Accept": "application/json; charset=UTF-8",
                "X-IG-API-KEY": self.apiKey,
                "Version": "2"
            }
            body = {
                "identifier": self.username,
                "password": self.password,
                "encryptedPassword": "null"
            }

            r = requests.post(url, headers=headers, json=body)

            if r.status_code == 200:
                self.X_SECURITY_TOKEN = r.headers["X-SECURITY-TOKEN"]
                self.CST = r.headers["CST"]
                self.last_connected = datetime.datetime.now()

                self.headers["X-SECURITY-TOKEN"] = self.X_SECURITY_TOKEN
                self.headers["CST"] = self.CST
                with open('sessiontokens.json', 'w') as f:
                    json.dump(self.headers, f)

                print("SUCCESSFUL LOGIN AND DUMP OF SESSION HEADERS: ", r.content.decode("utf-8"))

            else:
                print("ERROR ON LOGIN : ", r.status_code, r.content.decode("utf-8"))

        return

    def API_call(self, method, url, body, version):
        self.headers['Version'] = version
        r = requests.request(method=method, url=url, headers=self.headers, json=body)
        return r

    def logout(self):
        url = "https://demo-api.ig.com/gateway/deal/session"
        self.headers = self.get_session()
        version= "1"

        r = self.API_call(method="DELETE", url = url, body={}, version=version)

        if r.status_code == 204:
            print("SUCCESSSFUL LOGOUT ", r.content.decode("utf-8"))

        else:
            print("ERROR ON LOGOUT ATTEMPT: ", r.content.decode("utf-8"))

    def get_history(self):
        url = "https://demo-api.ig.com/gateway/deal/history/activity"
        version = "2"
        body = {}
        r = self.API_call('GET', url=url, body=body, version=version)
        if r.status_code == 200:
            print ("HISTORY CALL SUCCESS:  ", r.content.decode("utf-8"))
        else:
            print("ERROR GETTING HISTORY:  ",r.status_code,  r.content.decode('utf-8'))

    def market_nav(self):
        url = "https://demo-api.ig.com/gateway/deal/marketnavigation"
        version = "1"
        body = {

        }
        r = self.API_call('GET', url=url, body=body, version=version)
        if r.status_code == 200:
            print ("MARKET NAV CALL SUCCESS:  ", r.content.decode("utf-8"))
        else:
            print("ERROR MARKET NAV CALL:  ",r.status_code,  r.content.decode('utf-8'))
