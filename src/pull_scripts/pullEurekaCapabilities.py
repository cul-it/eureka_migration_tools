#!/usr/bin/env python3
import json
import os
from dotenv import load_dotenv
load_dotenv()
import requests


outputCap_JSON = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_EUREKA_CAPABILITIES")}.json"
outputCapSets_JSON = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_EUREKA_CAPABILITY_SETS")}.json"

def _login():
    url = f"{os.getenv('EUREKA_URL')}/authn/login-with-expiry"
    headers = {
        "X-Okapi-Tenant": os.getenv("EUREKA_TENANT"),
        "Content-Type":"application/json"
    }
    data = {
        "username": os.getenv("EUREKA_USER"),
        "password": os.getenv("EUREKA_PASSWORD"),
    }
    r = requests.post(url, json=data, headers=headers)
    r.raise_for_status()
    if r.status_code == 201:
        cookieData = {}
        for cookie in r.cookies:
            cookieData[cookie.name] = cookie.value
        return cookieData
    return None

cookieData = _login()
passCookie = {'folioAccessToken': cookieData['folioAccessToken']}
passHeader = {
        "X-Okapi-Tenant": os.getenv("EUREKA_TENANT"),
        "Content-Type":"application/json"
}
def get_capabilities():
    print("""Pulling EUREKA Capabilities Reference data""")
    url = f"{os.getenv('EUREKA_URL')}/capabilities?limit=10000000"
    r = requests.get(url, cookies=passCookie, headers=passHeader)
    jsonData = r.json()

    with open(outputCap_JSON, 'w') as f:
            json.dump(jsonData, f, indent=4)  # Save with indentation for readability
    print(f"""
          EUREKA Capabilities Reference data has been pulled and saved to the local file system.
          file: {outputCap_JSON}
                        ------ Script Complete -----
""")

def get_capability_sets():
    print("""Pulling EUREKA Capability Set Reference data""")
    url = f"{os.getenv('EUREKA_URL')}/capability-sets?limit=10000000"
    r = requests.get(url, cookies=passCookie, headers=passHeader)
    jsonData = r.json()

    with open(outputCapSets_JSON, 'w') as f:
            json.dump(jsonData, f, indent=4)  # Save with indentation for readability
    print(f"""
          EUREKA Capability Set Reference data has been pulled and saved to the local file system.
          file: {outputCapSets_JSON}
                        ------ Script Complete -----
""")
