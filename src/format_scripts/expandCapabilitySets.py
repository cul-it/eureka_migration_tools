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
output_JSON = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_EUREKA_CAPABILITY_SETS_EXPANDED")}.json"
output_CSV = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_EUREKA_CAPABILITY_SETS_EXPANDED")}.csv"
output_HTML = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_EUREKA_CAPABILITY_SETS_EXPANDED")}.html"

def expand_capability_sets():
    print("""Building Comparison Data - Expanding Capability Sets """)
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
        print(f'Error: JSON file not found. ${eurekaCapPath_JSON}')


    print("------ Processing Expansions -----")
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

    # Loop through all the capability sets and 
    for r in eurekaSets["capabilitySets"]:
        r["capabilities"] = getCapabilities(r["capabilities"], eurekaCap["capabilities"])
    with open(output_JSON, 'w') as file:
        json.dump(eurekaSets, file, indent=4)
    print(f"""
          Expanded Capability Sets has been processed and saved to the local file system.
          file: {output_JSON}
                        ------ Step Complete -----
    """)

    return eurekaSets

def generate_csv():
    print("------ Reformating to CSV -----")
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
        max_len = len(c['capabilities'])
        x = False
        for sub in c['capabilities']:
            if x == False:
                row = [
                    c['id'],
                    c['name'],
                    c['type'],
                    c['resource'],
                    c['description'] if 'description' in c else '',
                    c['action'],
                    sub['name'],
                    sub['type'],
                    sub['resource'],
                    sub['description'],
                    sub['action']
                ]   
                x = True
            else:
                row= ['','','','','','']
                row.extend([
                    sub['name'],
                    sub['type'],
                    sub['resource'],
                    sub['description'],
                    sub['action']
                ])
            flattened_data.append(row)

    # Write to CSV
    with open(output_CSV, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'id', 'name', 'type', 'resource', 'description', 'action', 
            'capabilities.name', 'capabilities.type', 'capabilities.resource',
            'capabilities.description', 'capabilities.action'
        ])
        writer.writerows(flattened_data)
    print(f"""
          Expanded Capability Sets has been processed and saved to the local file system.
          file: {output_CSV}
                        ------ Step Complete -----
    """)

def generate_wiki_page():
    print("------ Reformating to HTML / WIKI page -----")
    import json
    if os.path.isfile(output_JSON):  # Check if the file exists
        with open(output_JSON, 'r') as f:
            okapi = json.load(f)
        print(f'Reference file loaded: {output_JSON}')
            
    else:
        print(f'Error: JSON file not found. {output_JSON}')

    def _generate_page_section(data, key):
        section = ''
        for r in data:
            if r['type'] == key:
                section += f"""
                <ac:layout-section ac:type="two_left_sidebar">
                <ac:layout-cell>
                <h1>{r['resource']} - {r['action']}</h1>
                <p><strong>Resource</strong>:{r['resource']}</p>
                <p><strong>Action</strong>: {r['action']}</p>
                <p><strong>Description</strong>: {r['description'] if 'description' in r else ''}</p>
                </ac:layout-cell><ac:layout-cell>
                    <table class="relative-table wrapped" style="width: 98.4688%;">
                    <colgroup> <col style="width: 31.1497%;"/><col style="width: 5.60534%;"/><col style="width: 6.72641%;"/><col style="width: 31.7102%;"/><col style="width: 24.7283%;"/></colgroup>
                    <tbody>
                        <tr><th scope="col">Description</th><th scope="col">Type</th><th scope="col">Action</th><th scope="col">Capability Action</th><th scope="col">Resource</th></tr>
                """
                for s in r['capabilities']:
                    section += f"""
                    <tr>
                    <td>{s['description'] if 'description' in s else ''}</td>
                    <td>{s['type']}</td>
                    <td>{s['action']}</td>
                    <td>{s['name']}</td>
                    <td>{s['resource']}</td>
                    </tr>
                    """
                section += "</tbody></table></ac:layout-cell></ac:layout-section>"
        return section
    
    outputHtml = f"""
    <ac:layout> {_generate_page_section(okapi['capabilitySets'], 'data')} </ac:layout>
    <ac:layout> {_generate_page_section(okapi['capabilitySets'], 'settings')} </ac:layout>
    <ac:layout> {_generate_page_section(okapi['capabilitySets'], 'procedural')} </ac:layout>
    """
    with open(output_HTML, "w") as f:
        f.write(outputHtml)
    print(f"""
          Expanded Capability Sets has been processed and saved to the local file system.
          file: {output_HTML}
                        ------ Step Complete -----
    """)

def expand_and_save_capability_sets():
    expand_capability_sets()
    generate_csv()
    generate_wiki_page()