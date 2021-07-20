var moment = require('moment');
var aws = require('aws-sdk');
var lambda = new aws.Lambda({
  region: 'sa-east-1'
});

const chunkPrediction = async () => {
  const MongoClient = require('mongodb').MongoClient;
  const uri = 'mongodb+srv://atfUser:mvOX8tCv5Tv4pvJU@atfcluster.t51do.mongodb.net/atf_score?retryWrites=true&w=majority';
  const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });
  await client.connect();
  let registers = await client.db('atf_score').collection('feature-collection').find({ dado_valido: true }).limit(100).toArray();
  if (registers && registers.length > 0) {
    registers = registers.map(register => ({
      cnpj: register.cnpj
    }));
    const chunks = [];
    const chunk = 10;
    for (let i = 0, j = registers.length; i < j; i += chunk) {
      chunks.push(registers.slice(i, i + chunk));
    }
    console.log(chunks);
  }
  client.close();
};

var func = async () => {
  try {
    const MongoClient = require('mongodb').MongoClient;
    const uri = 'mongodb+srv://atfUser:mvOX8tCv5Tv4pvJU@atfcluster.t51do.mongodb.net/atf_score?retryWrites=true&w=majority';
    const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

    await client.connect();
    const registers = await client.db('atf_score').collection('initial-collection').find({ insertDate: moment().format('YYYY-MM-DD') }).toArray();
    let serasaRegisters = [];
    let vaduRegisters = [];

    if (registers && registers.length > 0) {
      serasaRegisters = registers.map(register => ({
        text: register.text,
        txt_type: register.txt_type,
        result: register.result
      }));
      vaduRegisters = registers.map(register => ({
        cnpj: register.cnpj
      }));

      for (const vaduRegister of vaduRegisters) {
        await invoke('py_vadu', vaduRegister);
      }

      // vaduRegisters.forEach(async (vaduRegister) => {
      // });

      // serasaRegisters.forEach(async (serasaRegister) => {
      //   invoke('py_serasa', serasaRegister);
      // });

      console.log(vaduRegisters);
    }
    client.close();
  } catch (error) {
    console.log(error);
  }
};

var invoke = async (name, registers) => {
  return new Promise((resolve, reject) => {
    try {
      const params = {
        FunctionName: name,
        InvocationType: 'RequestResponse'
      };
      let count = 0;

      for (const register of registers) {
        params.Payload = JSON.stringify(register);

        console.log(params);

        lambda.invoke(params, function (err, data) {
          if (err) {
            console.log(err);
          } else {
            console.log('Lambda_B said ' + data.Payload);
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

chunkPrediction();
