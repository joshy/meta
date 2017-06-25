/* NERF THIS! */
var fileControl = false;
var parseControl = false;
var rowHeaderControl = false;
var previewControl = false;

/* define valid date formats for birthdate detection* */

var birthdayFormats = [
    'YYYYMMDD',
    'YYYY-MM-DD',
    'YYYY-MM-DD HH:mm:ss',
    'DD.MM.YYYY',
    'DD.MM.YY'
]


/* define auto matiching mechanics */
var autoMatches = [];
autoMatches.push(
    {
        'type': 'firstname',
        'used': false,
        'values': ['firstname', 'vorname', 'prenom']
    }
);
autoMatches.push(
    {
        'type': 'lastname',
        'used': false,
        'values': ['lastname', 'name', 'nachname', 'nom']
    }
);
autoMatches.push(
    {
        'type': 'birthdate',
        'used': false,
        'values': ['geburtsdatum', 'geburtstag', 'birthdate']
    }
);

autoMatches.push(
    {
        'type': 'patientid',
        'used': false,
        'values': ['patientid', 'patient']
    }
);

/* ================================================================================
    Generic Helper Functions
================================================================================ */

/* Check Browser support */
function CheckBrowserSupport() {
    if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
        alert('File API not supported by browser!')
        return false;
    }
    else if (!fileControl.prop('files')) {
        alert('Files property not supported by browser!');
        return false;
    }
    return true;
}

function CreateTable(data, amount = -1) {
    if (amount == -1) {
        amount = data.length;
    }

    var table = document.createElement('table');
    for (var i = 0; i < amount; i++) {
        var row = document.createElement('tr');
        if (data[i]) {
            for (var j = 0; j < data[i].length; j++) {
                var cell = document.createElement((i == 0 && rowHeaderControl.is(':checked') ? 'th' : 'td'));
                cell.textContent = data[i][j];
                row.appendChild(cell);
            }
        }
        table.appendChild(row);
    }
    return table;
}

/* ================================================================================
    File Helper Functions
================================================================================ */

/* Get File Extension based on filename */
function GetFileExtension(fileName) {
    var extension = fileName.replace(/^.*\./, '');

    if (extension == fileName) {
        extension = '';
    } else {
        extension = extension.toLowerCase();
    }

    return extension;
}

/* Get file if correct extension */
function CheckFile() {
    var extension = GetFileExtension(fileControl.val());
    var result = false;
    switch (extension) {
        case 'csv':
        case 'xls':
        case 'xlsx':
            parseControl.show();
            fileControl.parent('form').removeClass('invalid');
            result = true;
            break;
        default:
            parseControl.hide();
            fileControl.parent('form').addClass('invalid');
            break;
    }
    return result;
}

/* Get File content (header + content) based on file extension */
function GetFileContent(callback) {
    var extension = GetFileExtension(fileControl.val());

    if (CheckBrowserSupport()) {
        var file = fileControl.prop('files')[0];
        var reader = new FileReader();
        if (extension == 'csv') {
            // get csv data
            reader.readAsText(file);
            reader.onload = function (event) {
                var csv = event.target.result;
                callback($.csv.toArrays(csv));
            };
        }
        else if (extension == 'xlsx' || extension == 'xls') {
            // get excel data
            reader.onload = function (event) {
                var data = event.target.result;
                var arr = String.fromCharCode.apply(null, new Uint8Array(data));
                var wb = XLSX.read(btoa(arr), { type: 'base64' });
                callback(WorkbookToJson(wb));
            };
            reader.readAsArrayBuffer(file);
        };
    };
    return;
}

/* ================================================================================
    File Data Functions
================================================================================ */

/* Create JSON from workbook (parse every sheet!) */
function WorkbookToJson(workbook) {
    var result = false;
    workbook.SheetNames.forEach(function (sheetName) {
        var roa = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName], { header: 1 });
        if (roa.length > 0) {
            if (result === false) {
                result = roa;
            }
        }
    });
    return result;
}

/* Display Preview Content */
function PreviewFileContent(data) {
    var table = CreateTable(data, 5);
    previewControl.html(table);
}

/* Prepare Content for next step */
function PrepareFileContent(data) {
    data = SplitData(data);
    data = DetectBirthdate(data);
    data = PrepareDefaults(data);

    var result = FinalizeData(data);
    console.log(JSON.stringify(result, 2, 2));
}

/* prepare data to send */
function FinalizeData(data) {
    var result = [];

    // prefill empty data array
    $.each(data['content'], function (key, value) {
        result.push({
            'full_name': '',
            'birthdate': '',
            'patient_id':''
        })
    });

    // fill data array based on selected cols
    $.each(data['header'], function (key, value) {
        if (value['selected']) {
            switch (value['selected']) {
                case 'firstname':
                    $.each(data['content'], function (subkey, subvalue) {
                        result[subkey]['full_name'] = subvalue[key] + result[subkey]['full_name'];
                    });
                    break;
                case 'lastname':
                    $.each(data['content'], function (subkey, subvalue) {
                        result[subkey]['full_name'] = result[subkey]['full_name'] + subvalue[key];
                    });
                    break;
                case 'fullname':
                    $.each(data['content'], function (subkey, subvalue) {
                        result[subkey]['full_name'] = subvalue[key];
                    });

                    break;
                case 'birthdate':
                    $.each(data['content'], function (subkey, subvalue) {
                        $.each(birthdayFormats, function (key, value) {
                            var parsedDate = moment(subvalue[key], value, true);
                            if (parsedDate.isValid()) {
                                result[subkey]['birthdate'] = parsedDate.format('DD.MM.YYYY');
                            }
                        });
                    });

                    break;
                case 'patientid':
                    $.each(data['content'], function (subkey, subvalue) {
                        result[subkey]['patient_id'] = subvalue[key];
                    });

                    break;
            }

        }
    });

    result = { patients: result };
    return result;
}

/* Prepare default dropdown values */
function PrepareDefaults(data) {
    var birthdateUsed = false;
    $.each(data['header'], function (key, value) {
        if (value['autoMatchType']) {
            data['header'][key]['selected'] = value['autoMatchType'];
            if (value['autoMatchType'] == 'birthdate') {
                birthdateUsed = true;
            }
        }
    });

    if (!birthdateUsed) {
        $.each(data['header'], function (key, value) {
            if (value['possibleBirthdate']) {
                data['header'][key]['selected'] = 'birthdate';
                return false;
            }
        });
    }

    return data;
}

/* auto detect birthdate based on values */
function DetectBirthdate(data) {
    if (data['content'].length > 0) {
        var firstDataLine = data['content'][0];

        for (var i = 0; i < firstDataLine.length; i++) {
            $.each(birthdayFormats, function (key, value) {
                var parsedDate = moment(firstDataLine[i], value, true);
                if (parsedDate.isValid()) {
                    data['header'][i]['possibleBirthdate'] = true;
                }
            });
        }
    }

    return data;
}

/* prepare data for manipulation */
function SplitData(data) {
    var result = { 'header': [], 'content': [] };
    var maxColSize = 0;

    for (var i = 0; i < data.length; i++) {
        if (rowHeaderControl.is(':checked') && i == 0) {
            var headerData = [];
            for (var j = 0; j < data[i].length; j++) {
                var headerItem = {};
                var title = data[i][j];
                headerItem['title'] = title;
                title = $.trim(title.toLowerCase());

                $.each(autoMatches, function (index, item) {
                    if ($.inArray(title, item['values']) !== -1) {
                        if (!item['used']) {
                            headerItem['autoMatchType'] = item['type'];
                            item['used'] = true;
                        }
                    }
                })
                result['header'].push(headerItem);
            }
        }
        else {
            if (data[i].length > maxColSize) {
                maxColSize = data[i].length;
            }
            result['content'].push(data[i]);
        }
    }

    if (result['header'].length == 0) {
        var headerItem = {};
        headerItem['title'] = '';
        headerItem['noHeaderProvided'] = true;
        for (var i = 0; i <= maxColSize; i++) {
            result['header'].push(headerItem);
        }
    }

    return result;
}


/* ================================================================================
    Main
================================================================================ */

$(function () {
    /* define controls */
    fileControl = $('#uploadFile');
    parseControl = $('#btnParse');
    rowHeaderControl = $('#firstRowIsHeader');
    previewControl = $('#filePreview');

    /* init */
    parseControl.hide();

    /* bind events */
    fileControl.on('change', function () {
        if (CheckFile()) {
            GetFileContent(PreviewFileContent);
        };
    });

    rowHeaderControl.on('change', function () {
        if (CheckFile()) {
            GetFileContent(PreviewFileContent);
        };
    })

    parseControl.on('click', function () {
        GetFileContent(PrepareFileContent);
    });
});