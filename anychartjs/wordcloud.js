anychart.onDocumentReady(function() {
    var data = [
      {"x": "Bingo", "value": 3, category: "Positive"},
      {"x": "Night", "value": 2, category: "Negative"},
      {"x": "Party", "value": 1, category: "Neutral"}
    ];
  // create a tag (word) cloud chart
    var chart = anychart.tagCloud(data);
  // set a chart title
    chart.title('Five Star vs One Star')
    // set an array of angles at which the words will be laid out
    chart.angles([0])
    // enable a color range
    chart.colorRange(true);
    // set the color range length
    chart.colorRange().length('80%');
  // display the word cloud chart
    chart.container("container");
    chart.draw();
  });