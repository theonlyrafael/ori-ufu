# Organização e Recuperação da Informação | ORI

> Trabalhos desenvolvidos em outubro e novembro de 2024 para o quinto período de Sistemas de Informação na UFU.

![Python](https://img.shields.io/badge/Python-3.11.3-3776AB?style=flat&logo=python&logoColor=white) ![spaCy](https://img.shields.io/badge/spaCy-PLN-09A3D5?style=flat&logo=spacy&logoColor=white) ![Status](https://img.shields.io/badge/Status-Concluído-success?style=flat)

## Objetivos

Guardar os trabalhos que desenvolvi na metade do curso, como uma forma de preservar meu histórico de aprendizado na universidade e registrar minha evolução na implementação de técnicas de organização e recuperação da informação.

## Estrutura do Repositório

O repositório está dividido em duas pastas principais, correspondentes aos trabalhos avaliativos desenvolvidos durante a disciplina:

* **`Trabalho1`**: contém a implementação de um modelo booleano de recuperação da informação, utilizando um índice invertido e os operadores lógicos `AND`, `OR` e `NOT`. A pasta também possui os documentos utilizados como base, as consultas de teste e os arquivos gerados pelo programa.

* **`Trabalho2`**: contém a implementação da ponderação TF-IDF, utilizada para calcular a importância dos termos dentro dos documentos de uma coleção. A pasta também possui as bases utilizadas, os documentos analisados e os arquivos produzidos pelo programa.

> **Nota:** as duas pastas possuem uma subpasta `resultados` com as saídas esperadas já executadas e testadas.

## Tecnologias Utilizadas

* Python 3.11.3;
* spaCy;
* Modelo de linguagem `pt_core_news_lg`;
* Processamento de Linguagem Natural;
* Remoção de stopwords;
* Lematização;
* Índice invertido;
* Modelo booleano de recuperação;
* Ponderação TF-IDF.

## Trabalho 1 — Modelo Booleano

O primeiro trabalho implementa um modelo booleano de recuperação da informação. O programa processa os documentos indicados em uma base, cria um índice invertido e executa uma consulta para identificar os documentos correspondentes.

Os operadores disponíveis são:

| Operador | Símbolo | Funcionamento |
|---|---:|---|
| AND | `&` | Retorna documentos que possuem todos os termos |
| OR | `\|` | Retorna documentos que possuem pelo menos um dos termos |
| NOT | `!` | Exclui documentos que possuem determinado termo |

### Execução

Dentro da pasta `Trabalho1`, execute o programa informando o arquivo da base e o arquivo da consulta:

```bash
python modelo_booleano.py base.txt consulta.txt
```

Para executar as demais consultas da base principal:

```bash
python modelo_booleano.py base.txt consulta2.txt
python modelo_booleano.py base.txt consulta3.txt
python modelo_booleano.py base.txt consulta4.txt
python modelo_booleano.py base.txt consulta5.txt
```

Para utilizar a base formada por letras de samba:

```bash
python modelo_booleano.py base_samba.txt consulta_samba.txt
```

As demais consultas dessa base podem ser executadas alterando o segundo argumento:

```bash
python modelo_booleano.py base_samba.txt consulta_samba2.txt
python modelo_booleano.py base_samba.txt consulta_samba3.txt
python modelo_booleano.py base_samba.txt consulta_samba4.txt
```

### Arquivos Gerados

A execução do programa cria ou substitui os seguintes arquivos:

* **`indice.txt`**: armazena o índice invertido da coleção utilizada;
* **`resposta.txt`**: armazena a quantidade e os nomes dos documentos recuperados pela consulta.

O arquivo `indice.txt` permanece com o mesmo conteúdo enquanto a base e seus documentos não forem alterados. Entretanto, o arquivo `resposta.txt` pode mudar de acordo com a consulta executada.

## Trabalho 2 — Ponderação TF-IDF

O segundo trabalho implementa o cálculo dos pesos TF-IDF utilizando logaritmo na base 10. O programa analisa a frequência de cada termo nos documentos e calcula sua importância dentro da coleção.

O cálculo considera:

* a frequência do termo dentro de cada documento;
* a quantidade total de documentos da coleção;
* a quantidade de documentos em que o termo aparece.

### Execução

Dentro da pasta `Trabalho2`, execute o programa informando somente o arquivo da base:

```bash
python tfidf.py base.txt
```

Para gerar o índice e os pesos da coleção formada por letras de samba:

```bash
python tfidf.py base_samba.txt
```

Diferentemente do primeiro trabalho, o programa `tfidf.py` não recebe um arquivo de consulta como argumento.

### Arquivos Gerados

A execução do programa cria ou substitui os seguintes arquivos:

* **`indice.txt`**: armazena o índice invertido e a frequência dos termos nos documentos;
* **`pesos.txt`**: armazena os pesos TF-IDF calculados para os termos de cada documento.

Como esses arquivos são produzidos a partir da coleção de documentos, executar novamente o programa utilizando a mesma base gera os mesmos resultados.

## Dependências

Para executar os trabalhos, é necessário instalar a biblioteca spaCy:

```bash
pip install spacy
```

Em seguida, é necessário instalar o modelo de linguagem em português utilizado pelos programas:

```bash
python -m spacy download pt_core_news_lg
```

## Conclusões

Ao revisar o Trabalho 1, percebi que minha implementação original removia os símbolos dos operadores durante o processamento das consultas. Como consequência, o operador `AND` funcionava apenas por coincidência, enquanto os operadores `OR` e `NOT` não eram interpretados corretamente. Portanto, corrigi o processamento para preservar os operadores e executar adequadamente as operações booleanas.

Já no Trabalho 2, percebi que os arquivos de consulta presentes originalmente na pasta não eram utilizados pelo programa `tfidf.py`, pois o script recebe apenas o arquivo da base como argumento. Consequentemente, executar o programa várias vezes com a mesma base produz os mesmos arquivos `indice.txt` e `pesos.txt`. 

Por fim, o desenvolvimento dos dois trabalhos me permitiu compreender, na prática, diferentes formas de organização e recuperação da informação. Além disso, a correção do modelo booleano após a primeira avaliação ajudou a consolidar meu entendimento sobre o funcionamento dos operadores lógicos, enquanto a implementação do TF-IDF ampliou minha compreensão sobre a importância dos termos em uma coleção de documentos.
