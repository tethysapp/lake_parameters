let lake_name
let lake_data
let lake_param
let param_bdl
let param_max
let fraction_list
var markers = []

$(function() {
  $("#select-lake").change(function() {
    lake_name = $("#select-lake option:selected").val()
    console.log(lake_name)
    get_lake()
    // lake_parameter()
  })
})

$(function() {
  $("#select-data").change(function() {
    lake_name = document.getElementById('select-lake').value
    lake_data = document.getElementById('select-data').value
    console.log(lake_data)
    lake_parameter()
  })
})

$(function() {
  $("#parameter2").change(function() {
    lake_param = document.getElementById('parameter2').value
    lake_name = document.getElementById('select-lake').value
    console.log(lake_param)
    param_fraction()
  })
})

function searchButton() {
  lake_name = document.getElementById('select-lake').value
  lake_data = document.getElementById('select-data').value
  lake_param = document.getElementById('parameter2').value
  param_fract = document.getElementById('fraction2').value
  param_bdl = document.getElementById('select-bdl').value
  param_max = document.getElementById('select-max').value
  console.log(param_fract)
  console.log(param_bdl)
  console.log(param_max)
  $( "#timeseries_plot" ).empty()
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
      allstations_coords = result["all_coords_stations"]
      allstations = result["all_stations"]
      difcoords = result["dif_coords_stations"]
      set_map()
      $(".loading").remove()
    }
  })
}

function param_fraction() {
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
    url: "/apps/lake/controllers/param_fraction/",
    type: "GET",
    data: { lake_name: lake_name,
            lake_param: lake_param
          },
    error: function(xhr, status, error) {
      var err = JSON.parse(xhr.responseText)
      console.log(err.Message)
      $(".loading").remove()
    },
    success: function(result) {
      console.log("Si se pudo enviar ", lake_param)
      select_fraction = result['fraction']
      $("#fraction2").empty();
      select_fraction['options'].forEach(function(x){
        let newHtml = `<option>${x[0]}</option>`
        $("#fraction2").append(newHtml);
      })
      $("#fraction2").selectpicker("refresh");
      $(".loading").remove()
    }
  })
}

function lake_parameter() {
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
    url: "/apps/lake/controllers/lake_parameter/",
    type: "GET",
    data: { lake_name: lake_name,
            lake_data: lake_data,
          },
    error: function(xhr, status, error) {
      var err = JSON.parse(xhr.responseText)
      console.log(err.Message)
      $(".loading").remove()
    },
    success: function(result) {
      console.log("Si se pudo enviar ", lake_name)
      select_parameter = result['parameter']
      $("#parameter2").empty();
      select_parameter['options'].forEach(function(x){
        let newHtml = `<option>${x[0]}</option>`
        $("#parameter2").append(newHtml);
      })
      $("#parameter2").selectpicker("refresh");
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
            param_fract: param_fract,
            param_max: param_max,
            param_bdl: param_bdl
          },
    error: function(xhr, status, error) {
      var err = JSON.parse(xhr.responseText)
      console.log(err.Message)
      $(".loading").remove()
    },
    success: function(result) {
      console.log("Si se pudo enviar. ", lake_name, lake_data, lake_param, param_fract, param_bdl)
      // console.log(result)
      allstations_coords = result["all_coords_stations"]
      allstations = result["all_data"]
      unit = result['unit']
      characteristic = lake_param
      difcoords = result["dif_coords_stations"]
      alldata = result["all_data"]
      console.log(characteristic)
      console.log(unit)

      set_map()
      $(".loading").remove()
    }
  })
}

function set_map() {
  for (var i = 0; i < markers.length; i++) {
    mymap.removeLayer(markers[i])
  }
  var lat_size = 32/(difcoords[0]+2.75)
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
    var timeseriesCorrectedY=[];
    timeseriesObject['values'].forEach(function(x){
      if(x < 0){
        timeseriesCorrectedY.push(NaN);
      }
      else{
        timeseriesCorrectedY.push(x);
      }
    });

    var station = d.options.station;
    console.log(station);
    var trace = {
      type: "scatter",
      mode: "lines",
      name: station + '<br>Station '.concat(location),
      text: name,
      x: timeseriesObject['dates'],
      y: timeseriesObject['values'],
    }

    var data = [trace];

    var layout = {
      title: param_fract+' '+characteristic,
      showlegend: true,
      legend:{
        xanchor:"center",
        yanchor:"top",
        y:-0.6, // play with it
        x:0.5   // play with it
      },
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
             text: 'value ('+unit+')'},
        // autorange: true,
        // range: [86.8700008333, 138.870004167],
        type: 'linear'
      }

    };
    var config = {responsive: true}

  Plotly.plot('timeseries_plot', data, layout, config);
  }
}
