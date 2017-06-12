
# Example data
data = {"patients": [
    {
        "first_name": "Bram",
        "last_name": "L. Munich",
        "birthdate": "24.01.1964"
    },
    {
        "first_name": "Flavio",
        "last_name": "D. Konstanz",
        "birthdate": "09.07.1966"
    }
]}

# Example call to API
$.ajax({
  type: "POST",
  url: "query_patients",
  data: JSON.stringify(data),
  success: function(d) {console.log(d)},
  contentType: 'application/json',
  dataType: 'json'
});
