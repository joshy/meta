/**
 * Created by Yannick on 12.06.2017
 */


var inputData = {"patients": [ { "first_name": "Bram", "last_name": "L. Munich", "birthdate": "24.01.1964" }, { "first_name": "Flavio", "last_name": "D. Konstanz", "birthdate": "09.07.1966" } ]}
// call to backend
function getData() {
    $.ajax({
        type: "POST",
        url: "query_patients",
        data: JSON.stringify(inputData),
        success: function(d) {
            console.log(d)
        },
        contentType: 'application/json',
        dataType: 'json'
    });
}

// modal
$(function() {
    sendEvent = function(sel, step) {
      $(sel).trigger('next.m.' + step);
    }
})