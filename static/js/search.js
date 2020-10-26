var search_params;
var button1 = d3.select("#search_button1")

// user query is saved and sent to python to webscrape and api call
button1.on("click", handleChange)
function handleChange() {
    var input = d3.select("#search_bar").property("value");
    var location = 'atlanta';

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
        console.log(data);
        var pair = data.object[1]
        console.log(pair);
        var pair1 = data.object[1][0];
        var pair2 = data.object[1][1];
        console.log(pair1);
        console.log(pair2);


        var background_url = data.object[0].image_url;
        ///var background_url = data.object[0].image_url
        var phone_num = data.object[0].display_phone;

        console.log(phone_num)
        var address = data.object[0].location.address1
        console.log(address)
        var is_closed = data.object[0].is_closed
        console.log(is_closed)
        var avg_rating = data.object[0].rating
        console.log(avg_rating)
        var yelp_first_review = ""
        var yelp_url = ""

        //part one. see below for further note
        ///it looks like the restaurant name is located in data[0].location.name
        var current_name = "test"

        d3.select("#background_img").style("background-image",`url(${background_url})`)
        ///d3.select("#current_search").append("p").text(current_name)
        d3.select("#phone_num").append("p").text(phone_num)
        d3.select("#address").append("p").text(address)
        ///need code in here to update 'current search: ', probably have to add a class to that h2 line in the html as well
        if (is_closed == false) {
            d3.select("#hours").append("p").text("Open")
        }
        else {
            d3.select("#hours").append("p").text("Closed")
        }
        d3.select("#rating").append("h3").text("Average Rating: " + avg_rating + "/5 Stars")
        
      })

};