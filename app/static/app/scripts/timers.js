var x = 0;
var time = 60;
var timePenalty = 2;
var timePenaltyGrowth = 0.1;
var timeForBonusPoint = 2;
function move() {
  if (x == 0) {
    x = 1;
    var elem = document.getElementById("progress-timer");
    var helem = document.getElementById("htimer");
    var id = setInterval(frame, 100);
    function frame() {
      if (time <= 0) {
        clearInterval(id);
        $("#modalMessage").text("Anda berhasil menjawab "+ record["score"] + " soal.");
        kuisModal.show();
        disableButton();
      } else {
        time-= 0.1;
        helem.textContent = "Time : " + time.toFixed(1);
        var width = time/60*100;
        elem.style.width = width + "%";
      }
    }
  }
}
function disableButton(){
  var elems = document.getElementsByTagName('button');
  for (j=0; j<4;j++){
    elems[j].disabled = true;
  }
  $('#choice-group').hide();
  $('#btStart').show();
}

function sendRecord(r){
  $(".record").each(function(){
    const value = r[$(this).attr("name")];
    $(this).val(parseInt(value));
  });
  $("#recordForm").submit(function(){
    $.ajax({
      data: $(this).serialize(),
      type: $(this).attr('method'),
      url: url,
    });
    return false;
  });
  $("#recordForm").submit();
}
