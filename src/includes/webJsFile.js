
var globalList = []
var globalSelList = []
var globalSelInd = []
var globalSel = ''
function updateCheck1(name) {
    var checkBox = document.getElementById(name);
    checkBox.checked = true;
    updateCheckData();
}
function updateCheck(checkbox, name) {
    updateCheckData();
}
function updateCheckData() {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
    const ary = [];
    checkboxes.forEach( (checkbox) => {
        var ckVal = checkbox.value
        if (!ckVal.endsWith("_b")) {
            ary.push(ckVal);
        }
    }
    );
    selectedValues = [...new Set(ary)]
    var cap_sets = JSON.parse(document.getElementById('cap_sets').textContent);
    var cap_data = JSON.parse(document.getElementById('cap_data').textContent);
    var caps = [];
    globalSelList = []
    globalSelInd = []
    selectedValues.forEach( (c) => {
        if (cap_sets[c]) {
            caps = [...caps, ...cap_sets[c]]
            globalSelList.push(cap_data[c])
        } else {
            caps.push(c)
            globalSelInd.push(c)
        }
    }
    );
    console.log(globalSelList)
    globalList = [...new Set(caps)];
    updateDisplays();
}
function updateList(value) {
    if (value == 000) {
        var checkboxes = document.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.checked = false;
        }
        );
        globalList = []
        document.getElementById('missing_items').innerHTML = "";
        document.getElementById('extra_items').innerHTML = "";
        globalSel = '';
    } else {
        globalSel = value;
        updateDisplays();
    }
}
function buildList(data) {
    var cap_data = JSON.parse(document.getElementById('cap_data').textContent);
    var rtnHtml = "<ul>"
    data.forEach(item => {
        rtnHtml += `
                            <li>${cap_data[item]['resource']} (<i>${cap_data[item]['type']}</i>) -> <b>${cap_data[item]['action']}</b>
                            <br />
                            <span style="font-size: small;" >${cap_data[item]['description']}</span></li>`;
    }
    )
    rtnHtml += "</ul>"
    return rtnHtml
}
function buildTable(data) {
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
    }
    );
    rtnHtml += "</tbody></table>";
    return rtnHtml;
}
function updateDisplays() {
    var okapi_data = JSON.parse(document.getElementById('okapi_data').textContent);
    var cap_sets = JSON.parse(document.getElementById('cap_sets').textContent);
    var find_cap = JSON.parse(document.getElementById('find_sets').textContent);
    var suggest = []
    find_cap.forEach(item => {
        if (item['id'] == globalSel) {
            suggest.push(item)
        }
    }
    )
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
function exportOne() {
    var cap_data = JSON.parse(document.getElementById('cap_data').textContent);
    var exportData = [
        ['level', 'type', 'resource', 'action']
    ]
    globalSelList.forEach(item => {
        exportData.push(['Capability set', item.type, item.resource, item.action])

    })
    globalSelInd.forEach(item => {
        exportData.push(['Capability', cap_data[item]['type'], cap_data[item]['resource'], cap_data[item]['action']])
    })
    var okapi_data = JSON.parse(document.getElementById('okapi_data').textContent);
    downloadCSV(exportData, `${okapi_data[globalSel]['displayName']}.csv`)
}
function downloadCSV(data, filename='data.csv') {
    const csvString = data.map(row => row.join(',')).join('\n');
    const blob = new Blob([csvString],{
        type: 'text/csv;charset=utf-8;'
    });

    if (navigator.msSaveBlob) {
        // IE
        navigator.msSaveBlob(blob, filename);
    } else {
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }
}
function togglePanel(id) {
    const panelContent = document.querySelector(`#${id} .panel-content`);
    panelContent.classList.toggle('expanded');
}