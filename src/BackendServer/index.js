const express = require("express");
const path = require("path");
const expressLayouts = require("express-ejs-layouts");

const app = express();

// Express body parser
app.use(express.urlencoded({ extended: true }));

//EJS
app.use(expressLayouts);
app.set("view engine", "ejs");

// const logger = (req, res, next) => {
//   console.log("logger");
//   next();
// };

// Init middleware
// app.use(logger);

app.get("/api/members", (req, res) => {
  console.log("in api.members");
  res.send("something");
});

// Main route
app.use("/", require("./routers/mainRouter"));

// Teacher Router
app.use("/teacher", require("./routers/teacher").router);

// Student Router
app.use("/student", require("./routers/student"));

// Set static folder
app.use(express.static(path.join(__dirname, "public")));

// app.get("/", (req, res) => {
//   res.sendFile(path.join(__dirname, "public", "index.html"));
// });

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`Server started on ${PORT}`);
});
