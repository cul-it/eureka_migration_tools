#!/usr/bin/env python3
import json
import os
from dotenv import load_dotenv
load_dotenv()
import csv

okapiPath_JSON = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_OKAPI_PERMISSIONS")}.json"
okapiRefPath_JSON = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_REF_OKAPI_PERMISSIONS")}.json"
eurekaCapSetsPath_JSON = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_EUREKA_CAPABILITY_SETS")}.json"
eurekaCapPath_JSON = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_EUREKA_CAPABILITIES")}.json"
output_JSON = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_COMPARED_CURRENT_TO_CAPABILITIES")}.json"
output_CSV = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_COMPARED_CURRENT_TO_CAPABILITIES")}.csv"

def compare_current_permissions():
    print(okapiPath_JSON)
    # Pull the JSON file containing the Eureka Capability Sets and ingest it as JSON.
    if os.path.isfile(okapiPath_JSON):  # Check if the file exists
        with open(okapiPath_JSON, 'r') as f:
            okapi = json.load(f)
        print(f'Reference file loaded: {okapiPath_JSON}')
    else:
        print(f'Error: JSON file not found. {okapiPath_JSON}')

    # Pull the JSON file containing the Eureka Capability Sets and ingest it as JSON.
    if os.path.isfile(okapiRefPath_JSON):  # Check if the file exists
        with open(okapiRefPath_JSON, 'r') as f:
            refSets = json.load(f)
        print(f'Reference file loaded: {okapiRefPath_JSON}')
    else:
        print(f'Error: JSON file not found. {okapiRefPath_JSON}')

    # Pull the JSON file containing the Eureka Capabilities and ingest it as JSON.
    if os.path.isfile(eurekaCapPath_JSON):  # Check if the file exists
        with open(eurekaCapPath_JSON, 'r') as f:
            eurekaCap = json.load(f)
        print(f'Reference file loaded: {eurekaCapPath_JSON}')
    else:
        print(f'Error: JSON file not found. {eurekaCapPath_JSON}')

    def _get_capability_data(sub):
        # this function thats the provided sub-permission (OKAPI) and matches it to a Eureka Capability
        rtnData = {"id":'', "name":"","description":"","type":"","action":"","resource":""}
        for p in eurekaCap['capabilities']:
            if p['permission'] == sub:
                rtnData = p    
        return rtnData
    
    def _get_permission_data(sub):
        # this function takes the provided sub permission and retries its details
        rtnData = {"displayName":"","description":""}
        for p in okapi['permissions']:
            if p['permissionName'] == sub:
                rtnData = p
        return rtnData
        
    def _build_sub_permissions(subData):
        rtnData = []
        total = 0
        missing = 0
        allEurekaPermissions = []
        for sub in subData:
            r = _get_capability_data(sub)
            c = _get_permission_data(sub)
            total += 1
            missing = missing + 1 if r["id"] == "" else missing
            rtnData.append({
                "subPermission": sub,
                "subPermissionDisplayName": c['displayName'] if 'displayName' in c else '',
                "subPermissionDescription": c['description'] if 'description' in c else '',
                "eurekaId": r["id"],
                "eurekaName": r["name"],
                "eurekaDescription": r['description'] if 'description' in r else '',
                "eurekaType": r["type"],
                "eurekaAction": r["action"],
                "eurekaResource": r["resource"]
            })
            if r["id"] != "":
                allEurekaPermissions.append(r["id"])
        return {"subPermissions": rtnData, "total": total, "missing": missing, "allEurekaPermissions": allEurekaPermissions}


    finalData = []
    print("------ Starting Comparison -----")
    for i in refSets:
        x = False
        subData = _build_sub_permissions(i['allSubPermissions'])
        finalData.append({
                "displayName": i['displayName'],
                "id": i['id'],
                "total": subData['total'],
                "missing": subData['missing'],
                "subPermissions": subData['subPermissions'],
                "allEurekaPermissions": subData['allEurekaPermissions']
        })
        

    with open(output_JSON, 'w') as f:
            json.dump(finalData, f, indent=4)  # Save with indentation for readability
    print(f"Saved Comparison JSON file {output_JSON}")

    flattened_data = []
    test = ''
    for m in finalData:
        x = False
        for f in m['subPermissions']:
            if x == False:
                insertName = m['displayName'] 
                insertTotal = m['total'] 
                insertMissing = m['missing'] 
                x = True
            else:
                insertName = '' 
                insertTotal = ''
                insertMissing = '' 

            flattened_data.append([
                    insertName, insertTotal, insertMissing,
                    f['subPermission'], f['subPermissionDisplayName'], f['subPermissionDescription'], 
                    f['eurekaId'], f['eurekaName'], f['eurekaDescription'], f['eurekaType'], f['eurekaAction'], f['eurekaResource']
                ])
            
    # Write to CSV
    with open(output_CSV, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'displayName', 'total', 'missing',
            'subPermission', 'subPermissionDisplayName', 'subPermissionDescription', 
            'eurekaId', 'eurekaName', 'eurekaDescription', 'eurekaType', 'eurekaAction', 'eurekaResource'
        ])
        writer.writerows(flattened_data)
    print(f"Saved Comparison CSV file {output_CSV}")

compare_current_permissions()
print("------ Complete -----")