d3.json("../JSONcopies/file3.json").then(function(data){
    anychart.onDocumentReady(function() {
      var data2 = JSON.parse(data)
      console.log(data2.negative)
  
      // create a tag (word) cloud chart
      var chart = anychart.tagCloud(data2.negative);
      // set a chart title
      chart.title('Negative Words')
      // set an array of angles at which the words will be laid out
      chart.angles([-45,45])
      // set the color range length
      chart.colorRange().length('80%');
      // display the word cloud chart
      chart.container("container");
      chart.draw();
    })
  })