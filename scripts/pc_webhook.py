import json
import os
import pprint

import dotenv
import requests.auth

dotenv.load_dotenv()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("data_file")

    args = parser.parse_args()

    auth = requests.auth.HTTPBasicAuth(os.getenv("USERNAME"), os.getenv("PASSWORD"))
    with open(args.data_file) as file:
        data = json.load(file)

    response = requests.post("http://127.0.0.1:5000/planning-center/plan-created", json=data, auth=auth)
    json_data = response.json()
    pprint.pprint(json_data)
