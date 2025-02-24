#!/usr/bin/env python3
import json
import os
from dotenv import load_dotenv
load_dotenv()
import csv

okapiPath_JSON = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_OKAPI_PERMISSIONS")}.json"
eurekaCapSetsPath_JSON = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_EUREKA_CAPABILITY_SETS")}.json"
eurekaCapPath_JSON = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_EUREKA_CAPABILITIES")}.json"
output_JSON = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_COMPARED_SETS_TO_PERMISSIONS")}.json"
output_CSV = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_COMPARED_SETS_TO_PERMISSIONS")}.csv"

def combine_data():
    import json

    # Pull the JSON file containing the OKAPI permissions and ingest it as JSON.
    if os.path.isfile(okapiPath_JSON):  # Check if the file exists
        with open(okapiPath_JSON, 'r') as f:
            okapi = json.load(f)
        print(f'Reference file loaded: {okapiPath_JSON}')
    else:
        print(f'Error: JSON file not found. {okapiPath_JSON}')

    # Pull the JSON file containing the Eureka Capability Sets and ingest it as JSON.
    if os.path.isfile(eurekaCapSetsPath_JSON):  # Check if the file exists
        with open(eurekaCapSetsPath_JSON, 'r') as f:
            eurekaSets = json.load(f)
        print(f'Reference file loaded: {eurekaCapSetsPath_JSON}')
    else:
        print(f'Error: JSON file not found. {eurekaCapSetsPath_JSON}')

    # Pull the JSON file containing the Eureka Capabilities and ingest it as JSON.
    if os.path.isfile(eurekaCapPath_JSON):  # Check if the file exists
        with open(eurekaCapPath_JSON, 'r') as f:
            eurekaCap = json.load(f)
        print(f'Reference file loaded: {eurekaCapPath_JSON}')
    else:
        print(f'Error: JSON file not found. {eurekaCapPath_JSON}')

    def getCapabilities(perms, compareJson):
        rtnData = []
        if perms:
            for p in perms:
                for r in compareJson:
                    if p == r['id']:
                        rtnData.append({
                            "id": r["id"],
                            "permission": r["permission"],
                            "name": r["name"],
                            "description": r['description'] if 'description' in r else '',
                            "type": r["type"],
                            "action": r["action"],
                            "resource": r["resource"]
                        })
        return rtnData
    
    def getPermissions(perms, compareJson):
        rtnData = []
        if perms:
            for p in perms:
                for r in compareJson:
                    if p == r['permissionName']:
                        rtnData.append({
                            "id": r["id"],
                            "name":  r['displayName'] if 'displayName' in r else '',
                            "description": r['description'] if 'description' in r else '',
                            "permissionName": r['permissionName']
                        })
        return rtnData
    

    # Loop through all the capability sets and 
    print("------ Starting Comparison -----")
    for r in eurekaSets["capabilitySets"]:
        r["okapiName"] = ""
        r["okapiSubPermissions"] = []
        r["okapiId"] = ""
        r["subCapabilities"] = getCapabilities(r["capabilities"], eurekaCap["capabilities"])
        for o in okapi["permissions"]:
            if o["permissionName"] == r["permission"]:
                r["okapiName"] = o["permissionName"]
                r["okapiDisplayName"] = o['displayName'] if 'displayName' in o else ''
                r["okapiSubPermissions"] = getPermissions(o["subPermissions"], okapi['permissions'])
                r["okapiId"] = o["id"]
    with open(output_JSON, 'w') as file:
        json.dump(eurekaSets, file, indent=4)
    print(f"Saved Comparison JSON file {output_JSON}")

    return eurekaSets

def generateCsv():
    print("------ Starting conversion to CSV -----")
    import json
    if os.path.isfile(output_JSON):  # Check if the file exists
        with open(output_JSON, 'r') as f:
            compared = json.load(f)
        print(f'Reference file loaded: {output_JSON}')
            
    else:
        print(f'Error: JSON file not found. {output_JSON}')


    flattened_data = []
    for c in compared['capabilitySets']:
        # Flatten the JSON data
        max_len = max(len(c['subCapabilities']), len(c['okapiSubPermissions']))
        x = False
        for i in range(max_len):
            if x == False:
                row = [
                    c['id'],
                    c['name'],
                    c['type'],
                    c['resource'],
                    c['description'] if 'description' in c else '',
                    c['action'],
                    c['okapiDisplayName'] if 'okapiDisplayName' in c else ''
                ]
                x = True
            else:
                row= ['','','','','','','']

            if i < len(c['subCapabilities']):
                sub = c['subCapabilities'][i]
                row.extend([
                    sub['name'],
                    sub['type'],
                    sub['resource'],
                    sub['description'],
                    sub['action']
                ])
            else:
                row.extend([''] * 5)
            
            if i < len(c['okapiSubPermissions']):
                okapi = c['okapiSubPermissions'][i]
                row.extend([
                    okapi['name'],
                    okapi['description'],
                    okapi['permissionName']
                ])
            else:
                row.extend([''] * 3)
            
            flattened_data.append(row)

    # Write to CSV
    with open(output_CSV, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'id', 'name', 'type', 'resource', 'description', 'action', 'okapiDisplayName',
            'subCapabilities.name', 'subCapabilities.type', 'subCapabilities.resource',
            'subCapabilities.description', 'subCapabilities.action',
            'okapiSubPermissions.name', 'okapiSubPermissions.description', 'okapiSubPermissions.permissionName'
        ])
        writer.writerows(flattened_data)
    print(f"Saved Comparison CSV file {output_CSV}")

    
# Example paths to test the function
combine_data()
generateCsv()
print("------ Complete -----")