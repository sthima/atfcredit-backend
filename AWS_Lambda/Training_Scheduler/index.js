'use strict';
const moment = require('moment');
const express = require('express');
var app = module.exports = express();
var router = express.Router();
const bodyParser = require('body-parser');
var aws = require('aws-sdk');
const lambda = new aws.Lambda({
  region: 'sa-east-1'
});

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.use(function (req, res, next) {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With, X-API-Key');
  next();
});

var invokeLambda = async (name, payload) => {
  return new Promise((resolve, reject) => {
    try {
      const params = {
        FunctionName: name,
        InvocationType: 'Event',
        Payload: JSON.stringify(payload)
      };
      lambda.invoke(params, function (err, data) {
        if (err) {
          console.log(params.FunctionName + ' -Error- ' + err);
        } else {
          console.log(params.FunctionName + ' -Response- ' + data.Payload);
        }
        resolve();
      });
    } catch (error) {
      reject(error);
      console.log(error);
    }
  });
};

// Scheduler
router.get('/', async function (req, res) {
  try {
    const dateScheduler = moment().format('YYYY-MM-DD');
    console.log('Scheduler date - ' + dateScheduler);

    const MongoClient = require('mongodb').MongoClient;
    const uri = '';
    const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

    await client.connect();
    await client.db('atf_score').collection('initial-collection').updateMany({ dado_valido: true }, { $set: { predicao_modelo1: -1, predicao_modelo3: -1 } });
    console.log('Updated predictions');
    client.close();

    try {
      await invokeLambda('py_modelo1_train', {});
      console.log('Done triggering model 1 training');
    } catch (error) {
      console.log('Error on training model 1', error);
    }

    try {
      await invokeLambda('py_modelo3_train', { epoch: 10 });
      console.log('Done triggering model 3 training');
    } catch (error) {
      console.log('Error on training model 3', error);
    }

    res.json({ success: true });
  } catch (error) {
    console.log(error);
    res.status(404).json({ message: error });
  }
});

app.use('/', router);
