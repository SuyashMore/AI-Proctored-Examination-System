const express = require("express");
const router = express.Router();
const publicDirPath = require("../public/toGetDir");
let tests = require("./teacher").tests;

let studentCred = [];

// resultArr contains objects of responses of students
// in format:
// {
//    testID,
//    student email,
//    [question index(ind), response answer, answer of that index question]
// }
let resultArr = [];

router.get("/login", (req, res) => {
  res.render("studentLogin");
  // res.sendFile(`${publicDirPath}/studentLogin.html`);
});

router.get("/register", (req, res) => {
  res.render("studentRegister");
  // res.sendFile(`${publicDirPath}/studentRegister.html`);
});

router.post("/login", (req, res) => {
  let found = -1;
  for (let i = 0; i < studentCred.length; i++) {
    if (studentCred[i].email === req.body.email) {
      if (studentCred[i].password === req.body.password) found = i;
      else found = -2;
      break;
    }
  }
  if (found === -1) {
    res.send("Entered email is not registered");
    return;
  }
  if (found === -2) {
    res.send("Entered password is incorrect");
    return;
  }
  //   res.redirect(`/student/${studentCred[found].email}`);
  // res.json(studentCred[found]);
  res.render("studentHome", {
    email: req.body.email
  });
});

router.get("/tp", (req, res) => {
  res.render("tp");
});

router.post("/register", (req, res) => {
  let found = false;
  for (let i = 0; i < studentCred.length; i++) {
    if (studentCred[i].email === req.body.email) {
      found = true;
      break;
    }
  }
  if (found) {
    res.send("Entered email is already registered");
    return;
  }
  studentCred.push(req.body);
  console.log(req.body);
  res.redirect("/student/login");
});

router.get("/showStudents", (req, res) => {
  res.json(studentCred);
});

// Student Home
router.get("/home", (req, res) => {
  res.render("studentHome");
});

// Show all tests to student
router.post("/showAllTests", (req, res) => {
  res.render("showAllTestsToStudent", {
    tests,
    email: req.body.email
  });
});

// Give Test
router.post("/takeTest", (req, res) => {
  let test = null;
  for (let i = 0; i < tests.length; i++) {
    if (tests[i].id === req.body.testID) {
      test = tests[i];
      break;
    }
  }
  // console.log(test);
  res.render("takeTestByStudent", {
    test,
    email: req.body.email
  });
});

// Route for accepting test responses from students
router.post('/submitTest', (req, res) => {
  let test = null;
  for (let i = 0; i < tests.length; i++) {
    if (tests[i].id === req.body.testID) {
      test = tests[i];
      break;
    }
  }
  let responseOfStudent = {};
  responseOfStudent.testID = req.body.testID;
  responseOfStudent.studentEmail = req.body.email;
  let qna = [];
  // i for response
  // j for main test.questions array
  for(let i=0;i<test.questions.length;i++){
    let obj = {};
    let pos = (i+1).toString();
    obj.ind = i+1;
    obj.studentAnswer = req.body[pos];
    for(let j=0;j<test.questions.length;j++){
      if(i+1 === test.questions[j].ind){
        if(test.questions[j].op1 !== undefined){
          obj.actualAnswer = test.questions[j].answer;
        }
        else {
          obj.actualAnswer = "This is a sbjective question";
        }
      }
    }
    qna.push(obj);
  }
  responseOfStudent.qna = qna;
  console.log(responseOfStudent);
  console.log(test);
  return;
})

module.exports = router;
