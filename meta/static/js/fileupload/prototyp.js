/* NERF THIS! */

/* Check Browser support */
function CheckBrowserSupport(fileControl) {
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

/* Create JSON from workbook (parse every sheet!) */
function WorkbookToJson(workbook) {
    var result = {};
    workbook.SheetNames.forEach(function (sheetName) {
        var roa = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[sheetName]);
        if (roa.length > 0) {
            result[sheetName] = roa;
        }
    });
    return result;
}

/* Get File content (header + content) based on file extension */
function GetFileContent(fileControl) {
    var extension = GetFileExtension(fileControl.val());

    if (CheckBrowserSupport(fileControl)) {
        var file = fileControl.prop('files')[0];
        var reader = new FileReader();
        var result = false;
        if (extension == 'csv') {
            // get csv data
            reader.readAsText(file);
            reader.onload = function (event) {
                var csv = event.target.result;
                result = $.csv.toArrays(csv);
                NormalizeData(result, extension);
            }
        }
        else if (extension == 'xlsx' || extension == 'xls') {
            // get excel data
            reader.onload = function (e) {
                var data = e.target.result;
                var arr = String.fromCharCode.apply(null, new Uint8Array(data));
                var wb = XLSX.read(btoa(arr), { type: 'base64' });
                result = WorkbookToJson(wb);
                NormalizeData(result, extension);
            };
            reader.readAsArrayBuffer(file);
            
        };        
    };
}

function NormalizeData(data, extension) {
    if (extension == 'csv') {
        // cleanup based on csv import
        $('#fileContent').text(JSON.stringify(data));
        console.log(JSON.stringify(data, 2, 2));
    }
    else if (extension == 'xls' || extension == 'xlsx') {
        // cleanup based on xls import
        $('#fileContent').text(JSON.stringify(data));
        console.log(JSON.stringify(data, 2, 2));
    }
}

/* Get file if correct extension */ 
function CheckFile(fileControl, parseControl) {
    var extension = GetFileExtension(fileControl.val());
    switch (extension) {
        case 'csv':
        case 'xls':
        case 'xlsx':            
            parseControl.show();
            fileControl.parent('form').removeClass('invalid');
            break;
        default:
            parseControl.hide();
            fileControl.parent('form').addClass('invalid');
            break;
    }
}

/* OnLoad */
$(function () {
    var fileControl = $('#uploadFile');
    var parseControl = $('#btnParse');
    parseControl.hide();

    fileControl.on('change', function () {
        $('#fileContent').text('');
        CheckFile(fileControl, parseControl);
    });

    parseControl.on('click', function () {
        GetFileContent(fileControl);
    });
});