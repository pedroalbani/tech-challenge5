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
