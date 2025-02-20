#!/usr/bin/env python3
import json
import os
from dotenv import load_dotenv
load_dotenv()
import csv
import requests

def _okapi_login():
    url = f"{os.getenv('OKAPI_URL')}/authn/login-with-expiry"
    headers = {
        "X-Okapi-Tenant": os.getenv("OKAPI_TENANT"),
        "Content-Type":"application/json"
    }
    data = {
        "username": os.getenv("OKAPI_USER"),
        "password": os.getenv("OKAPI_PASSWORD"),
    }
    r = requests.post(url, json=data, headers=headers)
    r.raise_for_status()
    if r.status_code == 201:
        cookieData = {}
        for cookie in r.cookies:
            cookieData[cookie.name] = cookie.value
        return cookieData
    return None

def _get_permissions():
    cookieData = _okapi_login()
    url = f"{os.getenv('OKAPI_URL')}/perms/permissions?limit=10000000"
    r = requests.get(url, cookies={'folioAccessToken': cookieData['folioAccessToken']})
    jsonData = r.json()

    with open(os.getenv('FILE_OKAPI_PERMISSIONS'), 'w') as f:
            json.dump(jsonData, f, indent=4)  # Save with indentation for readability


_get_permissions()