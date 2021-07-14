exports.landingPage = function (req, res) {
	res.render("landing-page");
};

exports.homePage = function (req, res) {
	res.send("made it");
};
