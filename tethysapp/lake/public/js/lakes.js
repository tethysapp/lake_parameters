
let lake_name;

$(function() { //wait for page to load
    $("#select-lake").change(function(){
      lake_name = $("#select-lake option:selected").text();
      get_lake(lake_name);
    });
});

function get_lake (lake_name){
  console.log(typeof lake_name);
  $.ajax({
    url:'/apps/lake/controllers/get_lake/',
    type:'GET',
    data: {'lake_name':lake_name},
    datatype:'string',
    error: function (xhr, status, error) {
      var err = JSON.parse(xhr.responseText);
      console.log(err.Message);
    },
    success: function (result) {
      console.log('Si se pudo enviar el dato del nombre del lago. ', lake_name);
      get_lake(result)
    }
   });
};
