#!/usr/bin/env python3
import json
import os
from dotenv import load_dotenv
load_dotenv()
import csv

def combine_data():
    import json

    # Pull the JSON file containing the OKAPI permissions and ingest it as JSON.
    path1 = os.getenv("FILE_OKAPI_PERMISSIONS")
    if os.path.isfile(path1):  # Check if the file exists
        with open(path1, 'r') as f:
            okapi = json.load(f)
    else:
        print('Error: JSON file not found. ${path1}')

    # Pull the JSON file containing the Eureka Capability Sets and ingest it as JSON.
    path2 = os.getenv("FILE_EUREKA_CAPABILITY_SETS")
    if os.path.isfile(path2):  # Check if the file exists
        with open(path2, 'r') as f:
            eurekaSets = json.load(f)
    else:
        print('Error: JSON file not found. ${path2}')

    # Pull the JSON file containing the Eureka Capabilities and ingest it as JSON.
    path3 = os.getenv("FILE_EUREKA_CAPABILITIES")
    if os.path.isfile(path3):  # Check if the file exists
        with open(path3, 'r') as f:
            eurekaCap = json.load(f)
    else:
        print('Error: JSON file not found. ${path3}')

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
    with open(os.getenv('FILE_COMPARED_SETS_TO_PERMISSIONS'), 'w') as file:
        json.dump(eurekaSets, file, indent=4)

    return eurekaSets

def generateCsv():
    import json
    path1 = os.getenv("FILE_COMPARED_SETS_TO_PERMISSIONS")
    if os.path.isfile(path1):  # Check if the file exists
        with open(path1, 'r') as f:
            compared = json.load(f)
            
    else:
        print('Error: JSON file not found. ${path1}')


    flattened_data = []
    for c in compared['capabilitySets']:
        # Flatten the JSON data
        max_len = max(len(c['subCapabilities']), len(c['okapiSubPermissions']))
        for i in range(max_len):
            row = [
                c['id'],
                c['name'],
                c['type'],
                c['resource'],
                c['description'] if 'description' in c else '',
                c['action'],
                c['okapiDisplayName'] if 'okapiDisplayName' in c else ''
            ]
            
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
    with open(os.getenv('FILE_COMPARED_SETS_TO_PERMISSIONS_CSV'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'id', 'name', 'type', 'resource', 'description', 'action', 'okapiDisplayName',
            'subCapabilities.name', 'subCapabilities.type', 'subCapabilities.resource',
            'subCapabilities.description', 'subCapabilities.action',
            'okapiSubPermissions.name', 'okapiSubPermissions.description', 'okapiSubPermissions.permissionName'
        ])
        writer.writerows(flattened_data)

    print("CSV file created successfully.")

    
# Example paths to test the function
combine_data()
generateCsv()
print('processing complete')