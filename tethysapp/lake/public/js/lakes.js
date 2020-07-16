let lake_name

var markers = []

// $(function() {

//   $("#select-lake").change(function() {
//   // $("#search-button").click(function() {
//     lake_name = $("#select-lake option:selected").val()
//     console.log(lake_name)
//     get_lake(lake_name)
//   })
// })
function searchButton() {
  lake_name = document.getElementById('select-lake').value;
  lake_data = document.getElementById('select-data').value;
  lake_param = document.getElementById('select-parameter').value;
  param_bdl = document.getElementById('select-bdl').value;
  param_max = document.getElementById('select-max').value;
  get_lake();
}

function get_lake() {
  $.ajax({
    url: "/apps/lake/controllers/get_lake/",
    type: "GET",
    data: { lake_name: lake_name,
            lake_data: lake_data,
            lake_param: lake_param,
            param_bdl: param_bdl,
            param_max: param_max
          },
    error: function(xhr, status, error) {
      var err = JSON.parse(xhr.responseText)
      console.log(err.Message)
    },
    success: function(result) {
      console.log("Si se pudo enviar el dato del nombre del lago. ", lake_name, lake_data, lake_param, param_bdl, param_max)
      allstations_coords = result["all_coords_stations"]
      allstations = result["all_stations"]
      set_map()
    }
  })
}

function set_map() {
  for (var i = 0; i < markers.length; i++) {
    mymap.removeLayer(markers[i])
  }
  console.log(allstations_coords)
  mymap.setView(allstations_coords, 11)

  let iconMiller = L.icon({
    iconUrl: byuImgUrl,
    iconSize: [15, 12]
  })

  let iconAwqms = L.icon({
    iconUrl: raindropImgUrl,
    iconSize: [15, 15]
  })

  for (var locat in allstations) {
    var location_data = allstations[locat]
    var coords = location_data["coords"]
    var loc = location_data["org"]
    var station = location_data["station"]
    if (loc == "BYU") {
      var marker = L.marker(coords, { title: locat, icon: iconMiller })
        .addTo(mymap)
        .bindPopup(
          "<b>Station: </b>" +
            station +
            "<br>ID: " +
            locat +
            "<br>Coordinates: " +
            coords +
            "<br>Organization: " +
            loc
        )
      markers.push(marker)
    } else if (location_data["org"] == "UTAHDWQ_WQX") {
      var marker = L.marker(coords, { title: locat, icon: iconAwqms })
        .addTo(mymap)
        .bindPopup(
          "<b>Station: </b>" +
            station +
            "<br>ID: " +
            locat +
            "<br>Coordinates: " +
            coords +
            "<br>Organization: " +
            loc
        )
      markers.push(marker)
    }
  }
}
