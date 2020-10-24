function makeChart(reviews){
    // rating labels in their own array
    var ratinglabels = ratings.map(function(d){
        return d.stars;
    });
    // rating score in its own array
    var ratingsscore = ratings.map(function(d){
        return +d.score;
    });

    // sort by stars
    fivestar = [];
    fourstar = [];
    threestar = [];
    twostar = [];
    onestar = [];


    for(var i =0; i<ratings.length;i++){
        if (ratings[i].stars == "fivestar"){
            fivestar.push(parseInt(ratings[i].stars))
        }
        else if (ratings[i].stars == "fourstar"){
            fourstar.push(parseInt(ratings[i].stars))
        } 
        else if (ratings[i].stars == "threestar"){
            threestar.push(parseInt(ratings[i].stars))
        } 
        else if (ratings[i].stars == "twostar"){
            twostar.push(parseInt(ratings[i].stars))
        } 
        else if (ratings[i].stars == "onestar"){
            onestar.push(parseInt(ratings[i].stars))
        }
       
    }


    // length of star ratings
    var fivestarlength = fivestar.length

    var fourstarlength = fourstar.length;

    var threestarlength = threestar.length;

    var twostarlength = twostar.length;

    var onestarlength = onestar.length;;

    var starlengthtogether = [fivestarlength, fourstarlength, threestarlength, twostarlength, onestarlength];
    
    // generate random ccolor
    function getRandomColor() {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++ ) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    // creating chartjs doughnut chart
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
                text: "Pie Chart by Rating",
                fontSize: 20
            }
        },
        data: {
            
            labels: ["fivestar", "fourstar", "threestar", "twostar", "onestar"],
            datasets:[
                {
                    label: "Restaurant Ratings",
                    data: starlengthtogether,
                    backgroundColor: ('#FFFFFF')
                },

            ]
        }
    });
}





// https://www.createwithdata.com/chartjs-and-csv/

d3.csv("insert_data_here")
.then(makeChart);