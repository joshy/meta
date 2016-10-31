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

  var getCheckedData(): function() {
    return $('input:checked[name=series]')
      .map(function() {
        var study_id = $(this).attr('data-study-id');
        var series_id =  $(this).attr('data-series-id');
        result = { "study_id" : study_id, "series_id" : series_id};
        return result;
       })
      .get();
  }

  $('#transfer-button').on('click', function(e) {
    e.preventDefault();
    var data = getCheckedData();
    var jsonData = JSON.stringify(data);
    var target = $("input[type='radio']:checked").val();
    $.ajax({
      type: 'POST',
      url: 'transfer/' + target,
      data: jsonData,
      dataType: 'application/json',
      success: function() { console.log('successfully posted')}
    });
  });

  $('#download-button').on('click', function(e) {
    e.preventDefault();
    var data = getCheckedData();
    var jsonData = JSON.stringify(data);
    $.ajax({
      type: 'POST',
      url: 'download',
      data: jsonData,
      dataType: 'application/json',
      success: function() { console.log('successfully posted')}
    })
  })

  $('#select-all').on('click', function(e) {
    $("input:checkbox").prop('checked', $(this).prop("checked"));
  });
});
