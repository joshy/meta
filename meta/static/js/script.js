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
});
