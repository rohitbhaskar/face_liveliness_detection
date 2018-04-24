var express = require('express');
var bodyParser = require('body-parser');
var multer = require('multer');
// var upload = multer();
var upload = multer({ dest: 'uploads/' })
var app = express();
var timeout = require('connect-timeout')
var fs = require('fs')
var http = require('http').Server(app);
var io = require('socket.io')(http);

// To run python code
var sys   = require('util')
const spawn = require('child_process').spawn

app.get('/', function(req, res){
   //res.render('form');
});

// app.set('view engine', 'pug');
// app.set('views', './views');

// for parsing application/json
app.use(bodyParser.json()); 

// for parsing application/xwww-
app.use(bodyParser.urlencoded({ extended: true })); 
//form-urlencoded

// for parsing multipart/form-data
// app.use(upload.array()); 
app.use(express.static('public'));

app.post('/', function(req, res){
   console.log(req.body);
   res.send("recieved your request!");
});


app.post('/upload', timeout('100s'), upload.single('video'), haltOnTimedout, function (req, res, next) {
	// debugger;
	if (req.timedout) console.log("--- timed out ---");
	console.log(req.body);
	console.log(req.file);
	res.send("recieved your request!");

	// rename the file saved
	fs.rename('uploads/'+req.file.filename, 'uploads/1.mp4', function(err) {
	    if ( err ) console.log('ERROR: ' + err);
	});

	// Clal python code
	setTimeout(function(){
		const trackIris  = spawn('python', ['Eye_Tracking/EyeTracking.py', 'uploads/1.mp4', req.body.motionType]);
		//Response from python code
		trackIris.stdout.on('data', function(data) {
		    console.log("Finished tracking Iris", data);
		    debugger;
		    io.emit('new message', {"username":"Rohit", "result":1});
		});
	}, 500);

  // req.file is the `avatar` file
  // req.body will hold the text fields, if there were any
})



function haltOnTimedout (req, res, next) {
  if (!req.timedout) next()
}


// Socket io part
io.on('connection', function(socket){
  console.log('a user connected');
  socket.on('disconnect', function(){
    console.log('user disconnected');
  });
});


http.listen(6000, function(){
  console.log('listening on *:6000');
});


app.listen(process.env.PORT || 5000)