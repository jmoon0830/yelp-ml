  anychart.onDocumentReady(function() {
    var data = [
      {"x": "Bingo", "value": 3, category: "Positive"},
      {"x": "Night", "value": 2, category: "Negative"},
      {"x": "Party", "value": 1, category: "Neutral"},
      {"x": "PPPrint", "value": 1, category: "Neutral"},
      {"x": "Dalmatian", "value": 3, category: "Positive"},
      {"x": "Daybreak", "value": 2, category: "Negative"},
      {"x": "Citidel", "value": 1, category: "Neutral"},
      {"x": "Bogus", "value": 1, category: "Neutral"}
    ];
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