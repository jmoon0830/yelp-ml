$(function() {
    // Create Map, Passing In satelliteMap & earthquakes as Default Layers to Display on Load
    var myMap = L.map("mapid", {
      center: [39.8283, -98.5795],
      zoom: 4,
    });
  
      // Define variables for our tile layers
      var streetmap = L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
        attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
        tileSize: 512,
        maxZoom: 18,
        zoomOffset: -1,
        id: "mapbox/streets-v11",
        accessToken: API_KEY
      }).addTo(myMap);
  
    const populateFilter = (id, values = [],) => {
      for (var i = 0; i < values.length; i++) {
        $(id).append('<option value="' + values[i] + '">' + values[i] + '</option>');
      }
    };
  
    // Load data from car.csv
    d3.csv("merged_data.csv").then(function(carData) {
  
      // Print the carData
      console.log(carData);
  
      // Creating choose filter
      var make = ["- choose"];
  
      for (var i = 0; i < carData.length; i++){
        var city = [carData[i].lat, carData[i].long]
        L.marker(city).addTo(myMap)
  
  
        if (!make.includes(carData[i].Make)){
          make.push(carData[i].Make)
        }
      }
  
      populateFilter('#make-select', make);
  
  
      $('#make-select').change(function() {
        console.log(this.value);
      });
    });
  });
  