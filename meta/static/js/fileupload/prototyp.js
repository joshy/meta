/* ================================================================================

    File recognition and validation of structure
    Created by J. Odermatt, Y. Hasler

================================================================================ */

/* define global variables */
var fileControl = false;
var parseControl = false;
var resetControl = false;
var rowHeaderControl = false;
var previewControl = false;
var dropareaControl = false;
var sourceFile = false;
var fileData = false;
var searchData = false;

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
        'values': ['firstname', 'vorname', 'prenom']
    }
);
autoMatches.push(
    {
        'type': 'last_name',
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
        'type': 'patient_id',
        'used': false,
        'values': ['patientid', 'patient']
    }
);

autoMatches.push(
    {
        'type': 'full_name',
        'used': false,
        'values': ['ganzer name', 'patientenname']
    }
);

/* ================================================================================
    Generic Helper Functions
================================================================================ */
function CheckBrowserSupport(fileControl) {
    if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
        alert('File API not supported by browser!')
        return false;
    }
    return true;
}

function CreateTable(data, amount) {
    if (!amount || amount < 0) {
        amount = data.length;
    }

    var table = document.createElement('table');
    table.className = "table-responsive table-bordered";
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

function Reset() {
    sourceFile = false;
    previewControl.html('');
    rowHeaderControl.closest('.firstRowIsHeader').hide();
    console.clear();
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
    var extension = GetFileExtension(sourceFile.name);
    var result = false;
    switch (extension) {
        case 'csv':
        case 'xls':
        case 'xlsx':
            parseControl.prop('disabled', false);
            rowHeaderControl.closest('.firstRowIsHeader').show();
            fileControl.parent('form').removeClass('invalid');
            result = true;
            break;
        default:
            parseControl.prop('disabled', true);
            rowHeaderControl.closest('.firstRowIsHeader').hide();
            fileControl.parent('form').addClass('invalid');
            break;
    }
    return result;
}

/* Get File content (header + content) based on file extension */
function GetFileContent(callback) {
    var extension = GetFileExtension(sourceFile.name);

    if (CheckBrowserSupport()) {
        var file = sourceFile.nativeFile;
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
    fileData = data;
}

/* Prepare Content for next step */
function PrepareFileContent() {
    SplitData();
    DetectBirthdate();
    PrepareDefaults();
    fillBoxes();
    //console.log(JSON.stringify(fileData, 2, 2));
}

/* fill markup of boxes for structure recognition */
function fillBoxes() {
    var parent = $('.step-2 .data-list');
    var box = parent.find('.data-template > div');

    $.each(fileData['header'], function(key, value) {
        var tempBox = box.clone(true);
        tempBox.addClass("box box-" + key).removeClass('data-template');
        tempBox.data('id', key);

        tempBox.find('[data-tmpl="header"]').html(value.title);
        tempBox.find('[data-tmpl="sampledata"]').html(value.sampledata);

        if (value.selected) {
            tempBox.find('[data-tmpl="select"]').val(value.selected);
            tempBox.find('.card-header').removeClass('has-warning').addClass('has-success');
        }

        tempBox.appendTo(parent);
    });

    // bind change event to all boxes
    $(window).on('change', box, function(event) {
        changeSelectedData(event.target);
    });

    goToStep(2);
    return;
}

/* change selected values */
function changeSelectedData(select) {
    // change views
    var $select = $(select);
    var box = $(select).closest('.box');
    var selectedValue = $select.val();

    $('.data-list .box select').each(function() {
        if ($(this).val() != "" && $(this).val() == selectedValue) {
            $(this).val("");
            $(this).closest('.card-header').removeClass('has-success').addClass('has-warning');
        }
    });
    $select.val(selectedValue);
    console.log(box);
    box.find('.card-header').removeClass('has-warning').addClass('has-success')

    //change data in array
    $.each(fileData['header'], function (key, value) {
        if (value['selected'] && value['selected'] == selectedValue) {
            value['selected'] = "";
        }
        if (key == box.data('id')) {
            value['selected'] = selectedValue;
        }
    });

    console.log(JSON.stringify(fileData, 2, 2));
    return;
}

/* prepare data to send */
function FinalizeData() {
    var result = [];

    // prefill empty data array
    $.each(fileData['content'], function (key, value) {
        result.push({
            'full_name': '',
            'birthdate': '',
            'patient_id': ''
        })
    });

    // fill data array based on selected cols
    $.each(fileData['header'], function (key, value) {
        if (value['selected']) {
            switch (value['selected']) {
                case 'firstname':
                    $.each(fileData['content'], function (subkey, subvalue) {
                        result[subkey]['full_name'] = subvalue[key] + result[subkey]['full_name'];
                    });
                    break;
                case 'lastname':
                    $.each(fileData['content'], function (subkey, subvalue) {
                        result[subkey]['full_name'] = result[subkey]['full_name'] + subvalue[key];
                    });
                    break;
                case 'full_name':
                    $.each(fileData['content'], function (subkey, subvalue) {
                        result[subkey]['full_name'] = subvalue[key];
                    });

                    break;
                case 'birthdate':
                    $.each(fileData['content'], function (subkey, subvalue) {
                        $.each(birthdayFormats, function (key, value) {
                            var parsedDate = moment(subvalue[key], value, true);
                            if (parsedDate.isValid()) {
                                result[subkey]['birthdate'] = parsedDate.format('DD.MM.YYYY');
                            }
                        });
                    });

                    break;
                case 'patient_id':
                    $.each(fileData['content'], function (subkey, subvalue) {
                        result[subkey]['patient_id'] = subvalue[key];
                    });

                    break;
            }

        }
    });

    result = { patients: result };
    fileData = result;
}

/* Prepare default dropdown values */
function PrepareDefaults() {
    var birthdateUsed = false;
    $.each(fileData['header'], function (key, value) {
        if (value['autoMatchType']) {
            fileData['header'][key]['selected'] = value['autoMatchType'];
            if (value['autoMatchType'] == 'birthdate') {
                birthdateUsed = true;
            }
        }
        fileData['header'][key]['sampledata'] = fileData['header'][key]['sampledata'].join(',');
    });

    if (!birthdateUsed) {
        $.each(fileData['header'], function (key, value) {
            if (value['possibleBirthdate']) {
                fileData['header'][key]['selected'] = 'birthdate';
                return false;
            }
        });
    }
}

/* auto detect birthdate based on values */
function DetectBirthdate() {
    if (fileData['content'].length > 0) {
        var firstDataLine = fileData['content'][0];

        for (var i = 0; i < firstDataLine.length; i++) {
            $.each(birthdayFormats, function (key, value) {
                var parsedDate = moment(firstDataLine[i], value, true);
                if (parsedDate.isValid()) {
                    fileData['header'][i]['possibleBirthdate'] = true;
                }
            });
        }
    }
}

/* prepare data for manipulation */
function SplitData() {
    var result = { 'header': [], 'content': [] };
    var maxColSize = 0;

    for (var i = 0; i < fileData.length; i++) {
        if (rowHeaderControl.is(':checked') && i == 0) {
            var headerData = [];
            for (var j = 0; j < fileData[i].length; j++) {
                var headerItem = {};
                var title = fileData[i][j];
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
            if (fileData[i].length > maxColSize) {
                maxColSize = fileData[i].length;
            }
            result['content'].push(fileData[i]);
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

    fileData = result;
}

/* ================================================================================
    Main
================================================================================ */

$(function () {
    /* define controls */
    fileControl = $('#uploadFile');
    parseControl = $('#btnParse');
    resetControl = $('.step-1 [data-reset], [data-dismiss="modal"]');
    rowHeaderControl = $('#firstRowIsHeader');
    previewControl = $('#filePreview');
    dropareaControl = $('#droparea');

    /* init file upload & file content recognition */
    parseControl.prop('disabled', true);
    rowHeaderControl.closest('.firstRowIsHeader').hide();

    rowHeaderControl.on('change', function () {
        if (CheckFile()) {
            GetFileContent(PreviewFileContent);
        };
    })

    parseControl.on('click', function () {
        GetFileContent(PrepareFileContent);
    });

    resetControl.on('click', function () {
        Reset();
    });

    dropareaControl.on('click', function () {
        $(this).find('input [type=file]').click();
    });

    var zone = new FileDrop($(dropareaControl)[0])
    zone.event('send', function (files) {
        files.each(function (file) {
            sourceFile = file;

            if (CheckFile()) {
                GetFileContent(PreviewFileContent);
                console.log(fileData);
            };
        })

    })

    /* init structure  */
    

    // sendControl.on('click', function() {
    //     FinalizeData();
    // })
});


/* ================================================================================
    Progress Step Helper
================================================================================ */

/* show/hide loading button */
function toggleLoader(nextStep) {
    // var loaderBtn = $('.btn.step-' + (nextStep-1));

    // if (loaderBtn.hasClass('loading')) {
    //     loaderBtn.removeClass('loading');
    //     loaderBtn.prop("disabled", false);
    // } else {
    //     loaderBtn.addClass('loading');
    //     loaderBtn.prop("disabled", true);
    // }
}

/* goes to a specific step */
function goToStep(nextStep) {

    $('#fileupload').trigger('next.m.' + nextStep);
    //toggleLoader(nextStep);
}


function searchPatients(data) {
    $.ajax({
        type: "POST",
        url: "query_patients",
        data: JSON.stringify(data),
        success: prepareOutputData,
        contentType: 'application/json',
        dataType: 'json'
    });
}