anychart.onDocumentReady(function() {
    var data = {
      "data.object[1][0]": {},"data.object[1][1]":{},
    };
    
    Object.keys(data).forEach(function(key) {
      console.table('Key : ' + key + ', Value : ' + data[key])
    })

    // set colors
    var colors = anychart.scales
      .ordinalColor()
      .colors(['#7FFF00', '#DC143C', '#B0C4DE']);
    // create a tag (word) cloud chart
    var chart = anychart.tagCloud(data);
    // set a chart title
    chart.title('Postive vs Negative')
    // set an array of angles at which the words will be laid out
    chart.angles([-45,45])
    // enable color scale
    chart.colorScale(colors);
    // set the color range length
    chart.colorRange().length('80%');
    // display the word cloud chart
    chart.container("container");
    chart.draw();
  });