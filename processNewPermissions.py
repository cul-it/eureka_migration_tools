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
findCapSets_CSV = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_FIND_MY_CAPABILITIES")}.csv"
output_JSON = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_NEW_ROLES")}.json"
output_CSV = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_NEW_ROLES")}.csv"
output_JSON2 = f"{os.getenv("BASE_DIR")}{os.getenv("NEW_ROLES")}_2.json"

def processCapSets():
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

    assignedCaps = []
    # Pull the CSV file containing the possible assigned Capability Sets and ingest it as JSON.
    if os.path.isfile(findCapSets_CSV):  # Check if the file exists
        with open(findCapSets_CSV, 'r') as f:
            csv_reader = csv.DictReader(f)
            name = ''
            total = ''
            for row in csv_reader:
                if row['permissionSetDisplayName'] != '':
                    name = row['permissionSetDisplayName']
                    total = row['totalPermissions']
                else:
                    row['permissionSetDisplayName'] = name
                    row['totalPermissions'] = total
                assignedCaps.append(row)
        print(f'Reference file loaded: {findCapSets_CSV}')
    else:
        print(f'Error: CSV file not found. {findCapSets_CSV}')

    def _get_eureka_capabilities(id):
        for e in eurCapSet['capabilitySets']:
            if e['id'] == id:
                return e['capabilities']
        return ''
    
    def _get_okapi_capabilities(name):
        for o in curToCap:
            if o['displayName'] == name:
                return o['allEurekaPermissions']
        return ''
    
    def _get_eureka_capability(id):
        for e in eurCaps['capabilities']:
            if e['id'] == id:
                return {
                    "id": e['id'],
                    "name": e['name'],
                    "type": e['type'],
                    "resource": e['resource'],
                    "description": e['description'] if 'description' in e else '',
                    "action": e['action'],
                }
        return {
            "id": id,
            "name": '',
            "type": '',
            "resource": '',
            "description": '',
            "action": '',
        }

    # remove all items that are not marked as yes
    wrkData = []
    for r in assignedCaps:
        if r['assign_yn'].lower() == 'y' or r['assign_yn'].lower() == 'yes':
            r['eurekaCapabilities'] = _get_eureka_capabilities(r['eurekaId'])
            wrkData.append(r)

    # process each line and find the capabilities assigned. 
    
    fullData = []
    roleName = ''
    tmpData = {}
    for r in wrkData:
        if roleName == r['permissionSetDisplayName']:
            tmpData['eurekaCapabilities'] = list(set(tmpData['eurekaCapabilities'] + r['eurekaCapabilities'] ))
        else:
            if len(tmpData) > 1:
                fullData.append(tmpData)
            roleName = r['permissionSetDisplayName']
            tmpData = {
                "permissionSetDisplayName": r['permissionSetDisplayName'],
                "totalPermissions": r['totalPermissions'],
                "missingCount": '',
                "extraCount": '',
                "eurekaCapabilities": r['eurekaCapabilities'],
                "okapiCapabilities": _get_okapi_capabilities(r['permissionSetDisplayName']),
                "missingList": [],
                "missingCapabilities": [],
                "extraList": [],
                "extraCapabilities": [],
                "suggestedAdditions": []
            }
    
    fullData.append(tmpData)

    # Get the missing count and list
    for f in fullData:
        difference = [item for item in f['okapiCapabilities'] if item not in f['eurekaCapabilities']]
        f['missingList'] = difference
        f['missingCount'] = len(difference)
        # get the information for the missing capabilities
        missingCapabilities = []
        for l in f['missingList']:
            missingCapabilities.append( _get_eureka_capability(l) )
        f['missingCapabilities'] = missingCapabilities

        # Process the extra items
        difference2 = [item for item in f['eurekaCapabilities'] if item not in f['okapiCapabilities']]
        f["extraCount"] = len(difference2)
        f["extraList"] = difference2
        # get the information for the extra capabilities
        extraCapabilities = []
        for l in f['extraList']:
            extraCapabilities.append( _get_eureka_capability(l) )
        f['extraCapabilities'] = extraCapabilities

        # generate more suggestions
        workingData = []
        for e in eurCapSet['capabilitySets']:
            common_items_count = len( set( e['capabilities'] ) & set( f['extraList'] ) )
            ranking = round( (common_items_count / len(e['capabilities']) ), 3 )
            if ranking > .3 :
                workingData.append({
                    "capabilitiesInPermissionSet": common_items_count,
                    "capabilitiesInSet": len(e['capabilities']),
                    "ranking": ranking,
                    "eurekaId": e['id'],
                    "eurekaName": e['name'],
                    "eurekaType": e['type'],
                    "eurekaResource": e['resource'],
                    "eurekaDescription": e['description'] if 'description' in e else '',
                    "eurekaAction": e['action']
                })
        f['suggestedAdditions'] = sorted(workingData, key=lambda x: ( -x['ranking']))
    

            


    with open(output_JSON2, 'w') as file:
        json.dump(fullData, file, indent=4)
    print(f"Saved Comparison JSON file {output_JSON2}")

processCapSets()