var express = require('express');
var app = express();

app.set('port', (process.env.PORT || 5000));

app.use(express.static('/client/views'));

// views is directory for all template files
app.set('views', __dirname + '/client/views');

app.get('/', function(request, response) {
  response.render('views/index');
});

app.listen(app.get('port'), function() {
  console.log('Node app is running on port', app.get('port'));
});