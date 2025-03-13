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
findCapSets_JSON = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_FIND_MY_CAPABILITIES")}.json"
output_JSON = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_WORKING_WEB_PAGE")}.json"
output_CSV = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_WORKING_WEB_PAGE")}.csv"
output_HTML  = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_WORKING_WEB_PAGE")}_non-caparison.html"

def generate_mock_web_page():
    print("""Processing data files and creating web interface""")
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

    # Pull the JSON file containing the Eureka Capabilities and ingest it as JSON.
    if os.path.isfile(CurrentToCapabilities_JSON):  # Check if the file exists
        with open(CurrentToCapabilities_JSON, 'r') as f:
            okapiCur = json.load(f)
        print(f'Reference file loaded: {CurrentToCapabilities_JSON}')
    else:
        print(f'Error: JSON file not found. {CurrentToCapabilities_JSON}')

    # Pull the JSON file containing the Eureka Capabilities and ingest it as JSON.
    if os.path.isfile(findCapSets_JSON):  # Check if the file exists
        with open(findCapSets_JSON, 'r') as f:
            findCap = json.load(f)
        print(f'Reference file loaded: {findCapSets_JSON}')
    else:
        print(f'Error: JSON file not found. {findCapSets_JSON}')


    # Order everything:
    eurCapSet = eurCapSet['capabilitySets']
    eurCapSet = sorted(eurCapSet, key=lambda x: ( x['type'], x['resource']))
    okapiCur = sorted(okapiCur, key=lambda x: ( x['displayName']))
    eurCaps = eurCaps['capabilities']
    eurCaps = sorted(eurCaps, key=lambda x: ( x['type'], x['resource']))

    #-------------------
    #   Reformat data for inclusion in the HTML page.
    #-------------------
    # Reformat the okapi current permissions to a smaller dataset
    nwOkapiCurData = {}
    for o in okapiCur:
        nwOkapiCurData[o['id']] = {
            "displayName": o['displayName'],
            "total": o['total'],
            "allEurekaPermissions": o['allEurekaPermissions']
        }
    #Reformat Capability Sets
    newCapSet = {}
    for c in eurCapSet:
        newCapSet[c['id']] = c['capabilities']
    #reformat Capabilities
    newCaps = {}
    for c in eurCaps:
        newCaps[c['id']] = {
            "resource": c['resource'],
            "type": c['type'],
            "action": c['action'],
            "description": c['description'] if "description" in c else ''
        }
    for c in eurCapSet:
        newCaps[c['id']] = {
            "resource": c['resource'],
            "type": c['type'],
            "action": c['action'],
            "description": c['description'] if "description" in c else ''
        }
    

    def _filter_results(data, filter):
        tmpResults = []
        resource = ''
        tmpAry = {}
        for s in data:
            if s['type'] == filter:
                if resource != s['resource']:
                    if len( tmpAry ) >= 1:
                        tmpResults.append(tmpAry)
                    resource = s['resource']
                    tmpAry = {
                        "resource": s['resource'],
                        "application": s['applicationId'],
                        "ckView": '',
                        "ckEdit": '',
                        "ckCreate": '',
                        "ckDelete": '',
                        "ckManage": '',
                        "ckExecute": ''
                    }
                tmpAry['ckView'] = s['id'] if s['action'] == 'view' else tmpAry['ckView']
                tmpAry['ckEdit'] = s['id'] if s['action'] == 'edit' else tmpAry['ckEdit']
                tmpAry['ckCreate'] = s['id'] if s['action'] == 'create' else tmpAry['ckCreate']
                tmpAry['ckDelete'] = s['id'] if s['action'] == 'delete' else tmpAry['ckDelete']
                tmpAry['ckManage'] = s['id'] if s['action'] == 'manage' else tmpAry['ckManage']
                tmpAry['ckExecute'] = s['id'] if s['action'] == 'execute' else tmpAry['ckExecute']
        return tmpResults


    dataCapSets = _filter_results(eurCapSet, 'data')
    settingsCapSets = _filter_results(eurCapSet, 'settings')
    proceduralCapSets = _filter_results(eurCapSet, 'procedural')
    dataCaps = _filter_results(eurCaps, 'data')
    settingsCaps = _filter_results(eurCaps, 'settings')
    proceduralCaps = _filter_results(eurCaps, 'procedural')



    with open(output_JSON, 'w') as file:
        json.dump(dataCapSets, file, indent=4)
    print(f"Saved Comparison JSON file {output_JSON}")

    def _gen_check_box(data):
        if data:
            return f'''<input type="checkbox" id="{data}" name="{data}" value="{data}" onChange="updateCheck(this, '{data}')" />'''
        return ''
    
    def _gen_table(data, header):
        tmpHtml = f'<h3>{header}</h3>'
        tmpHtml += '''<div style="position: static; overflow: auto; max-height: 464px; width: 100%;" >
        <table id="mainTable">
            <thead>
                <tr>
                    <th style="width: 15%;">Application</th>
                    <th style="width: 35%;">Resource</th>
                    <th>View</th><th>Edit</th>
                    <th>Create</th>
                    <th>Delete</th>
                    <th>Manage</th>
                    <th>Execute</th>
                </tr>
            </thead>
            <tbody>'''
        for t in data:
            tmpHtml += f"""<tr>
            <td style="font-size: xx-small;">{t['application']}</td>
            <td>{t['resource']}</td>
            <td>{_gen_check_box(t['ckView'])}</td>
            <td>{_gen_check_box(t['ckEdit'])}</td>
            <td>{_gen_check_box(t['ckCreate'])}</td>
            <td>{_gen_check_box(t['ckDelete'])}</td>
            <td>{_gen_check_box(t['ckManage'])}</td>
            <td>{_gen_check_box(t['ckExecute'])}</td>
            </tr>"""
        tmpHtml += "</tbody></table></div>"
        return tmpHtml

    #### Generate the HTML

    
    with open('./src/includes/webCss2.css', 'r') as fileCss:
        css_content = fileCss.read()

    outputHtml = f'''
                    <style>
                    {css_content}
                    </style>
                '''
    
    with open('./src/includes/webJsFile2.js', 'r') as fileJs:
        js_content = fileJs.read()
    outputHtml += f'''
                    <script>
                    {js_content}
                    </script>
                '''
    outputHtml += f'''
                    <script id="okapi_data" type="application/json">
                        {json.dumps(nwOkapiCurData)}
                    </script>
                    <script id="cap_sets" type="application/json">
                      {json.dumps(newCapSet)}
                    </script>
                    <script id="cap_data" type="application/json">
                      {json.dumps(newCaps)}
                    </script>
                    <script id="find_sets" type="application/json">
                      {json.dumps(findCap)}
                    </script>'''
    
    outputHtml += '''<body>
                        <div class="container">
                            <div class="header">
                                <h1>FOLIO Roles Simulator</h1>
                            </div>
                            <div class="wrapper clearfix">
                                <div class="table_area">'''
    outputHtml += '<h2>Capability Sets</h2>'
    outputHtml += _gen_table(dataCapSets, 'Data')
    outputHtml += _gen_table(settingsCapSets, 'Settings')
    outputHtml += _gen_table(proceduralCapSets, 'Procedural')
    outputHtml += '<h2>Capabilities</h2>'
    outputHtml += _gen_table(dataCaps, 'Data')
    outputHtml += _gen_table(settingsCaps, 'Settings')
    outputHtml += _gen_table(proceduralCaps, 'Procedural')
    outputHtml += '''
                                </div>
                            <div class="section">
                                <button onClick="exportOne()">Export Capabilities</button>
                                <button onClick="exportTwo()">Export Details</button>
                                <br /><br />
                                <div class="panel" id="panel3">
                                    <div class="panel-header" onclick="togglePanel('panel3')">
                                        <h3>Assigned Capabilities <span id="assigned_len"><span></h3>
                                        <span style=" font-size: small; font-style: italic;">All Capabilities that will be assigned based on your selection</span>
                                    </div>
                                    <div class="panel-content expanded" >
                                        <div id="assigned_items" class="table-container" ></div>
                                    </div>
                                </div>
                    '''

    outputHtml += '''       </div>
                        </div>
                    </body>'''

    with open(output_HTML, "w") as f:
        f.write(outputHtml)
    print(f"""
          The FOLIO Roles Simulator ahs been generated and saved to the local file system.
          file: {output_HTML}
                        ------ Script Complete -----
""")
