d3.json("../JSONcopies/file3.json").then(function(data){
    var data2 = JSON.parse(data) 
    console.log(data2)
    console.log(data2.yelp_stars)

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
    // console.log(onestar)
    // console.log(twostar)
    // console.log(threestar)
    // console.log(fourstar)
    // console.log(fivestar)

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


    var chart = new Chart('chart', {
        type: "doughnut",
        options:{
            responsive:true,
            maintainAspectRatio: true,
            legend:{
                display: true
            },
            title: {
                display: true,
                text: "Pie Chart by rating",
                fontSize: 20
            }
        },
        data: {
            
            labels: ["One Star", "Two Star", "Three Star", "Four Star", "Five Star"],
            datasets:[
                {
                    label: "Yelp Ratings",
                    data: star_together,
                    backgroundColor: [getRandomColor(),getRandomColor(),getRandomColor(),getRandomColor(),getRandomColor()]
                },

            ]
        }
    });
})


// https://www.createwithdata.com/chartjs-and-csv/

