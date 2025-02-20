#!/usr/bin/env python3
import json
import os
from dotenv import load_dotenv
load_dotenv()
import csv
import requests

def _okapi_login():
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

cookieData = _okapi_login()
def _get_capabilities():
    url = f"{os.getenv('EUREKA_URL')}/capability-sets?limit=10000000"
    r = requests.get(url, cookies={'folioAccessToken': cookieData['folioAccessToken']})
    jsonData = r.json()

    with open(os.getenv('FILE_EUREKA_CAPABILITIES'), 'w') as f:
            json.dump(jsonData, f, indent=4)  # Save with indentation for readability

def _get_capability_sets():
    cookieData = _okapi_login()
    url = f"{os.getenv('EUREKA_URL')}/capability?limit=10000000"
    r = requests.get(url, cookies={'folioAccessToken': cookieData['folioAccessToken']})
    jsonData = r.json()

    with open(os.getenv('FILE_EUREKA_CAPABILITY_SETS'), 'w') as f:
            json.dump(jsonData, f, indent=4)  # Save with indentation for readability

print(_okapi_login())
_get_capabilities()
_get_capability_sets()