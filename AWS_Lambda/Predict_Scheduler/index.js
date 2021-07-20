'use strict';
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

const invokeLambda = async (name, registers) => {
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

// Format and return array as chunks
const formatRegisters = (registers) => {
  registers = registers.map(register => ({
    cnpj: register.cnpj
  }));
  const chunks = [];
  const chunk = 10;
  for (let i = 0, j = registers.length; i < j; i += chunk) {
    chunks.push(registers.slice(i, i + chunk));
  }
  return chunks;
};

// Scheduler
router.get('/', async function (req, res) {
  try {
    const MongoClient = require('mongodb').MongoClient;
    const uri = '';
    const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

    await client.connect();
    let registers = [];
    let chunkRegisters = [];

    try {
      registers = await client.db('atf_score').collection('feature-collection').find({ dado_valido: true, predicao_modelo1: -1 }).limit(1000).toArray();

      if (registers.length === 0) throw new Error('Sem registros para o modelo 1');

      chunkRegisters = formatRegisters(registers);
      for (const chunkRegister of chunkRegisters) {
        await invokeLambda('py_modelo1_predict', chunkRegister);
      }
    } catch (error) {
      console.log('Error on Model 1 Prediction', error);
    }

    try {
      registers = await client.db('atf_score').collection('feature-collection').find({ dado_valido: true, predicao_modelo3: -1 }).limit(1000).toArray();

      if (registers.length === 0) throw new Error('Sem registros para o modelo 3');

      chunkRegisters = formatRegisters(registers);
      for (const chunkRegister of chunkRegisters) {
        await invokeLambda('py_modelo3_predict', chunkRegister);
      }
    } catch (error) {
      console.log('Error on Model 3 Prediction', error);
    }

    client.close();
    res.json({ success: true });
  } catch (error) {
    console.log(error);
    res.status(404).json({ message: error });
  }
});

app.use('/', router);
