#!/usr/bin/env python3
import json
import os
from dotenv import load_dotenv
load_dotenv()
import csv
import requests

output_JSON = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_REF_OKAPI_PERMISSIONS")}.json"

def _okapi_login():
    url = f"{os.getenv('REF_OKAPI_URL')}/authn/login-with-expiry"
    headers = {
        "X-Okapi-Tenant": os.getenv("REF_OKAPI_TENANT"),
        "Content-Type":"application/json"
    }
    data = {
        "username": os.getenv("REF_OKAPI_USER"),
        "password": os.getenv("REF_OKAPI_PASSWORD"),
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
    url = f"{os.getenv('REF_OKAPI_URL')}/perms/permissions?limit=10000000"
    r = requests.get(url, cookies={'folioAccessToken': cookieData['folioAccessToken']})
    jsonData = r.json()
    
    def _get_permissions(perms, compareJson):
        rtnData = []
        if perms:
            for p in perms:
                for r in compareJson:
                    if p == r['permissionName']:
                        rtnData.append({
                            "id": r["id"],
                            "name":  r['displayName'] if 'displayName' in r else '',
                            "description": r['description'] if 'description' in r else '',
                            "permissionName": r['permissionName'],
                            "subPermissions": r['subPermissions'],
                            "mutable": r['mutable'],
                            "visible": r['visible'],
                            "deprecated": r['deprecated']
                        })
        return rtnData

    writePermissions = []
    for o in jsonData['permissions']:
         if o['mutable'] == True:
            o['subPermissions'] = _get_permissions(o['subPermissions'],jsonData['permissions'])
            o['allSubPermissions'] = []
            for p in o['subPermissions']:
                o['allSubPermissions'].extend(p['subPermissions'])

            writePermissions.append(o)

    with open(output_JSON, 'w') as f:
            json.dump(writePermissions, f, indent=4)  # Save with indentation for readability
    print(f"Saved OKAPI Permissions file {output_JSON}")


_get_permissions()
print("------ Complete -----")