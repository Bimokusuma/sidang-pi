var record = {
  "score": 0,
  "score_addition":0,
  "score_substraction":0,
  "score_multiplication":0,
  "score_division":0,
  "tracker":[],
  addScore: function (op){
    this["score"]++;
    switch (op) {
      case "+":
        this["score_addition"]++;
        break;
      case "-":
        this["score_substraction"]++;
        break;
      case "*":
        this["score_multiplication"]++;
        break;
      case "/":
        this["score_division"]++;
    }
  }
};

var soalSoal = [];
var soalIndex = 0;

var kuisModal = new bootstrap.Modal(document.getElementById('kuisModal'));

function showSoal(soal){
  var placeholder = document.getElementById('soal');
  placeholder.innerHTML = soal.fullSoal();

  for (i=0;i<4;i++){
    var option = document.getElementById(`option${i}`);
    option.innerHTML = soal.choice[i];
    option.value = soal.choice[i];
  }
}

function pushSoal(n){
  for (i=0;i<n;i++){
    soalSoal.push(createSoal());
  };
}

$(document).ready(function(){

  pushSoal(10);

  $("[id^='option']").click(function(){
    const soal = soalSoal[soalIndex];
    soalIndex++;
    if (soalSoal.length - soalIndex <= 2){ pushSoal(10) }
    if (soal.ans == $(this).val()){
      record.addScore(soal.op)
    } else {
      timePenalty *= timePenaltyGrowth;
      time -= timePenalty;
    }
    showSoal(soalSoal[soalIndex]);
    $("#jumlahSoal").text("Score : "+ record["score"]);
  });

  $('#kuisModal').on('hidden.bs.modal', function () {
    sendRecord(record);
  });
});
