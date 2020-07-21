let lake_name
let lake_data
let lake_param
let param_bdl
let param_max
var markers = []

$(function() {
  $("#select-lake").change(function() {
    lake_name = $("#select-lake option:selected").val()
    console.log(lake_name)
    get_lake()
  })
})

// $(function() {
//   $("#select-parameter").change(function() {
//     lake_param = $("#select-lake option:selected").val()
//     console.log(lake_param)
//     get_fraction()
//   })
// })

function searchButton() {
  lake_name = document.getElementById('select-lake').value
  lake_data = document.getElementById('select-data').value
  lake_param = document.getElementById('select-parameter').value
  param_bdl = document.getElementById('select-bdl').value
  param_max = document.getElementById('select-max').value
  console.log(lake_name)
  charact_data()
}

function get_lake() {
  var loading = L.control({
      position: 'topleft'
  });

  loading.onAdd = function(mymap) {
      var div = L.DomUtil.create('div', 'info loading');
      div.innerHTML += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src='/static/lake/images/loading.gif'>";
      return div;
  };
  loading.addTo(mymap);

  $.ajax({
    url: "/apps/lake/controllers/get_lake/",
    type: "GET",
    data: { lake_name: lake_name },
    error: function(xhr, status, error) {
      var err = JSON.parse(xhr.responseText)
      console.log(err.Message)
      $(".loading").remove()
    },
    success: function(result) {
      console.log("Si se pudo enviar el dato del nombre del lago. ", lake_name)
      allstations_coords = result["all_coords_stations"]
      allstations = result["all_stations"]
      // difcoords = result["dif_coords_stations"]
      set_map()
      $(".loading").remove()
    }
  })
}

function charact_data() {
  var loading = L.control({
      position: 'topleft'
  });

  loading.onAdd = function(mymap) {
      var div = L.DomUtil.create('div', 'info loading');
      div.innerHTML += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src='/static/lake/images/loading.gif'>";
      return div;
  };
  loading.addTo(mymap);

  $.ajax({
    url: "/apps/lake/controllers/charact_data/",
    type: "GET",
    data: { lake_name: lake_name,
            lake_data: lake_data,
            lake_param: lake_param,
            param_bdl: param_bdl
          },
    error: function(xhr, status, error) {
      var err = JSON.parse(xhr.responseText)
      console.log(err.Message)
      $(".loading").remove()
    },
    success: function(result) {
      console.log("Si se pudo enviar. ", lake_name, lake_data, lake_param, param_bdl)
      // console.log(result)
      allstations_coords = result["all_coords_stations"]
      allstations = result["some_stations"]
      unit = result['unit']
      // difcoords = result["dif_coords_stations"]
      alldataparam = result["all_data"]
      set_map()
      $(".loading").remove()
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

  let iconAwqms2 = L.icon({
    iconUrl: raindrop2ImgUrl,
    iconSize: [15, 15]
  })

  for (var locat in allstations) {
    var location_data = allstations[locat]
    var coords = location_data["coords"]
		var data = location_data['data']
    var loc = location_data["org"]
    var inlake = location_data["type"]
    var station = location_data["station"]
    if (loc == "BYU") {
      var marker = L.marker(coords, { title: locat, custom: data, icon: iconMiller })
        .addTo(mymap).bindPopup(chart)
      markers.push(marker)
    } else if (loc == "UTAHDWQ_WQX") {
      if(inlake == "Lake"){
        var marker = L.marker(coords, { title: locat, custom: data, icon: iconAwqms })
          .addTo(mymap).bindPopup(chart)
        markers.push(marker)
      }
      else{
        var marker = L.marker(coords, { title: locat, custom: data, icon: iconAwqms2 })
          .addTo(mymap).bindPopup(chart)
        markers.push(marker)
      }
    }
  }

  function chart(d) {

    var location = d.options.title;
    var timeseriesObject = d.options.custom;
    var timeseriesCorrectedY=[];
    timeseriesObject['values'].forEach(function(x){
      if(x < 0){
        timeseriesCorrectedY.push(NaN);
      }
      else{
        timeseriesCorrectedY.push(x);
      }
    });

    var unit = d.options.unit;
    console.log(timeseriesObject);
    var trace = {
      x: timeseriesObject['dates'],
      y: timeseriesCorrectedY,
      type: 'bar'
    };
    var data = [trace];
    var layout = {
      title: {
        text:'Station '.concat(location),
        font: {
          family: 'Arial, sans-serif',
          size: 24
        },
        xref: 'paper',
        x: 0.5,
      },
      yaxis: {
        title: {
          text: 'Value '.concat(unit),
          font: {
      family: 'Arial, sans-serif',
      size: 18,
      color: '#7f7f7f'
          }
        }
      }
    };
    Plotly.newPlot('timeseries_plot', data, layout);
  }

}
