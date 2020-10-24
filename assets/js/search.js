var button1 = d3.select("#search_button1")

// user query is saved and sent to python to webscrape and api call
button1.on("click", handleChange)
function handleChange() {
    console.log("click")
    var query = d3.select("#search_bar").property("value");
    console.log(query)

    // python api pulls img url, yelp url, biz info
    var background_url = "https://s3-media0.fl.yelpcdn.com/bphoto/pzorRJoeAbhxGevGcsHSyA/o.jpg"
    var phone_num = "(678) 888-4884"
    var address = "299 Moreland Ave NE"
    var is_closed = false
    var avg_rating = 4.5
    var yelp_first_review = ""
    var yelp_url = ""

    d3.select("#background_img").style("background-image",`url(${background_url})`)
    d3.select("#phone_num").append("p").text(phone_num)
    d3.select("#address").append("p").text(address)
    if (is_closed == false) {
        d3.select("#hours").append("p").text("Open")
    }
    else {
        d3.select("#hours").append("p").text("Closed")
    }
    d3.select("#rating").append("h3").text("Average Rating: " + avg_rating + "/5 Stars")
}

