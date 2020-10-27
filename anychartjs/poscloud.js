d3.json("../JSONcopies/file3.json").then(function(data){
  anychart.onDocumentReady(function() {
    var data2 = JSON.parse(data)
    console.log(data2.positive)
  
    // create a tag (word) cloud chart
    var chart = anychart.tagCloud(data2.positive);
    // set a chart title
    chart.title('Postive Words')
    // set an array of angles at which the words will be laid out
    chart.angles([-45,45])
    // enable color scale
    chart.colorRange().length('80%');
    // display the word cloud chart
    chart.container("container");
    chart.draw();
  })
})