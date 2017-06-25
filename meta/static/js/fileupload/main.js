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

	


}


// modal
$(function() {
	prepareOutputData();
})
