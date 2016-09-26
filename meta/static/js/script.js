$(function () {
  console.log("ready!");

  var startDatePicker = $('#start-date-picker').pikaday({
    format: 'DD.MM.YYYY',
    firstDay: 1,
    minDate: new Date(2010, 0, 1),
    maxDate: new Date(),
    yearRange: [2010, 2016]
  });

  var endDatePicker = $('#end-date-picker').pikaday({
    format: 'DD.MM.YYYY',
    firstDay: 1,
    minDate: new Date(2010, 0, 1),
    maxDate: new Date(),
    yearRange: [2010, 2016]
  });

  $('#download-button').on('click', function(e) {
    var data = $('input:checked').map(function() {
      var study_id = $(this).attr('data-study-id');
      var series_id =  $(this).attr('data-series-id');
      result = { "study_id" : study_id, "series_id" : series_id};
      console.log(result);
      return result; })
      .get();
    console.log(data);
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
