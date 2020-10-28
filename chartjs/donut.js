d3.json("../JSONcopies/file3.json").then(function(data){
    var data2 = JSON.parse(data) 
    console.log(data2)
    console.log(data2.yelp_stars)

    onestar = []
    twostar = []
    threestar = []
    fourstar = []
    fivestar = []

    for (var i = 0; data2.yelp_stars.length; i++){
        if (i == 1){
            onestar.push(i);
        } 
        else if (i == 2){
            twostar.push(i);
        }
        else if (i == 3){
            threestar.push(i);
        }
        else if (i == 4){
            fourstar.push(i);
        }
        else {
            fivestar.push(i);
        }
    }
    console.log(onestar)
    console.log(twostar)
    console.log(threestar)
    console.log(fourstar)
    console.log(fivestar)
})


// https://www.createwithdata.com/chartjs-and-csv/

