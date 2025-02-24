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
output_JSON = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_WORKING_WEB_PAGE")}.json"
output_CSV = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_WORKING_WEB_PAGE")}.csv"
output_HTML  = f"{os.getenv("BASE_DIR")}{os.getenv("FILE_WORKING_WEB_PAGE")}.html"

def generate_web_page():
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
            return f'<input type="checkbox" id="{data}" name="{data}" value="{data}" onClick="runMe()">'
        return ''
    
    def _gen_table(data, header):
        tmpHtml = f'<h3>{header}</h3>'
        tmpHtml += '''<div style="position: static; overflow: auto; max-height: 464px; width: 100%;" >
        <table id="mainTable">
        <tr><th style="width: 15%;">Application</th><th style="width: 35%;">Resource</th><th>View</th><th>Edit</th><th>Create</th><th>Delete</th><th>Manage</th><th>Execute</th></tr>'''
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
        tmpHtml += "</table></div>"
        return tmpHtml
    
    def _gen_select_box():
        tmpHtml = '''<label for="role">Choose a role to work on:</label></br>
                    <select name="role" id="role" onChange="updateList(this.value)">
                    <option value="000">Select a Role</option>
                    '''
        for o in okapiCur:
            tmpHtml += f'<option value="{o['id']}">{o['displayName']}</option>'
        tmpHtml += '</select>'
        return tmpHtml

    #### Generate the HTML
    outputHtml = """<style>
        #mainTable {font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100%; font-size: small;}
        #mainTable td, #cusmainTabletomers th {border: 1px solid #ddd; padding: 8px;}
        #mainTable tr:nth-child(even){background-color: #f2f2f2;}
        #mainTable tr:hover {background-color: #ddd;}
        #mainTable th { padding-top: 12px;padding-bottom: 12px; text-align: left; background-color: #04AA6D;color: white;}
        .container { width: 100%; background: #f2f2f2; }
        .table_area, .section {float: left;padding: 20px;min-height: 170px;box-sizing: border-box;}
        .table_area {  width: 60%; overflow: scroll; max-height: 90%;}
        .section { width: 40%; background: #d4d7dc; }
        .clearfix:after { content: "."; display: block; height: 0; clear: both; visibility: hidden; }
        .data_display: { position: static; overflow: auto; max-height: 400px; width: 100%; }
        </style>"""
    outputHtml += '''<script  type="text/javascript">
                        var globalList = []
                        var globalSel = ''
                        function runMe(){
                            const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
                            const selectedValues = [];
                            checkboxes.forEach((checkbox) => {
                                selectedValues.push(checkbox.value);
                            });
                            var cap_sets = JSON.parse(document.getElementById('cap_sets').textContent);
                            var cap_data = JSON.parse(document.getElementById('cap_data').textContent);
                            var caps = [];
                            selectedValues.forEach((c) => {
                                if( cap_sets[c] ){
                                    caps = [ ...caps, ...cap_sets[c]]
                                }else{
                                    caps.push(c)
                                }
                            });
                            globalList = [...new Set(caps)];
                            console.log(selectedValues);
                            console.log(caps);
                            updateDisplays();
                        }
                        function updateList(value){
                            if ( value == 000 ){
                                var checkboxes = document.querySelectorAll('input[type="checkbox"]');
                                checkboxes.forEach(checkbox => {
                                    checkbox.checked = false;
                                });
                                globalList = []
                                document.getElementById('missing_items').innerHTML = "";
                                document.getElementById('extra_items').innerHTML = "";
                                globalSel = '';
                            }else{
                                globalSel = value;
                                updateDisplays();
                            }
                        }
                        function buildList(data){
                            var cap_data = JSON.parse(document.getElementById('cap_data').textContent);
                            var rtnHtml = "<ul>"
                            data.forEach( item => {
                                rtnHtml += '<li>' + cap_data[item]['resource'] + ' (<i>' + cap_data[item]['type'] + '</i>) -> <b>' + cap_data[item]['action'] + '</b><br /><span style="font-size: small;" >' + cap_data[item]['description'] + '</span></li>'
                            })
                            rtnHtml += "</ul>"
                            return rtnHtml
                        }
                        function updateDisplays(){
                                var okapi_data = JSON.parse(document.getElementById('okapi_data').textContent);
                                var cap_sets = JSON.parse(document.getElementById('cap_sets').textContent);
                                var okPerms = okapi_data[globalSel]['allEurekaPermissions']
                                var missing = okPerms.filter(x => !globalList.includes(x));
                                const set1 = new Set(okPerms)
                                var extra = globalList.filter(x => !set1.has(x));
                                document.getElementById('missing_items').innerHTML = buildList(missing);
                                document.getElementById('extra_items').innerHTML = buildList(extra);
                                document.getElementById('assigned_items').innerHTML = buildList(globalList);
                                document.getElementById('missing_len').innerHTML = "(" + missing.length + ")";
                                document.getElementById('extra_len').innerHTML = "(" + extra.length + ")";
                                document.getElementById('assigned_len').innerHTML = "(" + globalList.length + ")";
                        
                        }
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
                    </script>'''
    
    outputHtml += '''<body><div class="container">
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
    outputHtml += '</div><div class="section">'
    outputHtml += _gen_select_box()
    outputHtml += '''<h2>Missing Capabilities <span id="missing_len"><span></h2><br />
                    <div id="missing_items" style="position: static; overflow: auto; max-height: 400px; width: 100%;" >MISSING ITEMS</div>
                    <h2>Extra Capabilities <span id="extra_len"><span></h2><br />
                    <div id="extra_items" style="position: static; overflow: auto; max-height: 400px; width: 100%;" >EXTRA ITEMS</div>
                    <h2>Assigned Capabilities <span id="assigned_len"><span></h2><br />
                    <div id="assigned_items" style="position: static; overflow: auto; max-height: 400px; width: 100%;" >EXTRA ITEMS</div>
                    '''

    outputHtml += '</div></div></div></body>'

    with open(output_HTML, "w") as f:
        f.write(outputHtml)
    print(f"""
          The FOLIO Roles Simulator ahs been generated and saved to the local file system.
          file: {output_HTML}
                        ------ Script Complete -----
""")



generate_web_page()