import reprlib

from dotenv import load_dotenv
import json
import os
import requests
import datetime
from epic_mapping import epicMapping


class SessionManager:

    def __init__(self):
        self.session_headers = None
        self.session_account = None
        load_dotenv()
        self.username = os.environ.get("IG_USERNAME")
        self.password = os.environ.get("IG_PASSWORD")
        self.apiKey = os.environ.get("IG_API_KEY")
        self.CFD_account = os.environ.get("CFDACC")
        self.spread_account = os.environ.get("SPREADACC")
        self.live_session = False
        print("SESSION MANAGER INITIALISED: ENV variables= ", self.username, self.password, self.apiKey)

    def load_session_json(self):
        with open('sessiontokens.json', 'r') as f:
            self.session_headers = json.load(f)
        return

    def dump_session_json(self):
        with open('sessiontokens.json', 'w') as f:
            json.dump(self.session_headers, f)

    def what_account(self):
        MAP = {"Z4ZGAF": "CFD", "Z4ZGAG" : "SPREAD BET"}
        print("ACCOUNT USED ON THIS SESSION IS: ", self.session_account, MAP)
        return

    def create_live_session(self):
        if self.live_session == True:
            try:
                self.load_session_json()
                self.check_IG_session()
                print("ATTEMPTED CHECK IG SESSION")
            except:  # probably due to a black seesiontokens.json file
                self.login()

            if self.live_session == True:
                print("IG SESSION CHECKED: SESSION IS LIVE")
                return

        else:
            print("NO LIVE SESSION : LOGGING IN")
            self.login()
        return

    def check_IG_session(self):
        url = "https://demo-api.ig.com/gateway/deal/session"
        version = "1"

        r = self.API_call(method="GET", url=url, body={}, version=version)
        if r.status_code == 200:
            self.live_session == True
            print("CHECK IG SESSION: LIVE", r.content.decode('utf-8'), r.headers)
        else:
            print("CHECK IG SESSION: DEAD", r.content.decode('utf-8'))
            self.live_session == False
        return r

    def login(self):
        url = "https://demo-api.ig.com/gateway/deal/session"

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
            self.session_headers = headers
            self.session_headers["X-SECURITY-TOKEN"] = r.headers["X-SECURITY-TOKEN"]
            self.session_headers["CST"] = r.headers["CST"]
            self.dump_session_json()
            self.live_session = True
            self.session_account = json.loads(r.content.decode("utf-8"))['accountType']
            print("SUCCESSFUL LOGIN AND DUMP OF SESSION HEADERS: ", r.content.decode("utf-8"))

        else:
            print("ERROR ON LOGIN : ", r.status_code, r.content.decode("utf-8"))

        return

    def API_call(self, method, url, body, version):
        self.session_headers['Version'] = version
        r = requests.request(method=method, url=url, headers=self.session_headers, json=body)
        return r

    def change_account(self, account="CFD", to_default=True):
        """ Use 'CFD' or 'SPREAD' as string arg to account"""

        if account == "CFD":
            openacc = self.CFD_account
        else:
            openacc = self.spread_account

        if not self.live_session:
            self.create_live_session()

        url = "https://demo-api.ig.com/gateway/deal/session"
        version = "1"
        body = {"accountId": openacc,
                "defaultAccount": to_default
                }

        r = self.API_call('PUT', url=url, body=body, version=version)

        if r.status_code == 200:
            print("SUCCESSFUL ACCOUNT SWITCH ", r.status_code, r.content.decode("utf-8"), r.headers)
            self.session_headers["X-SECURITY-TOKEN"] = r.headers["X-SECURITY-TOKEN"]
            self.dump_session_json()
            self.session_account = openacc
        else:
            print("ERROR ON ACCOUNT SWITCH: ", r.status_code, r.content.decode("utf-8"))
        return

    def logout(self):
        url = "https://demo-api.ig.com/gateway/deal/session"
        version = "1"

        if not self.live_session:
            print("NO LIVE SESSION: WILL NOT CALL API TO LOG OUT")
            return

        r = self.API_call(method="DELETE", url=url, body={}, version=version)

        if r.status_code == 204:
            print("SUCCESSFUL LOGOUT ", r.content.decode("utf-8"))

        else:
            print("ERROR ON LOGOUT ATTEMPT: ", r.content.decode("utf-8"))
        return
