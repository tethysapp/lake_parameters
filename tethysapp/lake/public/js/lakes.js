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
      difcoords = result["dif_coords_stations"]
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
      allstations = result["all_data"]
      unit = result['unit']
      difcoords = result["dif_coords_stations"]
      alldata = result["all_data"]
      set_map()
      $(".loading").remove()
    }
  })
}

function set_map() {
  for (var i = 0; i < markers.length; i++) {
    mymap.removeLayer(markers[i])
  }
  var lat_size = 32/(difcoords[0]+2.65)
  console.log(lat_size)
  mymap.setView(allstations_coords, lat_size)

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
    var unit = unit
    var inlake = location_data["type"]
    var station = location_data["station"]
    if (loc == "BYU") {
      var marker = L.marker(coords, { title: locat, custom: data, icon: iconMiller, station:station})
        .addTo(mymap).bindPopup(chart)
      markers.push(marker)
    } else if (loc == "UTAHDWQ_WQX") {
      if(inlake == "Lake"){
        var marker = L.marker(coords, { title: locat, custom: data, icon: iconAwqms, station:station})
          .addTo(mymap).bindPopup(chart)
        markers.push(marker)
      }
      else{
        var marker = L.marker(coords, { title: locat, custom: data, icon: iconAwqms2, station:station})
          .addTo(mymap).bindPopup(chart)
        markers.push(marker)
      }
    }
  }

  function chart(d) {

    var location = d.options.title;
    var timeseriesObject = d.options.custom;

    var unit = d.options.unit;
    var station = d.options.station;
    console.log(unit);

    var trace = {
      type: "scatter",
      mode: "lines",
      name: 'AAPL High',
      x: timeseriesObject['dates'],
      y: timeseriesObject['values'],
      line: {color: '#17BECF'}
    }

    var data = [trace];

    var layout = {
      title: 'Station '.concat(station),
      xaxis: {
        autorange: true,
        range: ['1989-01-01', '2020-08-01'],
        rangeselector: {buttons: [
            {
              count: 6,
              label: '6m',
              step: 'month',
              stepmode: 'backward'
            },
            {
              count: 12,
              label: '12m',
              step: 'month',
              stepmode: 'backward'
            },
            {step: 'all'}
          ]},
        rangeslider: {range: ['1989-01-01', '2020-08-01']},
        type: 'date'
      },
      yaxis: {
            title: {
              text: 'Value '.concat(unit),
            // autorange: true,
        // range: [86.8700008333, 138.870004167],
        type: 'linear'
      }
  };

  Plotly.newPlot('timeseries_plot', data, layout);
  }
}
