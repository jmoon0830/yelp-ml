var search_params;
var loader;
var button1 = d3.select("#search_button1")

// user query is saved and sent to python to webscrape and api call
button1.on("click", handleChange)
function handleChange() {

    ///code to turn loader on
    

    ///Creating Variables
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
          ///code that turns loader off
          ///loadNow(1);
          
        console.log(data);
 
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


})
function loadNow(opacity) {
    if (opacity <= 0) {
        displayContent();
    } else {
        loader.style.opacity = opacity;
        window.setTimeout(function() {
            loadNow(opacity - 0.05);
        }, 50);
    }
}
function displayContent() {
    loader.style.display = 'none';
    document.getElementById('content').style.display = 'block';
}


document.addEventListener("DOMContentLoaded", function() {
    loader = document.getElementById('loader');
    loadNow(1);
});

};