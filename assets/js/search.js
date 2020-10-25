var button1 = d3.select("#search_button1")

// user query is saved and sent to python to webscrape and api call
button1.on("click", handleChange)
function handleChange() {
    console.log("click")
    var query = d3.select("#search_bar1").property("value");
    console.log(query)

    // python api pulls img url, yelp url, biz info
    var background_url = "https://s3-media0.fl.yelpcdn.com/bphoto/pzorRJoeAbhxGevGcsHSyA/o.jpg"
    var phone_num = "(678) 888-4884"
    var address = "299 Moreland Ave NE"
    var is_closed = false
    var avg_rating = 4.5
    var yelp_url = ""

    d3.select("#background_img").style("background-image",`url(${background_url})`)
    d3.select("#phone_num").append("p").text(phone_num)
    d3.select("#address").append("p").text(address)
    if (is_closed == false) {
        d3.select("#hours").append("h3").attr("class","card-header").text("Open")
    }
    else {
        d3.select("#hours").append("h3").attr("class","card-header").text("Closed")
    }
    d3.select("#rating").append("h3").text("Average Rating: " + avg_rating + "/5 Stars")
}

var reviewer_img1 = "https://s3-media2.fl.yelpcdn.com/photo/81TY6v8jrz4tLbP5Oj_vgg/o.jpg";
var reviewer_name1 = "Hannah C.";
var reviewer_text1 = "OH MY GOD i think i talk about hattie b's every day. this place is by far the best hot chicken. the hot chicken sandwich with the \"hot\" level is absolutely...";
var reviewer_rating1 = 5;

var reviewer_img2 = "https://s3-media4.fl.yelpcdn.com/photo/AZ91dRaJnhwWt6ARSNVc3A/o.jpg";
var reviewer_name2 = "Daniel B.";
var reviewer_text2 = "Hattie B's Moreland Ave location gets 4.5 stars rounded up to 5 from me. I thought the food here was excellent and better than my last experience at Hattie...";
var reviewer_rating2 = 5;

var all_reviewer_imgs = [reviewer_img1,reviewer_img2];
var all_reviewer_names = [reviewer_name1,reviewer_name2];
var all_review_text = [reviewer_text1,reviewer_text2];
var all_reviewer_ratings = [reviewer_rating2,reviewer_rating2];
var testimonials = ["#testimonial1","#testimonial2"];


d3.select("#person_1").data([0]).enter().append("img").attr("src",reviewer_img1)
console.log(d3.select("#person_1").attr("src"))

for (var i=0;i<2;i++) {
    d3.select(testimonials[i]).append("h4").text(all_reviewer_names[i])
    d3.select(testimonials[i]).append("p").attr("class", "description").text(all_reviewer_ratings[i] + "/5")
    d3.select(testimonials[i]).append("p").attr("class", "description").text(all_review_text[i])
}

// d3.select("#testimonial1").append("h4").text(reviewer_name1)
// d3.select("#testimonial1").append("p").attr("class", "description").text(reviewer_rating1 + "/5")
// d3.select("#testimonial1").append("p").attr("class", "description").text(review_text1)
