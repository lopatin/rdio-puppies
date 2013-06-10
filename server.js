var express = require('express'),
	app = express(),
	// pandora = require('./pandora'),
	config = require('./privateconfig'),
	exec = require('child_process').exec;

app.use(express.static(__dirname+'/public'));
app.use(express.bodyParser());

app.listen(8080);

var childProcesses = {};

app.post('/rdio_connect', function (req, res) {
	var id = req.body.clientid;
	var child = exec('python main.py url '+id, function (err, stdout, stderr) {
		console.log(stdout);
		res.send(stdout);
	});
});

app.post('/verify_pin', function (req, res) {
	var id = req.body.clientid,
		pin = req.body.pin;
	var child = exec('python main.py pin '+id+' '+pin, function (err, stdout, stderr) {
		console.log(stdout);
		res.send(stdout);
	});
});

app.post('/lastfm', function (req, res) {
	var id = req.body.clientid,
		username = req.body.username;
	var child = exec('python main.py lastfm '+id+' '+username, function (err, stdout, stderr) {
		console.log(stdout);
		res.send(stdout);
	});
});

// pandora.fetchTracks(config.pandora.username, config.pandora.password, function (result) {
// 	console.log(result);
// });
