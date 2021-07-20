'use strict';

const moment = require('moment');
const axios = require('axios');
const express = require('express');
var app = module.exports = express();
var router = express.Router();
const bodyParser = require('body-parser');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.use(function (req, res, next) {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With, X-API-Key');
  next();
});

// Scheduler
router.get('/', async function (req, res) {
  try {
    const MongoClient = require('mongodb').MongoClient;
    const uri = '';
    const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

    const dateScheduler = moment().subtract(1, 'days').format('YYYY-MM-DD');
    console.log('Scheduler date - ' + dateScheduler);

    const reqObj = {
      method: 'GET',
      timeout: 50000,
      url: 'http://45.7.171.16:8082/netFactor/netFactorWS/alpha/serasa',
      headers: {
        dataInicial: dateScheduler,
        dataFinal: dateScheduler
      }
    };

    const response = await axios(reqObj);
    const registers = response.data;
    let formattedRegisters = [];

    console.log('Registers Found - ' + registers.length);
    if (registers && registers.length > 0) {
      formattedRegisters = registers.map(register => ({
        cnpj: register.SConsCnpjCpf,
        text: register.retLinhaSerasa,
        txt_type: 'PURO',
        result: -1,
        insertDate: moment().format('YYYY-MM-DD')
      }));
      await client.connect();
      const data = await client.db('atf_score').collection('initial-collection').insertMany(formattedRegisters);
      client.close();

      if (data) res.json({ success: true });
      else res.status(404).json({ message: 'Nenhum registo encontrado' });
    } else {
      console.log('Nenhum registro encontrado');
      res.status(404).json({ message: 'Nenhum registro encontrado' });
    }
  } catch (error) {
    console.log(error);
    res.status(404).json({ message: error });
  }
});

app.use('/', router);
