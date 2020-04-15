{% load static %}

requirejs.config({
    'baseUrl': "{% static 'js/leaflet.wms-gh-pages/lib' %}",
    'paths': {
        'leaflet.wms':"{% static 'js/leaflet.wms-gh-pages/dist/leaflet.wms' %}"//.js'
        }
});

define(['leaflet', 'leaflet.wms'],
function(L, wms) {

var overlayMap = createMap('overlay-map', false);
var tiledMap = createMap('tiled-map', true);

function createMap(div, tiled) {
    // Map configuration
    var map = L.map(div);
    map.setView([40.2, -111.8], 11);

    var basemaps = {
        'Basemap': basemap().addTo(map),
        'Blank': blank()
    };

    // Add WMS source/layers
    var source = wms.source(
        'https://geoserver.hydroshare.org/geoserver/HS-3f4baeb41ab140d0b2207bbdcb168ad4/wms',
        {
            "format": "image/png",
            "transparent": "true",
            "tiled": tiled
        }
    );

    var layers = {
        'id_station': source.getLayer("Field3").addTo(map),
      };

    // Create layer control
    L.control.layers(basemaps, layers).addTo(map);

    // Opacity slider
    var slider = L.DomUtil.get('range-' + div);
    L.DomEvent.addListener(slider, 'change', function() {
        source.setOpacity(this.value);
    });
    return map;
}

function basemap() {
    // maps.stamen.com
    var attr = 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.';
    return L.tileLayer("http://tile.stamen.com/toner-background/{z}/{x}/{y}.png", {
        opacity: 0.1,
        attribution: attr
    });
}

function blank() {
    var layer = new L.Layer();
    layer.onAdd = layer.onRemove = function() {};
    return layer;
}

// Export maps for console experimentation
return {
    'maps': {
        'overlay': overlayMap,
        'tiled': tiledMap
    }
};

});
