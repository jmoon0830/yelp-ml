var search_params;
var button1 = d3.select("#search_button1")
var profile_img = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_640.png";
d3.select("#pro_pic1").attr("src",profile_img)
d3.select("#pro_pic2").attr("src",profile_img)
d3.select("#pro_pic3").attr("src",profile_img)

// user query is saved and sent to python to webscrape and api call
button1.on("click", handleChange)
function handleChange() {
    $('#loader').show();
    ///code to turn loader on
    var input = d3.select("#search_bar1").property("value");
    var location = d3.select("#search_bar2").property("value");
    search_params = {
        "name" : input,
        "location" : location
    };
    console.log(search_params);

    fetch('/api/home/api_call', {
        method: 'POST',
        body: JSON.stringify(search_params),
        headers: new Headers({
            "content-type": "application/json"
          })
      }).then(function (res) {
          ///console.log(res)
        return res.json()
      }).then((data) => {
        $('#loader').hide();
          ///code that turns loader off
        console.log(data);
        // var pair = data.object[1]
        // console.log(pair);
        // var pair1 = data.object[1][0];
        // var pair2 = data.object[1][1];
        // console.log(pair1);
        // console.log(pair2);
        if (typeof data != "string") {
            var background_url = data["yelp_api"]["image_url"]
            console.log(background_url)
            var auto_name = data["yelp_api"]["name"]
            console.log(auto_name)
            var phone_num = data["yelp_api"]["display_phone"];
            console.log(phone_num)
            var address_p1 = data["yelp_api"]["location"]["display_address"][0];
            var address_p2 = data["yelp_api"]["location"]["display_address"][1];
            console.log(address_p1)
            console.log(address_p2)
            var full_address = address_p1 + address_p2
            console.log(full_address)
            var is_closed = data["yelp_api"]["is_closed"]
            console.log(is_closed)
            var avg_rating = data["yelp_api"]["rating"]
            console.log(avg_rating)
            //part one. see below for further note
            ///it looks like the restaurant name is located in data[0].location.name
            // changes background img
            d3.select("#background_img").style("background-image",`url(${background_url})`)
            // changes current search
            d3.select("#current_search").select("h2").remove()
            d3.select("#current_search").append("h2").text(`Current Search: ${auto_name}`)
            // changes phone number
            d3.select("#phone_num").select("p").remove()
            d3.select("#phone_num").append("p").text(phone_num)
            // changes address
            d3.select("#address").select("p").remove()
            d3.select("#address").append("p").text(`${address_p1} ${address_p2}`)
            // changes open/close
            d3.select("#hours").select("p").remove()
            if (is_closed == false) {
                d3.select("#hours").append("p").text("Open")
            }
            else {
                d3.select("#hours").append("p").text("Closed")
            }
            // changes rating
            d3.select("#rating").select("h3").remove()
            d3.select("#rating").append("h3").text("Average Rating: " + avg_rating + "/5 Stars")
            
            // changes reviewers
            
            var reviewer_img1 = data["review_info"][0]["user"]["image_url"]
            console.log(reviewer_img1)
            var reviewer_name1 = data["review_info"][0]["user"]["name"]
            console.log(reviewer_name1)
            var reviewer_text1 = data["review_info"][0]["text"];
            console.log(reviewer_text1)
            var reviewer_rating1 = data["review_info"][0]["rating"];
            console.log(reviewer_rating1)

            var reviewer_img2 = data["review_info"][1]["user"]["image_url"]
            var reviewer_name2 = data["review_info"][1]["user"]["name"]
            var reviewer_text2 = data["review_info"][1]["text"];
            var reviewer_rating2 = data["review_info"][1]["rating"];

            var reviewer_img3 = data["review_info"][2]["user"]["image_url"]
            var reviewer_name3 = data["review_info"][2]["user"]["name"]
            var reviewer_text3 = data["review_info"][2]["text"];
            var reviewer_rating3 = data["review_info"][2]["rating"];

            var all_reviewer_imgs = [reviewer_img1,reviewer_img2,reviewer_img3];
            var all_reviewer_names = [reviewer_name1,reviewer_name2,reviewer_name3];
            var all_reviewer_text = [reviewer_text1,reviewer_text2,reviewer_text3];
            var all_reviewer_ratings = [reviewer_rating2,reviewer_rating2,reviewer_rating3];
            var testimonials = ["#testimonial1","#testimonial2","#testimonial3"];

            if (all_reviewer_imgs[0] != null) {
                d3.select("#pro_pic1").attr("src",all_reviewer_imgs[0])
            }
            else {
                d3.select("#pro_pic1").attr("src",profile_img)
            }
            if (all_reviewer_imgs[1] != null) {
                d3.select("#pro_pic2").attr("src",all_reviewer_imgs[1])
            }
            else {
                d3.select("#pro_pic2").attr("src",profile_img)
            }
            if (all_reviewer_imgs[2] != null) {
                d3.select("#pro_pic3").attr("src",all_reviewer_imgs[2])
            }
            else {
                d3.select("#pro_pic3").attr("src",profile_img)
            }

            for (var i=0;i<3;i++) {

                d3.select(testimonials[i]).select("h4").remove()
                d3.select(testimonials[i]).append("h4").style("color","white").text(all_reviewer_names[i])

                d3.select(testimonials[i]).select("p").remove()
                d3.select(testimonials[i]).select("p").remove()

                d3.select(testimonials[i]).append("p").attr("class", "description").style("color","white").text(all_reviewer_ratings[i] + "/5")

                d3.select(testimonials[i]).append("p").attr("class", "description").style("color","white").text(all_reviewer_text[i])
            }


        }
        else {
        var message = data;
        // removes all elements
        d3.select("#background_img").style("background-image","")
        d3.select("#current_search").select("h2").remove()
        d3.select("#rating").select("h3").remove()
        d3.select("#hours").select("p").remove()
        d3.select("#address").select("p").remove()
        d3.select("#phone_num").select("p").remove()
        d3.select("#current_search").append("h2").text(message)
        }

        var data2 = data;
        console.log(data2);

        // Create Map, Passing In satelliteMap & earthquakes as Default Layers to Display on Load

        d3.select("#map").remove();
        d3.select("#leaf-map").append("div").attr("id","map").style("width","400px").style("height","500px").style("position","relative").style("outline","none");
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
            accessToken: leaflet_key
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


    fetch('/api/home/ml', {
        method: 'POST',
        body: JSON.stringify(search_params),
        headers: new Headers({
            "content-type": "application/json"
          })
      }).then(function (res) {
          ///console.log(res)
        return res.json()
      }).then((data) => {
          ///code that turns loader off
        var data2 = data;

        onestar = []
        twostar = []
        threestar = []
        fourstar = []
        fivestar = []
    
        for (var i = 0; i < data2.yelp_stars.length; i++){
            if (data2.yelp_stars[i] == 1){
                onestar.push(data2.yelp_stars[i]);
            } 
            else if (data2.yelp_stars[i] == 2){
                twostar.push(data2.yelp_stars[i]);
            }
            else if (data2.yelp_stars[i] == 3){
                threestar.push(data2.yelp_stars[i]);
            }
            else if (data2.yelp_stars[i] == 4){
                fourstar.push(data2.yelp_stars[i]);
            }
            else {
                fivestar.push(data2.yelp_stars[i]);
            }
        }
        console.log(onestar)
        console.log(twostar)
        console.log(threestar)
        console.log(fourstar)
        console.log(fivestar)
    
        star_together = [onestar.length, twostar.length, threestar.length, fourstar.length, fivestar.length]
    
        // generate random ccolor
        function getRandomColor() {
            var letters = '0123456789ABCDEF'.split('');
            var color = '#';
            for (var i = 0; i < 6; i++ ) {
                color += letters[Math.floor(Math.random() * 16)];
            }
            return color;
        }
        
        d3.select("#chart").remove()
        d3.select("#wrapper").append("canvas").attr("id","chart")
        // <canvas id="chart" style="width: 250px; height: 250px; position: relative; outline: none;"></canvas>

        var piechart = new Chart('chart', {
            type: "doughnut",
            options:{
                responsive:true,
                maintainAspectRatio: true,
                aspectRatio:1,
                legend:{
                    display: true
                },
                title: {
                    display: true,
                    text: "Pie Chart by Rating",
                    fontSize: 20
                }
            },
            data: {
                
                labels: ["One Star", "Two Star", "Three Star", "Four Star", "Five Star"],
                datasets:[
                    {
                        label: "Yelp Ratings",
                        data: star_together,
                        backgroundColor: ["darkred","red","orange","lightgreen","green"]
                    },
    
                ]
            }
        });

        d3.select("#neg").remove()
        d3.select("#word_cloud2").append("div").attr("id","neg").style("width","300px").style("height","250px").style("position","relative").style("outline","none");

        anychart.onDocumentReady(function() {
        
            // create a tag (word) cloud chart
            console.log('negative words')
            console.log(data2.negative)
            var negCloud = anychart.tagCloud(data2.negative);
            // set a chart title
            negCloud.title('Negative Words')
            // set an array of angles at which the words will be laid out
            negCloud.angles([-45,45])
            // set the color range length
            negCloud.colorRange().length('80%');
            // display the word cloud chart
            negCloud.container("neg");
            negCloud.draw();
        })

        d3.select("#pos").remove()
        d3.select("#word_cloud1").append("div").attr("id","pos").style("width","300px").style("height","250px").style("position","relative").style("outline","none");
        anychart.onDocumentReady(function() {
          
            // create a tag (word) cloud chart
            var posCloud = anychart.tagCloud(data2.positive);
            // set a chart title
            posCloud.title('Postive Words')
            // set an array of angles at which the words will be laid out
            posCloud.angles([-45,45])
            // enable color scale
            posCloud.colorRange().length('80%');
            // display the word cloud chart
            posCloud.container("pos");
            posCloud.draw();
        })

    })

};