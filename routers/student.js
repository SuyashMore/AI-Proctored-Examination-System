const express = require("express");
var request = require('request');
const router = express.Router();
var crypto = require('crypto');

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

  let inputEmail = req.body.email;
  let inputPassword = req.body.password;
  inputPassword = crypto.createHash('md5').update(inputPassword).digest('hex');
    

    console.log(inputEmail);
    console.log(inputPassword);
    const options = {
        url: 'http://127.0.0.1:300/' + 'verifyStudent',
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

        res.render("studentHome", {
          email: req.body.email
        });

    });

    //suyash.21.more@gmail.com
    //pass1
 
  
  
});

router.get("/tp", (req, res) => {
  res.render("tp");
});

router.post("/register", (req, res) => {
  let found = false;

  let inputEmail = req.body.email;
  let inputName = req.body.name;
  let inputPassword = req.body.password;
  inputPassword = crypto.createHash('md5').update(inputPassword).digest('hex');
  let inputImage = req.body.photo;

  console.log(inputEmail);
  console.log(inputName);
  console.log(inputPassword);
  console.log(inputImage);

  const options = {
    url: 'http://127.0.0.1:300/' + 'addStudent',
    json: true,
    body: {
      'name': inputName,  
      'email': inputEmail,
      'password': inputPassword,
      'photo_url': inputImage
    }
};

request.post(options, (err, resp, body) => {
    if (err) {
        return console.log(err);
    }
    console.log(body);
});

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
   const options = {
    url: 'http://127.0.0.1:100/' + 'getAllTest'
  };

  request.post(options, (err, resp, body) => {
      if (err) {
          return console.log(err);
      }
      console.log("Database Data Retrived:")
      body = JSON.parse(body);
      console.log(body);
      console.log(body.length);

      for(let i=0;i<body.length;i++){
          
          console.log(body[i]['test_id']);
          console.log("--------------------------");
      }
      tests = body;
      console.log("Tests Before!:")
      console.log(tests)
      res.render("showAllTestsToStudent", {
        tests,
        email: "test@test.com"
      });
  });


  
});

// Give Test
router.post("/takeTest", (req, res) => {
  console.log("Avail Tests")
  console.log(tests)
  let testID = req.body.testID;
  let test = {};
  for(let i=0;i<tests.length;i++){
    if(tests[i].test_details.id === testID){
      test = tests[i].test_details;
      break;
    }
  }
  // let test = tests[ind].test_details;

  // console.log("Test ID Requested:");
  // console.log(req.body.testID);
  // for (let i = 0; i < tests.length; i++) {
  //   if (parseInt(tests[i].id) === parseInt(req.body.testID)) {
  //     test = tests[i];
  //     break;
  //   }
  // }
  // console.log("All Tests:")
  // console.log(tests)
  // console.log("Test is:")
  console.log(test)
  console.log(JSON.stringify(test));
  res.render("takeTestByStudent", {
    test,
    email: req.body.email
  });
  
});

// Route for accepting test responses from students
router.post('/submitTest', (req, res) => {
  // let test = null;
  // for (let i = 0; i < tests.length; i++) {
  //   if (tests[i].id === req.body.testID) {
  //     test = tests[i];
  //     break;
  //   }
  // }

  let test = tests[0].test_details;
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
  console.log("Response of Student")
  console.log(responseOfStudent);


  const options = {
    url: 'http://127.0.0.1:200/' + 'scoreAndStore',
    json: true,
    body: {
      'response': {
        "testID" : responseOfStudent.testID,
        "studentEmail" : responseOfStudent.studentEmail,
        "qna" :responseOfStudent.qna
      }
    }
};

request.post(options, (err, resp, body) => {
    if (err) {
        return console.log(err);
    }
    console.log(body);
    res.render("showAllTestsToStudent", {
      tests,
      email:responseOfStudent.studentEmail
    });
});


})

module.exports = router;
