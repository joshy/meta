$(function () {
  console.log("ready!");

  var startDatePicker = $('#start-date-picker').pikaday({
    format: 'DD.MM.YYYY',
    firstDay: 1,
    minDate: new Date(2000, 0, 1),
    maxDate: new Date(),
    yearRange: [2000, 2016]
  });

  var endDatePicker = $('#end-date-picker').pikaday({
    format: 'DD.MM.YYYY',
    firstDay: 1,
    minDate: new Date(2000, 0, 1),
    maxDate: new Date(),
    yearRange: [2000, 2016]
  });

  $('#download-button').on('click', function(e) {
    var data = $('input:checked').map(function() {return $(this).attr('data-id'); }).get().join();
    var jsonData = JSON.stringify(data);
    console.log(jsonData);
    $.ajax({
      type: 'POST',
      url: 'download',
      data: jsonData,
      dataType: 'application/json',
      success: function() { console.log('sucessful posted')}

    })
  })
});
