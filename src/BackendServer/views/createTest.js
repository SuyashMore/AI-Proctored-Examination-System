document.getElementById("mcq").addEventListener("click", function () {
  //   document.getElementById("enterquestion").innerHTML = `
  //   `;
  document.getElementById("mcqform").style.display = "block";
  document.getElementById("subform").style.display = "none";
  document.getElementById("displayques").style.display = "none";
});

document.getElementById("subjective").addEventListener("click", function () {
  //   document.getElementById("enterquestion").innerHTML = `
  //   `;
  document.getElementById("subform").style.display = "block";
  document.getElementById("mcqform").style.display = "none";
  document.getElementById("displayques").style.display = "none";
});

let questions = [];
function submitQuestion(type) {
  let question = {};
  question.type = type;
}

document.getElementById("submitmcq").addEventListener("click", function () {
  let question = {};
  question.type = "mcq";
  question.question = document.getElementById("mcqquestion").value;
  question.op1 = document.getElementById("op1").value;
  question.op2 = document.getElementById("op2").value;
  question.op3 = document.getElementById("op3").value;
  question.op4 = document.getElementById("op4").value;
  question.ans = document.getElementById("answer").value;
  //   console.log(question.question);
  questions.push(question);
  document.getElementById("mcqform").style.display = "none";
});

document.getElementById("submitsub").addEventListener("click", function () {
  let question = {};
  question.type = "subjective";
  question.question = document.getElementById("subquestion").value;
  //   console.log(question.question);
  questions.push(question);
  document.getElementById("subform").style.display = "none";
});

function displayQuestionsFunction(check) {
  console.log(questions);
  let questionsArr = ``;
  for (let i = 0; i < questions.length; i++) {
    if (questions[i].type === "mcq") {
      questionsArr += `Question ${i + 1}: <br>`;
      questionsArr += questions[i].question;
      questionsArr += `<br>`;
      questionsArr += `Options: <br>`;
      questionsArr += questions[i].op1;
      questionsArr += `<br>`;
      questionsArr += questions[i].op2;
      questionsArr += `<br>`;
      questionsArr += questions[i].op3;
      questionsArr += `<br>`;
      questionsArr += questions[i].op4;
      questionsArr += `<br>`;
      questionsArr += `Answer: <br>`;
      questionsArr += questions[i].ans;
      questionsArr += `<br>`;
    } else {
      questionsArr += `Question: ${i + 1} <br>`;
      questionsArr += questions[i].question;
      questionsArr += `<br>`;
    }
  }
  document.getElementById("displayques").style.display = "block";
  document.getElementById("displayques").innerHTML = questionsArr;
}

document
  .getElementById("displayquesbtn")
  .addEventListener("click", displayQuestionsFunction);

document
  .getElementById("submittest")
  .addEventListener("click", displayQuestionsFunction("submitTest"));
