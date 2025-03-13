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
    globalList = [...new Set(caps)];
    document.getElementById('assigned_items').innerHTML = buildList(globalList);
    document.getElementById('assigned_len').innerHTML = "(" + globalList.length + ")";
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
    downloadCSV(exportData, `export.csv`)
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