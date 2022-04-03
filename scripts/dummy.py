import pprint

import requests.auth

from config import USERNAME, PASSWORD

if __name__ == '__main__':
    auth = requests.auth.HTTPBasicAuth(USERNAME, PASSWORD)
    response = requests.get("http://127.0.0.1:5000/planning-center/get-confirmed-team-members", auth=auth)
    json = response.json()
    pprint.pprint(json)
