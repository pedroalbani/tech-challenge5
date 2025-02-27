# 🚀 Guia para Rodar o Projeto com Docker

Este projeto utiliza **Docker Compose** para configurar e rodar os serviços necessários, incluindo **MongoDB**, **Mongo Express** e **MLflow**.

---

## 📌 **Pré-requisitos**

Antes de começar, certifique-se de ter instalado:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## 🔧 **Configuração Inicial**

### 1️⃣ Criar o arquivo de variáveis de ambiente `.env`

Crie um arquivo chamado `.env` na raiz do projeto e adicione:

```
MONGO_USERNAME=root
MONGO_PASSWORD=example
MONGO_DATABASE=admin
MONGO_PORT=27017

MLFLOW_PORT=8080
```

---

## 🚀 **Rodando o Projeto**

### 2️⃣ Subindo os containers com Docker Compose

Para iniciar todos os serviços, execute:

```
docker-compose up -d
```

📌 Isso iniciará os serviços em segundo plano (`-d` = _detached mode_).

### 3️⃣ **Verificando os logs**

Se precisar visualizar os logs de um serviço específico, use:

```
docker logs -f <nome_do_serviço>
```

Exemplos:

```
docker logs -f mongo_db_tech_5
docker logs -f mlflow_server
```

---

## 🎯 **Acessando os Serviços**

### 🔹 **Mongo Express** (Interface gráfica do MongoDB)

Acesse no navegador:

```
http://localhost:8081
```

Use as credenciais do `.env` (`MONGO_USERNAME` e `MONGO_PASSWORD`).

### 🔹 **MLflow** (Gerenciamento de Experimentos)

Acesse no navegador:

```
http://localhost:8080
```

---

## 🛑 **Parando os Containers**

Para parar todos os serviços rodando:

```
docker-compose down
```

Se quiser remover volumes e dados armazenados:

```
docker-compose down -v
```

---

## 🐞 **Rodando em Modo Debug**

Caso queira rodar apenas o banco de dados e executar a aplicação manualmente no modo debug:

```
docker-compose up -d mongo
```

Agora, você pode rodar seu código localmente sem precisar subir os outros serviços.

---

## 🛠 **Dicas e Problemas Comuns**

### 🔹 **Erro de porta em uso**

Se receber um erro de que a porta está em uso:

```
ERROR: Bind for 0.0.0.0:27017 failed: port is already allocated
```

Tente parar os serviços que estão rodando na porta 27017:

```
docker ps  # Lista os containers em execução
docker stop <id_do_container>
docker rm <id_do_container>
```

---

Agora seu ambiente está pronto para rodar com Docker! 🚀

# Conjunto de Treino - Datathon Fase 5

## Introdução

O conjunto de treino do Datathon da Fase 5 foi projetado para fornecer dados estruturados que permitem a construção de um sistema de recomendação eficiente para conteúdos da Globo. Ele contém informações sobre usuários, seu histórico de interações e os conteúdos acessados.

## Estrutura do Conjunto de Treino

Os dados de treino foram divididos em múltiplas partes (arquivos `treino_parte_X.csv`, onde X varia de 1 a 6) e armazenados em diferentes pastas. Eles contêm as seguintes colunas:

### **Informações dos Usuários**

- **`userId`**: Identificação única do usuário.
- **`userType`**: Indica se o usuário está logado ou é anônimo.
- **`HistorySize`**: Número total de notícias lidas pelo usuário.
- **`history`**: Lista de notícias visitadas pelo usuário.
- **`TimestampHistory`**: Momento em que o usuário acessou a página.
- **`timeOnPageHistory`**: Tempo (em milissegundos) que o usuário permaneceu na página.
- **`numberOfClicksHistory`**: Número total de cliques do usuário na matéria.
- **`scrollPercentageHistory`**: Porcentagem do conteúdo visualizado pelo usuário.
- **`pageVisitsCountHistory`**: Quantidade de vezes que o usuário acessou a matéria.

### **Informações dos Itens (Matérias)**

Além dos arquivos de histórico de usuários, há uma subpasta chamada `itens` contendo detalhes sobre as matérias acessadas:

- **`Page`**: ID único da matéria (mesmo ID da coluna `history`).
- **`Url`**: URL da matéria.
- **`Issued`**: Data em que a matéria foi publicada.
- **`Modified`**: Última data de modificação da matéria.
- **`Title`**: Título da matéria.
- **`Body`**: Conteúdo textual da matéria.
- **`Caption`**: Subtítulo da matéria.

## Considerações Importantes

- Os dados foram coletados até um determinado período (`T`), garantindo que refletem padrões reais de consumo.
- O conjunto de treino permite modelar padrões de leitura e prever conteúdos que os usuários provavelmente acessarão no futuro.
- O problema do _cold-start_ deve ser tratado, pois novos usuários ou conteúdos não possuem histórico suficiente para alimentar o modelo.

## Próximos Passos

O objetivo do Datathon é desenvolver um modelo de recomendação capaz de prever as próximas notícias que um usuário irá consumir, com base nos dados disponíveis. O modelo precisa considerar a relevância temporal e estratégias de mitigação para o problema de _cold-start_.

---

Para acessar a base de dados e o dicionário de dados, utilize o link oficial:
[Download da base de dados](https://drive.google.com/file/d/13rvnyK5PJADJQgYe-VbdXb7PpLPj7lPr/view)

Sobre os arquivos disponíveis no drive acima

## Arquivos de Dados:

- **`validacao.csv`**: Dados de validação, incluindo histórico de interações dos usuários.
- **`treino_parte1.csv`**: Dados de treino, contendo padrões de comportamento dos usuários. ()
- **`itens-parte1.csv`**: Provavelmente contém metadados dos itens recomendáveis.
- **`test_top10_submission.csv`**: Submissão de previsões para avaliação do modelo.

## Scripts de Processamento:

- **`convert_kaggle.py`**: Processa os dados de validação, transformando o histórico de interações em um formato adequado para submissão no Kaggle​convert_kaggle.
- **`topk.py`**: Utiliza o histórico de interações dos usuários para calcular os top 10 itens mais acessados por cada usuário​topk.

## Processamento de dados

Antes de treinar o modelo, na etapa de tratamento dos dados (feature store), iremos inputar um dado de categoria baseado no Título e Subtítulo das notícias, em um cenário real/ideal utilizariamos um outro Modelo de Machine Learning que através da cariação de tokens a partir do texto (após a limpeza de "fillers"), seria capaz de categorizar os dados. Contudo, como esse não é o objetivo principal do projeto, sendo apenas um ponto que achamos interessante adicionar, iremos fazer de uma forma mais rudimentar.

Iremos predefinir grupos de palavras que esperamos encontrar, enquanto subdividimos as matérias em 3 categorias: G1 (Notícias em geral), GE (Notícias esportivas) e EGO (entretenimento e afins), baseado nesses grupos pré definidos (salvos numa coleção do mongo) e utilizando a geração de tokens dos textos previamente citados usando o scikit learn, criaremos mais um ponto importante a ser levado em consideração durante a sugestão de próximas matérias.

O fluxo dos dados será o seguinte:
<img src="./docs/img/data-flow.svg">

## Fluxo de vida do Modelo

O modelo treinado será exportado para um .pickle usando Ml Flow, suas sugestões serão salvas em uma collection do MongoDB, e junto com os dados futuros serão utilizados para avaliação do modelo em ambiente de produção (essa parte é apenas como teorizamos que isso funcionará em um ambiente real, não está no escopo do projeto atual), onde os clicks do usuário e o tempo passado nas páginas poderiam ser considerados a melhor forma de feedback.

<img src="./docs/img/life-cycle.svg">
