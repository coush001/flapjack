from eodhd import APIClient
from dotenv import load_dotenv
import os
import urllib, json

load_dotenv()

tok = os.environ.get("EODHDKEY")
# api = APIClient(tok)


url = f"https://eodhistoricaldata.com/api/eod/AAPL.US?api_token={tok}&order=d&fmt=json"

response = urllib.url(url)

data = json.loads(response.read())

print(data)
