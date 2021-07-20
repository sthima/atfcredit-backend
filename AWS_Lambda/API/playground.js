var func = async () => {
  try {
    // const cnpj = req.params.cnpj;
    // if (!cnpj) res.status(422).json({ message: 'CNPJ não informada' });

    const MongoClient = require('mongodb').MongoClient;
    const uri = 'mongodb+srv://atfUser:mvOX8tCv5Tv4pvJU@atfcluster.t51do.mongodb.net/atf_score?retryWrites=true&w=majority';
    const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

    await client.connect();
    // const data = await client.db('atf_score').collection('feature-collection').find({ cnpj: '01877691000179' })
    //   .project({ _id: 0, cnpj: 1, classificacao_modelo1: 1, predicao_modelo1: 1, vadu_info: 1 }).toArray();

    // const formattedData = data.map((record) => {
    //   return {
    //     cnpj: record.cnpj,
    //     classificacao: record.classificacao_modelo1,
    //     predicao: record.predicao_modelo1,
    //     nome: record.vadu_info ? record.vadu_info.Nome : null,
    //     UF: record.vadu_info ? record.vadu_info.UfEndereco : null
    //   };
    // });

    const count = await client.db('atf_score').collection('feature-collection').find({ predicao_modelo1: { $gt: 0.5 } }).count();
    console.log(count);
    client.close();
  } catch (error) {
    console.log(error);
  }
};

func();
