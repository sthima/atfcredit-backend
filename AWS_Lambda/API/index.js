'use strict';

const express = require('express');
var app = module.exports = express();
var router = express.Router();
const creditRouter = require('./routes/credit');

const bodyParser = require('body-parser');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// const basicAuth = require('express-basic-auth');

// app.use(basicAuth({
//   users: { atf: 'atf' }
// }));

app.use(function (req, res, next) {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With, X-API-Key');
  next();
});

router.get('/test', function (request, response) {
  response.send('Done');
});

app.use('/', router);
app.use('/credit', creditRouter);
