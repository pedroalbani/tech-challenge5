db = db.getSiblingDB('admin');

if (db.getUser(process.env.MONGO_INITDB_ROOT_USERNAME) === null) {
  db.createUser({
    user: process.env.MONGO_INITDB_ROOT_USERNAME,
    pwd: process.env.MONGO_INITDB_ROOT_PASSWORD,
    roles: [{ role: 'readWrite', db: process.env.MONGO_INITDB_DATABASE }]
  });
}

db = db.getSiblingDB(process.env.MONGO_INITDB_DATABASE);

const collections = ['history', 'master-data', 'validation', 'news', 'categories'];

collections.forEach(collection => {
  if (!db.getCollectionNames().includes(collection)) {
    db.createCollection(collection);
  }
});

// Inserir dados na collection 'categories'
let categories = [
  { "categoria": "politica", "palavras_chave": ["vota", "politica", "voto", "stf", "candidato", "presidente", "eleicoes", "eleição", "ministro", "congresso", "vereador", "prefeito", "vereadora", "prefeita"] },
  { "categoria": "cultura", "palavras_chave": ["atriz", "filme", "cultura", "cinema", "teatro", "ator", "série", "show", "música", "arte", "pop", "artista", "cantor", "cantora", "album"] },
  { "categoria": "tecnologia", "palavras_chave": ["tecnologia", "celular", "game", "console", "smartphone", "computador", "notebook", "tablet", "streaming", "elétrica", "elétrico", "aparelho", "dispositivo"] },
  { "categoria": "saude", "palavras_chave": ["doença", "saúde", "saude", "bem-estar", "epidemia", "sintoma", "remédio", "medicina", "médico", "tratamento", "vacina"] },
  { "categoria": "economia", "palavras_chave": ["economia", "imposto", "renda", "taxa", "salário", "tributação", "dolar", "real", "euro", "libra", "R$", "$", "importar", "importação", "importacao"] },
  { "categoria": "criminal", "palavras_chave": ["polícia", "prisão", "crime", "assassinato", "sequestro", "morte", "inocente", "culpado", "bandido", "criminoso", "delegado", "morto", "mandado", "morre", "morta", "facada", "arma", "tiro"] }
];

db.categories.insertMany(categories);
