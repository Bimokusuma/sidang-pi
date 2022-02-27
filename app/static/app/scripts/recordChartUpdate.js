function updateData(chart, labels, data){
  chart.data.labels = labels;
  chart.data.datasets.forEach((dataset) => {
    dataset.data = data;
  });
  chart.update();
}

function getData() {
  $.ajax({
    data: {
      'year': cYear,
      'month': cMonth
    },
    url: "{% url 'get_data' %}",
    success: function(response){
      data_record = response.data;
      label_record = response.label;
      updateData(myLineChart, label_record, data_record);
    },
    error:function(response) {
      console.log(response.responseJSON.errors)
    }
  });
  return false;
};

function viewStatistic(){

}

$(document).ready(function(){
  $("#staticView > a").click(function(){

  });
  $("#month").change(async function(){
    cMonth = Number($(this).children("option:selected").val());
    await getData();
  });

  $("#year").change(async function(){
    cYear = $(this).children("option:selected").val();
    await getData();
  });
});
