### Consultas pela ponderação TF-IDF (log base 10) - ORI - 2024/1 ###
### Rafael Lopes Fraga - 12211BSI257 ###

import spacy
import math
from collections import defaultdict
import sys

nlp = spacy.load("pt_core_news_lg")

# Função para carregar documentos da base
def carregarDocumentos(caminho_base):
    documentos = []
    with open(caminho_base, 'r', encoding='utf-8') as arquivo_base:
        for linha in arquivo_base:
            caminho_documento = linha.strip()
            with open(caminho_documento, 'r', encoding='utf-8') as doc:
                documentos.append(doc.read().lower())
    return documentos

# Função para filtrar o texto: remove stopwords e realiza lematização
def removerStopwords(texto):
    doc = nlp(texto)
    termos_filtrados = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return termos_filtrados

# Função para gerar índice invertido
def geraIndiceInvertido(documentos):
    indice_invertido = defaultdict(lambda: defaultdict(int))
    for i, doc in enumerate(documentos):
        termos = removerStopwords(doc)
        for termo in termos:
            indice_invertido[termo][i] += 1
    return indice_invertido

# Função para calcular a ponderação TF-IDF
def calcularTFIDF(indice_invertido, num_documentos):
    tfidf = defaultdict(lambda: defaultdict(float))
    for termo, docs in indice_invertido.items():
        ni = len(docs)
        for doc_id, freq in docs.items():
            tf = 1 + math.log10(freq)
            idf = math.log10(num_documentos / ni)
            tfidf[termo][doc_id] = tf * idf
    return tfidf

# Função para salvar o índice invertido em arquivo
def salvarIndice(indice_invertido, caminhos_documentos):
    with open("indice.txt", 'w', encoding='utf-8') as indice_file:
        for termo, docs in sorted(indice_invertido.items()):
            linhas = [f"{caminhos_documentos[doc_id]}: {freq}" for doc_id, freq in docs.items()]
            indice_file.write(f"{termo}: {', '.join(linhas)}\n")

# Função para salvar os pesos TF-IDF em arquivo
def salvarPesos(tfidf, caminhos_documentos):
    with open("pesos.txt", 'w', encoding='utf-8') as pesos_file:
        for doc_id in range(len(caminhos_documentos)):
            linha = f"{caminhos_documentos[doc_id]}: "
            pesos = [f"{termo}, {peso:}" for termo, docs in tfidf.items() if doc_id in docs for peso in [docs[doc_id]]]
            pesos_file.write(linha + " ".join(pesos) + "\n")

# Função principal
def main():
    if len(sys.argv) < 2:
        print("Uso: python tfidf.py <caminho_base.txt>")
        return
    
    caminho_base = sys.argv[1]
    
    # Carregar documentos
    caminhos_documentos = []
    with open(caminho_base, 'r', encoding='utf-8') as f:
        caminhos_documentos = [linha.strip() for linha in f.readlines()]
    
    documentos = carregarDocumentos(caminho_base)
    
    # Gerar índice invertido e calcular TF-IDF
    indice_invertido = geraIndiceInvertido(documentos)
    tfidf = calcularTFIDF(indice_invertido, len(documentos))
    
    # Salvar resultados em arquivos
    salvarIndice(indice_invertido, caminhos_documentos)
    salvarPesos(tfidf, caminhos_documentos)
    
    print("Arquivos 'indice.txt' e 'pesos.txt' gerados.")

if __name__ == "__main__":
    main()
