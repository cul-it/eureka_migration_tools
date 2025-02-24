#!/usr/bin/env python3
import json
import os
from dotenv import load_dotenv
load_dotenv()
import csv

okapiPath_JSON = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_OKAPI_PERMISSIONS")}.json"
okapiRefPath_JSON = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_REF_OKAPI_PERMISSIONS")}.json"
eurekaCapSets_JSON = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_EUREKA_CAPABILITY_SETS")}.json"
eurekaCaps_JSON = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_EUREKA_CAPABILITIES")}.json"
CurrentToCapabilities_JSON = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_COMPARED_CURRENT_TO_CAPABILITIES")}.json"
eurekaCapPath_JSON = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_EUREKA_CAPABILITIES")}.json"
output_JSON = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_FIND_MY_CAPABILITIES")}.json"
output_CSV = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_FIND_MY_CAPABILITIES")}.csv"

def find_possible_compatibility_sets():
    print("""Find Possible Capability Sets for User Permissions in Okapi""")
    # Pull the JSON file containing the Eureka Capability Sets and ingest it as JSON.
    if os.path.isfile(CurrentToCapabilities_JSON):  # Check if the file exists
        with open(CurrentToCapabilities_JSON, 'r') as f:
            curToCap = json.load(f)
        print(f'Reference file loaded: {CurrentToCapabilities_JSON}')
    else:
        print(f'Error: JSON file not found. {CurrentToCapabilities_JSON}')

    # Pull the JSON file containing the Eureka Capability Sets and ingest it as JSON.
    if os.path.isfile(eurekaCapSets_JSON):  # Check if the file exists
        with open(eurekaCapSets_JSON, 'r') as f:
            eurCapSet = json.load(f)
        print(f'Reference file loaded: {eurekaCapSets_JSON}')
    else:
        print(f'Error: JSON file not found. {eurekaCapSets_JSON}')

    # Pull the JSON file containing the Eureka Capabilities and ingest it as JSON.
    if os.path.isfile(eurekaCaps_JSON):  # Check if the file exists
        with open(eurekaCaps_JSON, 'r') as f:
            eurCaps = json.load(f)
        print(f'Reference file loaded: {eurekaCaps_JSON}')
    else:
        print(f'Error: JSON file not found. {eurekaCaps_JSON}')


    workingData = []
    for c in curToCap:
        for e in eurCapSet['capabilitySets']:
            common_items_count = len( set( e['capabilities'] ) & set( c['allEurekaPermissions'] ) )
            extra_items_in_cap_set = list(set(e['capabilities']) - set(c['allEurekaPermissions']))
            items_not_in_cap_set = list(set(c['allEurekaPermissions']) - set(e['capabilities']))
            ranking = round( (common_items_count / len(e['capabilities']) ), 3 )
            if ranking > .5 :
                workingData.append({
                    "permissionSetDisplayName": c['displayName'],
                    "totalPermissions": c['total'],
                    "totalCapInSet": len(e['capabilities']),
                    "capabilitiesInPermissionSet": common_items_count,
                    "ranking": ranking,
                    "eurekaId": e['id'],
                    "eurekaName": e['name'],
                    "eurekaType": e['type'],
                    "eurekaResource": e['resource'],
                    "eurekaDescription": e['description'] if 'description' in e else '',
                    "eurekaAction": e['action']
                })

    sorted_data = sorted(workingData, key=lambda x: (x['permissionSetDisplayName'], -x['ranking']))

    with open(output_JSON, 'w') as file:
        json.dump(sorted_data, file, indent=4)
    print(f"""
          Possible Capability Sets for User Permissions in Okapi has been Processed and saved to the local file system.
          file: {output_JSON}
                        ------ Script Complete -----
""")

    print("""Reformating into CSV format""")
    flattened_data = []
    test = ''
    for m in sorted_data:
        if test != m['permissionSetDisplayName']:
            permissionSetDisplayName = m['permissionSetDisplayName'] 
            totalPermissions = m['totalPermissions'] 
            test = m['permissionSetDisplayName']
        else:
            permissionSetDisplayName = '' 
            totalPermissions = ''

        flattened_data.append([
                permissionSetDisplayName, totalPermissions, 
                m['totalCapInSet'], m['capabilitiesInPermissionSet'], m['ranking'], 
                m['eurekaId'], m['eurekaName'], m['eurekaDescription'], m['eurekaType'], m['eurekaAction'], m['eurekaResource'],
                'n'
            ])
            
    # Write to CSV
    with open(output_CSV, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'permissionSetDisplayName', 'totalPermissions', 
            'totalCapInSet', 'capabilitiesInPermissionSet', 'ranking', 
            'eurekaId', 'eurekaName', 'eurekaDescription', 'eurekaType', 'eurekaAction', 'eurekaResource',
            'assign_yn'
        ])
        writer.writerows(flattened_data)
    print(f"""
          CSV file was processed and saved to the local file system.
          file: {output_CSV}
                        ------ Script Complete -----
""")

