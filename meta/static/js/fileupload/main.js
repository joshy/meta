/* ================================================================================

	Search Patients with File upload process
	Created by J. Odermatt, Y. Hasler (IP-517bb, 2017)

================================================================================ */



/* ================================================================================
	Initialize options
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
var matchesClosest = false;
var matchesNotfound = false;
var matchesFinal = false;

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
		'values': ['first_name', 'firstname', 'first name', 'vorname', 'prénom', 'prenome']
	}
);
autoMatches.push(
	{
		'type': 'last_name',
		'used': false,
		'values': ['last_name', 'lastname', 'last name', 'nachname', 'nom de famille', 'cognome']
	}
);
autoMatches.push(
	{
		'type': 'birthdate',
		'used': false,
		'values': ['birthdate', 'geburtsdatum', 'date de naissance', 'data di nascita']
	}
);

autoMatches.push(
	{
		'type': 'patient_id',
		'used': false,
		'values': ['patient_id', 'patient_number', 'patient_nr', 'patient id', 'patienten id', 'patienten nummer', 'paziente id']
	}
);

autoMatches.push(
	{
		'type': 'full_name',
		'used': false,
		'values': ['full_name', 'full name', 'vollständiger name', 'ganzer name', 'name', 'nom', 'nom complet', 'nome', 'nome completo']
	}
);

/* ================================================================================
	Generic Helper Functions
================================================================================ */

/* checking compatibility of browser */
function CheckBrowserSupport(fileControl) {
	if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
		alert('File API not supported by browser!')
		return false;
	}
	return true;
}

/* generate preview of uploaded data */
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

/* reset upload */
function Reset() {
	sourceFile = false;
	previewControl.html('');
	rowHeaderControl.closest('.firstRowIsHeader').hide();
	fileData = false;
	console.clear();
}

/* show a message inside step */
function showMessage(step, message, status) {
	var actionEl = $('.step-'+step+' .text-action');
	actionEl.removeClass('text-danger text-warning text-success text-info');

	status = (status == '' ? 'info' : status);
	actionEl.addClass('text-'+status);
	actionEl.html(message);

	if (status == "danger") {
		$('#fileupload').animate({
			scrollTop: $(actionEl).offset().top
		}, 300);
	}
	deactivateAllLoader();
}

/* ================================================================================
	Progress Step Helper
================================================================================ */

/* show/hide loading button */
function activateLoader(step) {
	deactivateAllLoader();

	var loaderBtn = $('.m-next .btn.step-' + (step));
	loaderBtn.addClass('loading');
	loaderBtn.prop("disabled", true);
	
}

/* deactivate loader */
function deactivateAllLoader() {
	$('.m-next .btn.step').removeClass('loading');
	$('.m-next .btn.step').prop('disabled', false);
}

/* go to a specific step */
function goToStep(nextStep) {
	$('#fileupload').trigger('next.m.' + nextStep);
	deactivateAllLoader();
}

/* ================================================================================
	File Helper Functions
================================================================================ */

/* Get File Extension based on filename */
function GetFileExtension(fileName) {
	if (fileName) {
		var extension = fileName.replace(/^.*\./, '');

		if (extension == fileName) {
			extension = '';
		} else {
			extension = extension.toLowerCase();
		}
		return extension;
	}
	return false;    
}

/* Get file if correct extension */
function CheckFile() {
	var result = false;
			
	if (sourceFile) {
		var extension = GetFileExtension(sourceFile.name);
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
	fillStructureBoxes();
}

/* change selected values */
function finalizeClosestMatches(radio) {
	var $radio = $(radio);
	var card = $radio.closest('.card');
	var selectedValue = $radio.val();

	//change data in array
	$.each(matchesClosest, function(key, value) {
		if (selectedValue == "") {
			matchesFinal.pop(value.closest[selectedValue]);
		} else {
			if (value.patient_key == card.data('id')) {
				matchesFinal.push(value.closest[selectedValue])
			}
		}
	});

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

	searchPatients();
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
		for (var i = 0; i <= maxColSize; i++) {
			result['header'].push({ title: '', sampledata: [], noHeaderProvided: true });
		}
	}

	var maxSampleData = 4;
	if (result['content'].length < maxSampleData) {
		maxSampleData = result['content'].length;
	}
	
	for (var x = 0; x < result['header'].length; x++) {
		for (var y = 0; y < maxSampleData; y++) {            
			var currentSample = result['content'][y][x];
			result['header'][x]['sampledata'].push(currentSample);
		}
	}

	fileData = result;
}

/* ================================================================================
	DOM Manipulations
================================================================================ */

/* fill markup of boxes for structure recognition */
function fillStructureBoxes() {
	var parent = $('.step-2 .data-list');
	var box = parent.find('> .data-template > div');
	parent.find('> .box').remove();

	$.each(fileData['header'], function(key, value) {
		var tempBox = box.clone(true); // clone(true) binds data and events
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

	checkStructureMinimum();

	goToStep(2);
	return;
}

/* fills markup of not founded patients with data */
function fillNotFoundMatches() {
	var parent = $('.step-3 .patient-list');
	var card = parent.find('> .data-template > div');
	parent.find('> .card').remove();

	$.each(matchesNotfound, function(key, value) {
		var tempCard = card.clone();
		tempCard.addClass("card-" + key).removeClass('data-template');
		tempCard.attr('data-id', key);

		var content = "";
		content += "Zeile " + (value+1) + ": ";
		content += (fileData['patients'][value]['full_name'] ? fileData['patients'][value]['full_name'] : "");
		content += (fileData['patients'][value]['birthdate'] ? ", " + fileData['patients'][value]['birthdate'] : "");
		content += (fileData['patients'][value]['patient_id'] ? ", " + fileData['patients'][value]['patient_id'] : "");

		tempCard.find('[data-tmpl="patient"]').html(content);

		tempCard.appendTo(parent);
	});

	goToStep(3);
	return;
}

/* fills markup of closest matches with data */
function fillClosestMatches() {
	var parent = $('.step-4 .patient-list');
	var card = parent.find('> .data-template > div');
	var parentRadio = card.find('.card-block');
	var radio = parentRadio.find('.data-template > div');

	parent.find('> .card').remove();

	$.each(matchesClosest, function(key, value) {
		var tempCard = card.clone(true);
		var uniqueId = "card_" + key + "_" +Math.floor((Math.random() * 1000) + 1);
		tempCard.addClass(uniqueId).removeClass('data-template');
		tempCard.attr('data-id', value.patient_key);

		tempCard.find('[data-tmpl="header"]').attr("id", "header-" + uniqueId);
		tempCard.find('[data-tmpl="collapse_body"]').attr("aria-labelledby", "header-" + uniqueId);
		tempCard.find('[data-tmpl="collapse_body"]').attr("id", "body-" + uniqueId);

		var content = "";
		content += "Zeile " + (value.patient_key+1) + ": ";
		content += (fileData['patients'][value.patient_key]['full_name'] ? fileData['patients'][value.patient_key]['full_name'] : "");
		content += (fileData['patients'][value.patient_key]['birthdate'] ? ", " + fileData['patients'][value.patient_key]['birthdate'] : "");
		content += (fileData['patients'][value.patient_key]['patient_id'] ? ", " + fileData['patients'][value.patient_key]['patient_id'] : "");
		
		tempCard.find('[data-tmpl="toggler"]').html(content);
		tempCard.find('[data-tmpl="toggler"]').attr("href", "#body-" + uniqueId);
		tempCard.find('[data-tmpl="toggler"]').attr("aria-controls", "body-" + uniqueId);
		tempCard.find('[data-tmpl="closest_radio_default"]').attr("name", "closestpatient_" + uniqueId);

		tempCard.find('.card-block > .form-check').remove();

		/* radio boxes */
		$.each(value.closest, function(key, value) {
			var tempRadio = radio.clone(true);
			tempRadio.addClass("check-" + uniqueId).removeClass('data-template');
			tempRadio.attr('data-id', key);
			tempRadio.find('[data-tmpl="closest_radio"]').attr("name", "closestpatient_" + uniqueId);
			tempRadio.find('[data-tmpl="closest_radio"]').attr("value", key);

			var content = "";
			content += value.doclist.docs[0].PatientName;
			content += ", " + value.doclist.docs[0].PatientBirthDate;
			content += ", " + value.doclist.docs[0].PatientID;
 
			tempRadio.find('[data-tmpl="closest_patient"]').html(content);            
			tempRadio.appendTo(tempCard.find('.card-block'));
		});
		
		tempCard.appendTo(parent);
	});

	$(window).on('change', radio, function() {
		finalizeClosestMatches(event.target);
	});

	goToStep(4);
	return;
}

/* fills markup of final matches with data */
function fillFinalMatches() {
	var parent = $('.step-5 .patient-list');
	var card = parent.find('> .data-template > div');
	parent.find('> .card').remove();

	$.each(matchesFinal, function(key, value) {
		var tempCard = card.clone(true);
		tempCard.addClass("check-" + key).removeClass('data-template');
		tempCard.attr('data-id', key);

		var patient = value.doclist.docs[0];
		var content = "";
		content += patient.PatientName;
		content += ", " + patient.PatientBirthDate;
		content += ", " + patient.PatientID;
		tempCard.find('[data-tmpl="patient"]').html(content);

		tempCard.find('[data-tmpl="patient_info"]').attr('data-patient-id', patient.PatientID);
		tempCard.find('[data-tmpl="patient_info"]').attr('data-study-id', patient.StudyID);
		tempCard.find('[data-tmpl="patient_info"]').attr('data-series-id', patient.SeriesInstanceUID);
		tempCard.find('[data-tmpl="patient_info"]').attr('data-accession-number', patient.AccessionNumber);
		tempCard.find('[data-tmpl="patient_info"]').attr('data-series-number', patient.SeriesNumber);

		tempCard.appendTo(parent);
	});

	goToStep(5);
	return;
}

/* ================================================================================
	Validation Helper
================================================================================ */

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
	if (selectedValue == "") {
		box.find('.card-header').removeClass('has-success').addClass('has-warning');
	} else {
		box.find('.card-header').removeClass('has-warning').addClass('has-success');
	}

	//change data in array
	$.each(fileData['header'], function (key, value) {
		if (value['selected'] && value['selected'] == selectedValue) {
			value['selected'] = "";
		}
		if (key == box.data('id')) {
			value['selected'] = selectedValue;
		}
	});

	checkStructureMinimum();

	return;
}

/* to show minimum required messages on structure */
function checkStructureMinimum() {
	var minimumReached = false;
	var minimumCounter = 0;
	$.each(fileData['header'], function (key, value) {
		
		if (value['selected'] && value['selected'] == 'patient_id') {
			minimumReached = true;
		}
		if (value['selected'] && value['selected'] == 'full_name') {
			minimumCounter++;
		}
		if (value['selected'] && value['selected'] == 'first_name') {
			minimumCounter++;
		}
		if (value['selected'] && value['selected'] == 'last_name') {
			minimumCounter++;
		}
		if (value['selected'] && value['selected'] == 'birthdate') {
			minimumCounter++;
		}
	});

	if (minimumCounter >= 2) {
		minimumReached = true;
	}

	if (minimumReached) {
		showMessage(2, "Die minimalen Kategorien sind ausgewählt. Sie können nun die Suche starten.", "success");
	} else {
		showMessage(2, "Wählen Sie weitere Kategorien aus, um die Suche zu starten.", "danger");
	}
}

/* ================================================================================
	API Call: Search Patients
================================================================================ */

/* search the patients */
function searchPatients() {
	if (fileData.length == 0) {
		showMessage(2, "Keine Daten für die Suche vorhanden.", "danger");
	}

	$.ajax({
		type: "POST",
		url: "query_patients",
		data: JSON.stringify(fileData),
		success: prepareOutputData,
		error: showSearchError,
		contentType: 'application/json',
		dataType: 'json'
	});
}

function showSearchError(e) {
	console.log("En Error occured", e);
	showMessage(2, "Bei der Übertragung ist ein Fehler aufgetreten.", "danger");
}

/* process and prepare the search results */
function prepareOutputData(data) {
	// init vars
	searchData = data;

	if (searchData.length == 0) {
		showMessage(2, "Keine Daten für die Suche vorhanden.", "danger");
	}

	matchesClosest = [];
	matchesNotfound = [];
	matchesFinal = [];

	// each through searched patients
	$.each(searchData, function(key, value) {
		if (value[0].length != 0 && value[1].length != 0) {
			if (value[0].matches == 0) {
				if (value[1].matches == 0) {
					// no match
					matchesNotfound.push(key);
				} else {
					// closest matches
					matchesClosest.push({ "patient_key": key, "closest": value[1].groups });
				}
			} else {
			// exact match
			matchesFinal.push(value[0].groups[0]);
			}
		}
	});

	// jump over steps if there is nothing to show
	if (matchesFinal.length == 0 && matchesClosest.length == 0) {
		showMessage(2, "Es konnten keine Patienten gefunden werden", "warning");
		return;	
	}

	if (matchesNotfound.length > 0) {
		fillNotFoundMatches();
	} else if (matchesClosest.length > 0) {
		fillClosestMatches();
	} else if (matchesFinal.length > 0) {
		fillFinalMatches();
	} else {
		showMessage(2, "Es konnten keine Patienten gefunden werden", "warning");
	}
}

/* ================================================================================
	Main
================================================================================ */

$(function () {
	/* define controls */
	fileControl = $('#uploadFile');
	parseControl = $('#btnParse');
	searchControl = $('#btnSearch');
	resetControl = $('.step-1 [data-reset], [data-dismiss="modal"]');
	rowHeaderControl = $('#firstRowIsHeader');
	previewControl = $('#filePreview');
	dropareaControl = $('#droparea');

	/* init file upload & file content recognition */
	parseControl.prop('disabled', true);
	rowHeaderControl.closest('.firstRowIsHeader').hide();
	rowHeaderControl.prop('checked', true);

	rowHeaderControl.on('change', function () {
		if (CheckFile()) {
			GetFileContent(PreviewFileContent);
		};
	})

	parseControl.on('click', function () {
		activateLoader(1);
		GetFileContent(PrepareFileContent);
	});

	resetControl.on('click', function () {
        parseControl.prop('disabled', true);
		Reset();
	});

	/* drag&drop upload area */
	dropareaControl.on('click', function () {
		$(this).find('input [type=file]').click();
	});

	var zone = new FileDrop($(dropareaControl)[0], {
		logging: false
	})
	zone.event('send', function (files) {
		files.each(function (file) {
			sourceFile = file;
			if (CheckFile()) {
				GetFileContent(PreviewFileContent);
			};
		})

	})

	/* init structure and search API call  */
	searchControl.on('click', function () {
		activateLoader(2);
		FinalizeData();
	});

	/* show closest matches if found or finalize  */
	$('.m-next .btn.step-3').on('click', function () {
		activateLoader(3);
		if (matchesClosest.length > 0) {
			fillClosestMatches();
		} else {
			fillFinalMatches();
		}
	});

	/* show finale matches  */
	$('.m-next .btn.step-4').on('click', function () {
		activateLoader(4);
		fillFinalMatches();
	});
});