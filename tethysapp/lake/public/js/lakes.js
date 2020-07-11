
let lake_name;

$(function() { //wait for page to load
    $("#select-lake").change(function(){
      lake_name = $("#select-lake option:selected").text();
      get_lake(lake_name);
    });
});

function get_lake (lake_name){
  console.log(lake_name);
  $.ajax({
    url:'lake/lakes/get_lake',
    type:'GET',
    data: {'lake_name':lake_name},
    error: function (xhr, status, error) {
      var err = JSON.parse(xhr.responseText);
      console.log(err.Message);
    },
    success: function (data) {
      if  (!data.error) {
        console.log('Si se pudo enviar el dato del nombre del lago. ', lake_name);
      } else if (data.error) {
        console.log('Un error desconocido ocurrio enviando el nombre del lago');
      } else {
        console.log('Un error inexplicable ocurrio enviando el nombre del lago');
      }
    }
   });
};
