/**
 * Created by Yannick on 12.06.2017
 */
var inputData = {"patients": [ { "first_name": "Bram", "last_name": "L. Munich", "birthdate": "24.01.1964" }, { "first_name": "Flavio", "last_name": "D. Konstanz", "birthdate": "09.07.1966" } ]}
var outputData = {"patients": [ [[{"first_name": "ExaktBram", "last_name": "L. Munich", "birthdate": "24.01.1964"}], []], [[{}], [{"first_name": "Closest1Bram", "last_name": "L. Munich", "birthdate": "24.01.1964"}, {"first_name": "Closest2Bram", "last_name": "L. Munich", "birthdate": "24.01.1964"}]], [] ]};
// call to backend
function getData() {
	$.ajax({
		type: "POST",
		url: "query_patients",
		data: JSON.stringify(inputData),
		success: prepareOutputData,
		contentType: 'application/json',
		dataType: 'json'
	});
}

var matchesExact = [];
var matchesClosest = [];
var matchesNotfound = [];

function prepareOutputData(data) {
	data = outputData;

	
	console.log(data);

}

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

// modal
$(function() {
	prepareOutputData();

	sendEvent = function(sel, nextStep) {
		switch(nextStep) {
			case 2:
				// check file validation
				toggleLoader(nextStep);
				$(sel).trigger('next.m.' + nextStep);
				toggleLoader(nextStep);
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
})
