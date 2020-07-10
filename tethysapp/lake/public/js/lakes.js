$(function() { //wait for page to load
    $("#select-lake").change(function(){
      var lake_name = $("#select-lake option:selected").text();
      alert(lake_name);
      $.post("controllers.py",
      {
        lake_name:lake_name
      })


      }
    });

});
