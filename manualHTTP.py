from dotenv import load_dotenv, dotenv_values
import http.client

env = dotenv_values(".env")

print('AND HERES THE API KEY:   ', env.get('IGAPIKEY'))


conn = http.client.HTTPSConnection("demo-api.ig.com")

payload = "{ \n\"identifier\": \"coush001demo\", \n\"password\": \"igdemopasS5\" \n} "

headers = {
    'Content-Type': "application/json",
    'Accept': "application/json; charset=UTF-8",
    'VERSION': "2",
    'X-IG-API-KEY': "f19b42e6774160aec5a6ca652860861018fdf678"
    }

conn.request("POST", "/gateway/deal/session", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
print(res.headers)