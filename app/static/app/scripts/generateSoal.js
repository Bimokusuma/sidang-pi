function createSoal(){
  let x1, x2;
  const op = ["+", "-", "/", "*"];
  const opChoice = op[Math.floor(Math.random()*op.length)];

  if (opChoice == "/"){
    x2 = Math.floor((Math.random() * 8) + 2);
    x1 = Math.floor((Math.random() * 8) + 2);
    x1 *= x2;
  } else {
    x1 = Math.floor((Math.random() * 8) + 2);
    x2 = Math.floor((Math.random() * 8) + 2);
  }
  const jwb = eval(`${x1} ${opChoice} ${x2}`);
  if (jwb==0){
    return createSoal();
  } else {
    const soal = {
      n1:x1,
      n2:x2,
      op:opChoice,
      ans: jwb,
      choice: answerChoice(jwb, opChoice, x1,x2),
      fullSoal: function(){return `${this.n1} ${this.op} ${this.n2}`;}
  	};
  	return soal;
  }
}

function shuffleArray(arr) {
  arr.sort(() => Math.random() - 0.5);
}

function answerChoice(number, opCode, x1,x2){
	let answer = [number];
  let num;
  const op = ["+", "-"];
  while(answer.length < 4){
    if (opCode != "*"){
      	num = eval("number"+op[Math.floor(Math.random()*op.length)]+"Math.floor((Math.random() * 3) + 1)");
          if (opCode == "/" && num == 0){ continue; }
      } else {
      	const pr = [eval("number"+op[Math.floor(Math.random()*op.length)]+"Math.floor((Math.random() * 3) + 1)"),
          eval("(x1"+ op[Math.floor(Math.random()*op.length)] + "1)") * x2
          ]
          num = pr[Math.floor(Math.random()*pr.length)];
      }
    if (num === x1 || num === x2){ continue; }
    if (!answer.includes(num)){ answer.push(num); }
  }
  shuffleArray(answer);
  return answer;
}
