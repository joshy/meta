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
        var patient_id = $(this).attr('data-patient-id');
        var study_id = $(this).attr('data-study-id');
        var series_id =  $(this).attr('data-series-id');
        var accession_number =  $(this).attr('data-accession-number');
        var series_number =  $(this).attr('data-series-number');
        result = {
          "patient_id": patient_id,
          "study_id" : study_id,
          "series_id" : series_id,
          "accession_number" : accession_number,
          "series_number": series_number
        };
        return result;
       })
      .get();
  };

  /**
   * Whenever a user clicks on a facet links the field in the search
   * form get populated by the clicked facet value. The form is then
   * posted to the server. If there is only one facet, this means it is
   * selected and with a click it will remove the facet.
   */
  $('.facet-link').on('click', function(e) {
    input_name = $(this).data('name');
    input_value = $(this).data('value');
    selected = $(this).data('selected');
    if (selected === 'True') {
      $('input[name="' + input_name + '"]').val('')
    } else {
      $('input[name="' + input_name + '"]').val('"' + input_value + '"')
    }
    $('#search-form').submit();
  });

  $('.page-link').on('click', function(e) {
    page = $(this).data('page');
    $('input[name="offset"]').val(page);
    $('#search-form').submit();
  });

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
      dataType: 'json'
    }).done(function(data) {
        console.log(data);
        noty({
          text: 'Successfully added ' + data.series_length + ' series',
          layout: 'centerRight',
          timeout: '3000',
          closeWith: ['click', 'hover'],
          type: 'success'
        });
    }).fail(function(error) {
      console.log(error);
      console.error("Post failed");
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

  $('input[name=select-all-accession-number').on('click', function(e) {
    var table = $(e.target).closest('table')
    $("td input:checkbox", table).prop('checked', $(this).prop("checked"));
  });

  $('input[name=select-all-patient').on('click', function(e) {
    var patientId = $(e.target).attr('data-patient-id');
    var selector = 'table[data-patient-id="' + patientId + '"]'
    $(selector).find('thead tr th input').trigger('click')
  });

  $('input[name=select-all-page').on('click', function(e) {
    $('input[name=select-all-patient]').trigger('click');
  });

  $('li.list-group-item.patients a').on('click', function(e) {
    // parent is in because user can click also on icon
    $(e.target).parent().find('span').first().toggleClass('oi-chevron-left oi-chevron-top')
  });

  /**
   * Pasting the names will escape them automatically. This means that a
   * name like Jon Doe will be become "John\^Doe". In the PACS the whitespace
   * is replace by a '^'. The usecase is that people are coming with lists of
   * names and they don't need to remember how to escape it properly.
   */
  $('#patientname-input').on('paste', function(e) {
    // cancel paste
    e.preventDefault();
    var data = e.originalEvent.clipboardData.getData('Text');
    var names = data.split(/(?:\r\n|\r|\n)/g);
    names = names.map(function(x) { return x.trim(); });
    names = names.filter(function(x) { return x !== '' } );
    names = names.map(function(x) { return x.replace(/\s/g, "\\^"); });
    names = names.map(function(x) { return '"' + x + '"' });
    value = names.join(',');
    $('#patientname-input').val(value);
  });
});
