const express = require("express");
var crypto = require('crypto');
const router = express.Router();
const publicDirPath = require("../public/toGetDir");
var request = require('request');

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
                    ind: tests[i].questions.length + 1
                });
            } else {
                tests[i].questions.push({
                    question: req.body.question,
                    ind: tests[i].questions.length + 1,
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
    test.startTime = req.body.startTime;
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

    let inputEmail = req.body.email;
    let inputPassword = req.body.password;
    inputPassword = crypto.createHash('md5').update(inputPassword).digest('hex');

    console.log(inputEmail);
    console.log(inputPassword);
    const options = {
        url: 'http://127.0.0.1:300/' + 'verifyAdmin',
        json: true,
        body: {
            'email': inputEmail,
            'password': inputPassword
        }
    };

    request.post(options, (err, resp, body) => {
        if (err) {
            return console.log(err);
        }
        console.log(body);
        if (body['verify'] == 'Success') {
            found = 1;
        }

        if (found === -1) {
            res.send("Invalid Email Password Combination");
            return;
        }

        res.redirect("/teacher/home");

    });


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
    let inputEmail = req.body.email;
  let inputName = req.body.name;
  let inputPassword = req.body.password;
  inputPassword = crypto.createHash('md5').update(inputPassword).digest('hex');

  console.log(inputEmail);
  console.log(inputName);
  console.log(inputPassword);

  const options = {
    url: 'http://127.0.0.1:300/' + 'addAdmin',
    json: true,
    body: {
      'name': inputName,  
      'email': inputEmail,
      'password': inputPassword
    }
};

request.post(options, (err, resp, body) => {
    if (err) {
        return console.log(err);
    }
    console.log(body);
});

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

    let testID = req.body.testID;
    let testJSON = test;
    

    const options = {
        url: 'http://127.0.0.1:100/' + 'createTest',
        json: true,
        body: {
          'test_id': testID,  
          'test_details': testJSON,
        }
    };
    
    request.post(options, (err, resp, body) => {
        if (err) {
            return console.log(err);
        }
        console.log(body);
    });
    
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

module.exports = {
    router,
    tests
};