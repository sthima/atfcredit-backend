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

var invokeLambda = async (name, registers) => {
  return new Promise((resolve, reject) => {
    try {
      const params = {
        FunctionName: name,
        InvocationType: 'RequestResponse'
      };
      let count = 0;

      for (const register of registers) {
        params.Payload = JSON.stringify(register);

        lambda.invoke(params, function (err, data) {
          if (err) {
            console.log(params.FunctionName + ' -Error- ' + err);
          } else {
            console.log(params.FunctionName + ' -Response- ' + data.Payload);
          }
          count++;
          if (count >= registers.length) resolve();
        });
      }
    } catch (error) {
      reject(error);
      console.log(error);
    }
  });
};

// Scheduler
router.get('/', async function (req, res) {
  try {
    const MongoClient = require('mongodb').MongoClient;
    const uri = '';
    const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

    const dateScheduler = moment().format('YYYY-MM-DD');
    console.log('Scheduler date - ' + dateScheduler);

    await client.connect();
    const registers = await client.db('atf_score').collection('initial-collection').find({ insertDate: dateScheduler }).toArray();
    let serasaRegisters = [];
    let vaduRegisters = [];

    console.log('Registers Found - ' + registers.length);
    if (registers && registers.length > 0) {
      // Handle VADU process
      try {
        vaduRegisters = registers.map(register => ({
          cnpj: register.cnpj
        }));

        await invokeLambda('py_vadu', vaduRegisters);
      } catch (error) {
        console.log('Error on VADU Sync', error);
      }

      // Handle SERASA process
      try {
        serasaRegisters = registers.map(register => ({
          text: register.text,
          txt_type: register.txt_type,
          result: register.result
        }));

        await invokeLambda('py_serasa', serasaRegisters);
      } catch (error) {
        console.log('Error on SERASA Sync', error);
      }

      console.log(vaduRegisters);
      client.close();
      res.json({ success: true });
    } else {
      res.status(404).json({ message: 'Nenhum registo encontrado' });
      client.close();
    }
  } catch (error) {
    console.log(error);
    res.status(404).json({ message: error });
  }
});

app.use('/', router);
