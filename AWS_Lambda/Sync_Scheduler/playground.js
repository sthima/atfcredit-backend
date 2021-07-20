const axios = require('axios');
const moment = require('moment');
const tr = require('moment/locale/hu');

var func = async () => {
  try {
    const MongoClient = require('mongodb').MongoClient;
    const uri = 'mongodb+srv://mongo:mongo@basecluster.hozn3.mongodb.net/test?retryWrites=true&w=majority';
    const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

    await client.connect();
    const data = await client.db('test').collection('initial-collection').insertOne({
      cnpj: '31637711000103',
      txt_path: '31637711000103.txt',
      txt_content: '',
      isProcessed: false,
      insertDate: new Date()
    });

    console.log(data);
    client.close();
  } catch (error) {
    console.log(error);
  }
};

var req = async () => {
  try {
    const MongoClient = require('mongodb').MongoClient;
    const uri = 'mongodb+srv://atfUser:mvOX8tCv5Tv4pvJU@atfcluster.t51do.mongodb.net/atf_score?retryWrites=true&w=majority';
    const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });
    const reqObj = {
      method: 'GET',
      timeout: 50000,
      url: 'http://45.7.171.16:8082/netFactor/netFactorWS/alpha/serasa',
      headers: {
        dataInicial: '2021-07-01',
        dataFinal: '2021-07-09'
      }
    };

    const response = await axios(reqObj);
    const registers = response.data;
    const formattedRegisters = registers.map(register => ({
      cnpj: register.SConsCnpjCpf,
      text: register.retLinhaSerasa,
      txt_type: 'PURO',
      result: -1,
      insertDate: moment().format('YYYY-MM-DD')
    }));
    await client.connect();
    const data = await client.db('atf_score').collection('initial-collection').insertMany(formattedRegisters);
    client.close();

    console.log(formattedRegisters);
  } catch (error) {
    console.log(error);
  }
};

req();
