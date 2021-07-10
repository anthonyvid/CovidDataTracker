const express = require("express");
const router = require("./router");

const app = express();

console.log("in App.js");

app.use(express.urlencoded({ extended: false }));
app.use(express.json());
app.use(express.static("public"));

app.set("views", "views");
app.set("view engine", "ejs");

app.use(router);

app.listen(4000, () => {
	console.log("server start on port 4000");
});

module.exports = app;
