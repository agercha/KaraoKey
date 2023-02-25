
const MONTHS = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December'
];

function months(config) {
  var cfg = config || {};
  var count = cfg.count || 12;
  var section = cfg.section;
  var values = [];
  var i, value;

  for (i = 0; i < count; ++i) {
    value = MONTHS[Math.ceil(i) % 12];
    values.push(value.substring(0, section));
  }

  return values;
}


window.onload =  function() {
  const ctx = document.getElementById('myChart');
  
  
  const labels = months({count: 7});
  const data = {
    labels: labels,
    datasets: [{
      label: 'Dummy Dataset',
      data: [3.6, 8.51, 9.38, 6.66, 1.1, 2, 6.5],
      fill: true,
      borderColor: 'white',
      tension: 0,
      gridline
    }]
  };
  
  const config = {
    type: 'line',
    data: data,
  };
  
  new Chart(ctx, config);
}
