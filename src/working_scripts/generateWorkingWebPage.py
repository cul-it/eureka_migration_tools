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
            .table-container {
                width: 100%;
                height: 400px; /* Adjust the height as needed */
                overflow-y: auto;
                border: 1px solid #ccc;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                font-family: Arial, Helvetica, sans-serif;
                font-size: small;
            }

            th, td {
                padding: 8px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }

            tr:hover {
                background-color: #ddd;
            }
            tr:nth-child(even){
                background-color: #f2f2f2;
            }
            thead th {
                position: sticky;
                top: 0;
                background-color: #04AA6D;
                color: white;
                z-index: 1;
            }
            .container { width: 100%; background: #f2f2f2; }
            .table_area, .section {float: left;padding: 20px;min-height: 170px;box-sizing: border-box;}
            .table_area {  width: 60%; overflow: scroll; max-height: 90%;}
            .section { width: 40%; background: #d4d7dc; }
            .clearfix:after { content: "."; display: block; height: 0; clear: both; visibility: hidden; }
            .data_display: { position: static; overflow: auto; max-height: 400px; width: 100%; }
            .panel{border:1px solid #ccc;border-radius:4px;overflow:hidden; auto}
            .panel-header{background-color:#f1f1f1;padding:1px;cursor:pointer}
            .panel-content{max-height:0;overflow:hidden;transition:max-height .3s ease}
            .panel-content.expanded{max-height:300px}
        </style>"""
    outputHtml += '''<script  type="text/javascript">
                        var globalList = []
                        var globalSel = ''
                        function updateCheck1(name){                          
                            var checkBox = document.getElementById(name);
                            checkBox.checked = true;
                            updateCheckData();
                        }
                        function updateCheck(checkbox, name) {
                            updateCheckData();
                        }
                        function updateCheckData(){
                            const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
                            const ary = [];
                            checkboxes.forEach((checkbox) => {
                                var ckVal = checkbox.value
                                if (!ckVal.endsWith("_b")){
                                    ary.push(ckVal);
                                }
                            });
                            selectedValues = [...new Set(ary)]
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
                                rtnHtml += `
                                <li>${cap_data[item]['resource']} (<i>${cap_data[item]['type']}</i>) -> <b>${cap_data[item]['action']}</b>
                                <br />
                                <span style="font-size: small;" >${cap_data[item]['description']}</span></li>`;
                            })
                            rtnHtml += "</ul>"
                            return rtnHtml
                        }function buildTable(data) {
                            var rtnHtml = `<table id="mainTable">
                                                <thead>
                                                    <tr>
                                                        <th>Ranking</th>
                                                        <th>Cap/Matched</th>
                                                        <th>Type</th>
                                                        <th>Name</th>
                                                        <th>Action</th>
                                                        <th>Selected</th>
                                                    </tr>
                                                </thead>
                                                <tbody>`;
                            data.forEach(item => {
                                rtnHtml += `
                                    <tr>
                                        <td>${item['ranking']}</td>
                                        <td>${item['totalCapInSet']}/${item['capabilitiesInPermissionSet']}</td>
                                        <td>${item['eurekaType']}</td>
                                        <td>${item['eurekaResource']}</td>
                                        <td>${item['eurekaAction']}</td>
                                        <td><button onClick="updateCheck1('${item['eurekaId']}')">Add</button></td>
                                    </tr>`;
                            });
                            rtnHtml += "</tbody></table>";
                            return rtnHtml;
                        }
                        function updateDisplays(){
                                var okapi_data = JSON.parse(document.getElementById('okapi_data').textContent);
                                var cap_sets = JSON.parse(document.getElementById('cap_sets').textContent);
                                var find_cap = JSON.parse(document.getElementById('find_sets').textContent);
                                var suggest = []
                                find_cap.forEach(item => {
                                    if ( item['id'] == globalSel ){
                                        suggest.push(item)
                                    }
                                })
                                var okPerms = okapi_data[globalSel]['allEurekaPermissions']
                                var missing = okPerms.filter(x => !globalList.includes(x));
                                const set1 = new Set(okPerms)
                                var extra = globalList.filter(x => !set1.has(x));
                                document.getElementById('missing_items').innerHTML = buildList(missing);
                                document.getElementById('extra_items').innerHTML = buildList(extra);
                                document.getElementById('assigned_items').innerHTML = buildList(globalList);
                                document.getElementById('suggested_sets').innerHTML = buildTable(suggest);
                                document.getElementById('missing_len').innerHTML = "(" + missing.length + ")";
                                document.getElementById('extra_len').innerHTML = "(" + extra.length + ")";
                                document.getElementById('assigned_len').innerHTML = "(" + globalList.length + ")";
                        
                        }
                        function togglePanel(id) {
                            const panelContent = document.querySelector(`#${id} .panel-content`);
                            panelContent.classList.toggle('expanded');
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
                            <div class="section">'''
    outputHtml += _gen_select_box()
    outputHtml += '''
                                <div class="panel" id="panel1">
                                    <div class="panel-header" onclick="togglePanel('panel1')">
                                        <h3>Missing Capabilities <span id="missing_len"><span></h3>
                                        <span style=" font-size: small; font-style: italic;">Based on the Permission set these Capabilities are missing</span>
                                    </div>
                                    <div class="panel-content expanded" >
                                        <div id="missing_items" class="table-container" ></div>
                                    </div>
                                </div>
                                <br />
                                <div class="panel" id="panel4">
                                    <div class="panel-header" onclick="togglePanel('panel4')">
                                        <h3>Suggested Capability Sets</h3>
                                        <span style=" font-size: small; font-style: italic;">Suggested Capabilities sets; these are ranked by the number of matching capabilities in the set</span>
                                    </div>
                                    <div class="panel-content expanded" >
                                        <div id="suggested_sets" class="table-container" ></div>
                                    </div>
                                </div>
                                <br />
                                <div class="panel" id="panel2">
                                    <div class="panel-header" onclick="togglePanel('panel2')">
                                        <h3>Extra Capabilities <span id="extra_len"><span></h3>
                                        <span style=" font-size: small; font-style: italic;">Extra Capabilities that will be assigned based on your selection</span>
                                    </div>
                                    <div class="panel-content expanded" >
                                        <div id="extra_items" class="table-container" ></div>
                                    </div>
                                </div>
                                <br />
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



generate_web_page()