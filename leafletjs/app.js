d3.json("../JSONcopies/file3.json").then(function(data){
  var data2 = JSON.parse(data) 
  console.log(data2)

  // Create Map, Passing In satelliteMap & earthquakes as Default Layers to Display on Load
  var myMap = L.map("map", {
    center: [data2.yelp_api.coordinates.latitude, data2.yelp_api.coordinates.longitude],
    zoom: 15,
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

    // Create a new marker
    // Pass in some initial options, and then add it to the map using the addTo method
    var marker = L.marker([data2.yelp_api.coordinates.latitude, data2.yelp_api.coordinates.longitude], {
      draggable: true,
      title: data2.yelp_api.name
    }).addTo(myMap);

    // Binding a pop-up to our marker
    marker.bindPopup(data2.yelp_api.name);


  })

