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

  var getCheckedData = function() {
    return $('input:checked[name=series]')
      .map(function() {
        var study_id = $(this).attr('data-study-id');
        var series_id =  $(this).attr('data-series-id');
        result = { "study_id" : study_id, "series_id" : series_id};
        return result;
       })
      .get();
  };

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
    dirName = $('#download-dir').val();
    if (!dirName) {
      setError();
      return
    } else {
      clearError();
    }
    var checkedData = getCheckedData();
    var data = {
     'data':  checkedData,
     'dir' : dirName
    }

    $.ajax({
      type: 'POST',
      url: 'download',
      data: JSON.stringify(data),
      dataType: 'application/json',
      success: function() { console.log('successfully posted')}
    });
  });

  setError = function() {
    $('#download-form').addClass('has-danger');
    $('#download-error-text').text('Please enter a directory name');
    $('input[name=download-dir]').addClass("form-control-danger");
  }

  clearError = function() {
    $('#download-form').removeClass('has-danger');
    $('#download-error-text').text('');
    $('input[name=download-dir]').removeClass("form-control-danger");
  }

  $('#select-all').on('click', function(e) {
    $("input:checkbox").prop('checked', $(this).prop("checked"));
  });

  $('li.list-group-item a').on('click', function(e) {
    $(e.target).find('span').toggleClass('oi-chevron-right oi-chevron-top')
  });
});
