const { Router } = require('express');

const creditRouter = Router();

const formatData = (data) => {
  return data.map((record) => {
    return {
      cnpj: record.cnpj,
      classificacao: record.classificacao_modelo3,
      predicao: (record.predicao_modelo3 * 100).toFixed(1) + '%',
      resultado: record.resultado,
      nome: record.vadu_info ? record.vadu_info.Nome : null,
      UF: record.vadu_info ? record.vadu_info.UfEndereco : null
    };
  });
};

const initMongoClient = () => {
  const MongoClient = require('mongodb').MongoClient;
  const uri = '';
  return new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });
};

creditRouter.post('/validate/:cnpj', async (req, res) => {
  try {
    const cnpj = req.params.cnpj;
    if (!cnpj) res.status(422).json({ message: 'CNPJ não informado' });

    const resultado = req.body.resultado;
    if (resultado === null) res.status(422).json({ message: 'Resultado não informado' });

    const client = initMongoClient();
    await client.connect();

    await client.db('atf_score').collection('feature-collection')
      .updateOne({ cnpj: cnpj }, { $set: { resultado: resultado ? 1 : 0 } });

    res.status(200).send();

    client.close();
  } catch (error) {
    console.log(error);
    res.status(404).json({ message: error });
  }
});

creditRouter.get('/register/:cnpj', async (req, res) => {
  try {
    const cnpj = req.params.cnpj;
    if (!cnpj) res.status(422).json({ message: 'CNPJ não informado' });

    const client = initMongoClient();
    await client.connect();

    const data = await client.db('atf_score').collection('feature-collection').find({ cnpj: cnpj })
      .project({ _id: 0, cnpj: 1, resultado: 1, classificacao_modelo3: 1, predicao_modelo3: 1, vadu_info: 1 }).toArray();

    if (data && data.length > 0) res.json({ company: formatData(data)[0] });
    else res.status(404).json({ message: 'Nenhum registo encontrado' });

    client.close();
  } catch (error) {
    console.log(error);
    res.status(404).json({ message: error });
  }
});

creditRouter.get('/best', async (req, res) => {
  try {
    const client = initMongoClient();
    await client.connect();

    const data = await client.db('atf_score').collection('feature-collection').find({ dado_valido: true }).sort({ predicao_modelo3: -1 })
      .limit(100).project({ _id: 0, cnpj: 1, resultado: 1, classificacao_modelo3: 1, predicao_modelo3: 1, vadu_info: 1 }).toArray();

    if (data && data.length > 0) res.json({ companies: formatData(data) });
    else res.status(404).json({ message: 'Nenhum registo encontrado' });

    client.close();
  } catch (error) {
    console.log(error);
    res.status(404).json({ message: error });
  }
});

creditRouter.get('/info', async (req, res) => {
  try {
    const client = initMongoClient();
    await client.connect();

    const totalCount = await client.db('atf_score').collection('feature-collection').find().count();
    const predictCount = await client.db('atf_score').collection('feature-collection').find({ predicao_modelo3: { $gt: 0 } }).count();
    const validCount = await client.db('atf_score').collection('feature-collection').find({ dado_valido: true }).count();

    res.json({
      totalEmpresas: totalCount,
      predicaoEmpresas: predictCount,
      validacaoEmpresas: validCount
    });

    client.close();
  } catch (error) {
    console.log(error);
    res.status(404).json({ message: error });
  }
});

module.exports = creditRouter;
