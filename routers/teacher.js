const express = require("express");
const router = express.Router();
const publicDirPath = require("../public/toGetDir");

let teacherCred = [];
let tests = [];

router.post("/submitQues", (req, res) => {
  console.log(req.body.question);
  for (let i = 0; i < tests.length; i++) {
    if (tests[i].id === req.body.testID) {
      if (req.body.op1 !== undefined) {
        tests[i].questions.push({
          question: req.body.question,
          op1: req.body.op1,
          op2: req.body.op2,
          op3: req.body.op3,
          op4: req.body.op4,
          answer: req.body.answer,
          ind: tests[i].questions.length+1
        });
      } else {
        tests[i].questions.push({
          question: req.body.question,
          ind: tests[i].questions.length+1,
        });
      }
    }
  }
  res.render("createTest2", {
    testIDfromNode: req.body.testID,
  });
});

router.get("/enterTestID", (req, res) => {
  res.render("enterTestID");
});

router.post("/takeTestID", (req, res) => {
  let test = {};
  test.id = req.body.testID;
  test.testDuration = req.body.testDuration;
  test.warningThreshold = req.body.warningThreshold;
  test.questions = [];
  tests.push(test);
  res.render("createTest2", {
    testIDfromNode: req.body.testID,
  });
});

router.get("/login", (req, res) => {
  res.render("teacherLogin");
  // res.sendFile(`${publicDirPath}/teacherLogin.html`);
});

router.get("/register", (req, res) => {
  res.render("teacherRegister");
  // res.sendFile(`${publicDirPath}/teacherRegister.html`);
});

router.post("/login", (req, res) => {
  let found = -1;
  for (let i = 0; i < teacherCred.length; i++) {
    if (teacherCred[i].email === req.body.email) {
      if (teacherCred[i].password === req.body.password) found = i;
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
  res.redirect("/teacher/home");
  res.json(teacherCred[found]);
});

let questionsOnNode;

router.get("/createTest", (req, res) => {
  res.render("createTest2", {
    questionsOnNode,
  });
  // res.sendFile(`${publicDirPath}/createTest.html`);
});

router.get("/test", (req, res) => {
  res.json(questionsOnNode);
  return;
});

router.post("/register", (req, res) => {
  let found = false;
  for (let i = 0; i < teacherCred.length; i++) {
    if (teacherCred[i].email === req.body.email) {
      found = true;
      break;
    }
  }
  if (found) {
    res.send("Entered email is already registered");
    return;
  }
  teacherCred.push(req.body);
  res.redirect("/teacher/login");
});

router.get("/showTeachers", (req, res) => {
  res.json(teacherCred);
});

// Show test after creation
router.post("/showTestAfterCreation", (req, res) => {
  let test = null;
  for (let i = 0; i < tests.length; i++) {
    if (tests[i].id === req.body.testID) {
      test = tests[i];
      break;
    }
  }
  // console.log(test);
  res.render("showTestAfterCreation", {
    test,
  });
});

// SHow All Tests
router.get("/showAllTests", (req, res) => {
  res.render("showAllTests", {
    tests,
  });
});

// Teacher Home Page
router.get("/home", (req, res) => {
  res.render("teacherHome");
});

module.exports = { router, tests };
