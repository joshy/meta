/* ================================================================================

    File recognition and validation of structure
    Created by J. Odermatt, Y. Hasler

================================================================================ */

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
        'type': 'first_name',
        'used': false,
        'values': ['first_name', 'vorname', 'prenom']
    }
);
autoMatches.push(
    {
        'type': 'last_name',
        'used': false,
        'values': ['last_name', 'name', 'nachname', 'nom']
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
        'type': 'patient_id',
        'used': false,
        'values': ['patient_id', 'patient']
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

/* Create output table */
function CreateTable(data, amount = -1) {
    if (amount == -1) {
        amount = data.length;
    }

    var table = document.createElement('table');
    table.className = "table-responsive";
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
            parseControl.prop('disabled', false);
            fileControl.parent('form').removeClass('invalid');
            result = true;
            break;
        default:
            parseControl.prop('disabled', true);
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

    fillBoxes(data);

    //var result = FinalizeData(data);
    console.log(JSON.stringify(data, 2, 2));
}

function fillBoxes(data) {
    toggleLoader(3);

    var parent = $('.step-2 .data-list');
    var box = parent.find('.data-template > div');

    $.each(data['header'], function(key, value) {
        var tempBox = box.clone(true);
        tempBox.addClass("box box-" + key).removeClass('data-template');
        tempBox.data('id', key);

        tempBox.find('[data-tmpl="header"]').html(value.title);
        tempBox.find('[data-tmpl="sampledata"]').html(value.sampledata);
        tempBox.find('[data-tmpl="select"]').val(value.selected);
        tempBox.appendTo(parent);
    });

    $(window).on('change', box, function(event) {
        changeSelectedData(event.target, data);
    });

    $('#fileupload').trigger('next.m.' + 2);
    toggleLoader(3);
}

/* change selected values */
function changeSelectedData(select, data) {
    // change views
    var $select = $(select);
    var box = $(select).closest('.box');
    var selectValue = $select.val();

    $('.box select').each(function() {
        if ($(this).val() == $select.val()) {
            $(this).val("");
        }
    });
    $select.val(selectValue);
    $select.removeClass('has-danger');

    // change data array
    $.each(data['header'], function (key, value) {
        if (value['selected'] && value['selected'] == selectValue) {
            value['selected'] = "";
        }
        if (key == box.data('id')) {
            value['selected'] = selectValue;
        }
    });

    console.log(data);
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
                case 'first_name':
                    $.each(data['content'], function (subkey, subvalue) {
                        result[subkey]['full_name'] = subvalue[key] + result[subkey]['full_name'];
                    });
                    break;
                case 'last_name':
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
                case 'patient_id':
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
                headerItem['sampledata'] = [];
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
        headerItem['sampledata'] = [];
        headerItem['noHeaderProvided'] = true;
        for (var i = 0; i <= maxColSize; i++) {
            result['header'].push(headerItem);
        }
    }

    var maxSampleData = 4;
    if (result['content'].length < maxSampleData) {
        maxSampleData = result['content'].length;
    }

    for (var i = 0; i < maxSampleData; i++) {
        for (var j = 0; j < result['header'].length; j++) {
            result['header'][j]['sampledata'].push(result['content'][i][j]);
        }
    }

    return result;
}

/* ================================================================================
    Step Helper
================================================================================ */

function toggleLoader(nextStep) {
    var loaderBtn = $('.btn.step-' + (nextStep-1));

    if (loaderBtn.hasClass('loading')) {
        loaderBtn.removeClass('loading');
        loaderBtn.prop("disabled", false);
    } else {
        loaderBtn.addClass('loading');
        loaderBtn.prop("disabled", true);
    }
}

/* ================================================================================
    Main
================================================================================ */

$(function () {
    /* define controls */
    fileControl = $('#uploadFile');
    parseControl = $('#parseControl');
    rowHeaderControl = $('#firstRowIsHeader');
    previewControl = $('#filePreview');

    /* init */
    parseControl.prop('disabled', true);

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



    /* multi steps handler */
    sendEvent = function(sel, nextStep) {
        switch(nextStep) {
            case 2:
                // check file validation
                
                break;

            case 3:
                // check output
                var parent = $('.step-3 .patient-list');
                var tmpl = parent.find('.data-template').html();

                var appended = parent.append(tmpl);
                appended.find('[data-tmpl="info"]').html('Patient blah');
                appended.find('[data-tmpl="id"]').attr('data-id', 1);

                // when there are not founded patients
                if (false) {
                    $(sel).trigger('next.m.' + nextStep);
                } else {
                    $(sel).trigger('next.m.' + (nextStep+1));
                }
                break;

            case 4:
                $(sel).trigger('next.m.' + nextStep);
                break;

            case 5:
                // make exakt matches out of selected closest match
                $(sel).trigger('next.m.' + nextStep);
                break;

            default:
                $(sel).trigger('next.m.' + nextStep);
                break;
        }

    }
});