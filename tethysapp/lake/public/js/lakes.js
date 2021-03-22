let lake_name
let lake_data
let lake_param
let param_bdl
let param_max
let fraction_list
var characteristic
var markers = []
var plotted = []
var graph_data = []
var count = 0

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
    par.style.display = 'block';
    param_fraction()
  })
})

function downloadButton() {
  lake_name = document.getElementById('select-lake').value
  lake_data = document.getElementById('select-data').value
  lake_param = document.getElementById('parameter2').value
  param_fract = document.getElementById('fraction2').value
  param_bdl = document.getElementById('select-bdl').value
  param_max = document.getElementById('select-max').value
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
      var csvParameter = JSON.parse(result['csvParameter']) // convert to dict
      var header = Object.keys(csvParameter) // grab the columns for header
      console.log(csvParameter)
      var csvData = [];
      csvData.push(header);
      var lines = []
      for (var i = 0; i < header.length; i++){ //data
        var new_col_vals = []
        var new_col_names = Object.keys(csvParameter[header[i]])
        for (var j = 0; j < new_col_names.length; j++){ //data
          new_col_vals.push(csvParameter[header[i]][new_col_names[j]])
        }
        lines.push(new_col_vals)
      }
      lines = lines[0].map((_, colIndex) => lines.map(row => row[colIndex]));
        for (var i = 0; i < lines.length; i++){ //data
        csvData.push(lines[i]);
      }
      var csvFile = csvData.map(e=>e.map(a=>'"'+((a||"").toString().replace(/"/gi,'""'))+'"').join(",")).join("\r\n"); //quote all fields, escape quotes by doubling them.
      var blob = new Blob([csvFile], { type: 'text/csv;charset=utf-8;' });
      var link = document.createElement("a");
      var url = URL.createObjectURL(blob);
      link.setAttribute("href", url);
      link.setAttribute("download", lake_name.replace(/[^a-z0-9_.-]/gi,'_') +"_"+ lake_data.replace(/[^a-z0-9_.-]/gi,'_') +"_"+ param_fract.replace(/[^a-z0-9_.-]/gi,'_') + lake_param.replace(/[^a-z0-9_.-]/gi,'_') + ".csv");
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      $(".loading").remove()
    }
  })
}

function downloadButton2() {
  var loading = L.control({
      position: 'topleft'
  });
  loading.onAdd = function(mymap) {
      var div = L.DomUtil.create('div', 'info loading');
      div.innerHTML += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src='/static/lake/images/loading.gif'>";
      return div;
  };
  loading.addTo(mymap);
  console.log(graph_data);
  var csvGraphic = {};
  const header2 = ['Station','Date','Value','Unit']
  for (var i = 0; i < header2.length; i++){
    csvGraphic[header2[i]]=[]
    for (var j = 0; j < graph_data.length; j++){
      csvGraphic[header2[i]].push(graph_data[j][i]);
    }
    var newArr=[];
    for(var z=0;z<csvGraphic[header2[i]].length; ++z){
      newArr = newArr.concat(csvGraphic[header2[i]][z]);
    }
    csvGraphic[header2[i]]=newArr
    var newArr2={};
    for(var z=0;z<csvGraphic[header2[i]].length; ++z){
      newArr2[z] = csvGraphic[header2[i]][z];
    }
    csvGraphic[header2[i]]=newArr2
   }

  var header = Object.keys(csvGraphic) // grab the columns for header
  console.log(csvGraphic)
  var csvGraph = [];
  csvGraph.push(header);
  var lines = []
  for (var i = 0; i < header.length; i++){ //data
    var new_col_vals = []
    var new_col_names = Object.keys(csvGraphic[header[i]])
    for (var j = 0; j < new_col_names.length; j++){ //data
      new_col_vals.push(csvGraphic[header[i]][new_col_names[j]])
    }
    lines.push(new_col_vals)
  }
  lines = lines[0].map((_, colIndex) => lines.map(row => row[colIndex]));
    for (var i = 0; i < lines.length; i++){ //data
    csvGraph.push(lines[i]);
    csvGraph[i][2] = csvGraph[i][2].toString();
  }

  var csvFile = csvGraph.map(e=>e.map(a=>'"'+((a||"").toString().replace(/"/gi,'""'))+'"').join(",")).join("\r\n"); //quote all fields, escape quotes by doubling them.
  var blob = new Blob([csvFile], { type: 'text/csv;charset=utf-8;' });
  var link = document.createElement("a");
  var url = URL.createObjectURL(blob);
  link.setAttribute("href", url);
  link.setAttribute("download", param_fract.replace(/[^a-z0-9_.-]/gi,'_') + lake_param.replace(/[^a-z0-9_.-]/gi,'_') + "plot.csv");
  link.style.visibility = 'hidden';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
      $(".loading").remove()
}

function searchButton() {
  count = 0
  lake_name = document.getElementById('select-lake').value
  lake_data = document.getElementById('select-data').value
  lake_param = document.getElementById('parameter2').value
  param_fract = document.getElementById('fraction2').value
  param_bdl = document.getElementById('select-bdl').value
  param_max = document.getElementById('select-max').value
  console.log(param_fract)
  console.log(param_bdl)
  console.log(param_max)
  console.log(lake_param)
  plotted = []
  $( "#timeseries_plot" ).empty()
  document.getElementById("char2").innerHTML = 'To create a plot, click on some stations';
  document.getElementById("down2").style.visibility = "visible";
  console.log(timeseries_plot)
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
      let length = select_fraction['options'].length
      console.log(length)
      if(length==1){
        par.style.display = 'none';
      }
      else{
        par.style.display = 'block';
        $("#fraction2").selectpicker("refresh");
      }
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
      console.log("Si se pudo enviar ", lake_name, lake_data, lake_param, param_fract, param_bdl)
      // console.log(result)
      allstations_coords = result["all_coords_stations"]
      allstations = result["all_data"]
      unit = result['unit']
      characteristic = result["characteristic"]
      fraction = result["fraction"]
      difcoords = result["dif_coords_stations"]
      alldata = result["all_data"]
      console.log(alldata)
      document.getElementById("down").style.visibility = "visible";
      document.getElementById("char").innerHTML = fraction + ' ' + characteristic;
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

  let iconBYU = L.icon({
    iconUrl: byu2ImgUrl,
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
    plotted = []
    graph_data = []
    var location_data = allstations[locat]
    var coords = location_data["coords"]
		var data = location_data['data']
    var loc = location_data["org"]
    var inlake = location_data["type"]
    var station = location_data["station"]
    if (loc == "BYU") {
      if(inlake == "Lake"){
        var marker = L.marker(coords, { title: locat, custom: data, icon: iconBYU, station:station})
          .addTo(mymap).bindPopup(chart)
        markers.push(marker)
      }
      else{
      var marker = L.marker(coords, { title: locat, custom: data, icon: iconMiller, station:station})
        .addTo(mymap).bindPopup(chart)
      markers.push(marker)
      }
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
    var station = d.options.station;
    var p = plotted.includes(station)
    console.log(p)

  // add if statement
    if (p == false) {
      plotted.push(station);
      console.log(station);
      console.log(plotted);
      var trace = {
        type: "scatter",
        mode: "lines",
        name: station+ ' ' +location+ '    ',
        text: name,
        x: timeseriesObject['dates'],
        y: timeseriesObject['values'],
      }
      var data = [trace];
      var dd = timeseriesObject['dates'].length
      const stat = [];
      const u = [];
      for (let i=0; i<dd; i++){
        stat[i] = station
        u[i] = unit
      };
      const data_download = [stat,timeseriesObject['dates'],timeseriesObject['values'],u]

      graph_data.push(data_download);
      console.log(graph_data);
      var layout = {
        title: param_fract+' '+characteristic,
        showlegend: true,
        legend:{
          xanchor:"center",
          yanchor:"top",
          font:{
            size:12
          },
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
      if(count>0){
        Plotly.plot('timeseries_plot', data, layout, config);
      }
      if(count==0){
        Plotly.newPlot('timeseries_plot', data, layout, config);
      count = count+1
      }
    }
  }
}
