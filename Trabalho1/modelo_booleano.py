### Consultas pelo Modelo Booleano - ORI - 2024/1 ###
### Rafael Lopes Fraga - 12211BSI257 ###

import spacy
from collections import defaultdict
import sys

nlp = spacy.load("pt_core_news_lg")

def removerStopwords(texto):
    doc = nlp(texto.lower())
    termos_filtrados = []
    for token in doc:
        if not token.is_stop and token.is_alpha:
            termos_filtrados.append(token.lemma_)
    return termos_filtrados

def geraIndiceInvertido(caminho_arquivos):
    indice_invertido = defaultdict(lambda: defaultdict(int))
    
    for i, caminho in enumerate(caminho_arquivos, 1):
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()
            termos = removerStopwords(conteudo)
            for termo in termos:
                indice_invertido[termo][i] += 1
    return indice_invertido

def salvarIndiceInvertido(indice, nome_arquivo="indice.txt"):
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        for termo, arquivos in sorted(indice.items()):
            linha = f"{termo}: " + " ".join([f"{doc},{freq}" for doc, freq in sorted(arquivos.items())]) + "\n"
            arquivo.write(linha)

def processarConsulta(consulta):
    return removerStopwords(consulta)

def resolverConsulta(consulta, indice_invertido, num_arquivos):
    termos_consultas = processarConsulta(consulta)
    resultado = set(range(1, num_arquivos + 1))
    
    operacao_atual = "&"
    
    for termo in termos_consultas:
        if termo in {"&", "|", "!"}:
            operacao_atual = termo
        else:
            documentos = set(indice_invertido.get(termo, []))
            if operacao_atual == "&":
                resultado &= documentos  # AND lógico
            elif operacao_atual == "|":
                resultado |= documentos  # OR lógico
            elif operacao_atual == "!":
                resultado -= documentos  # NOT lógico
                
    return resultado

def salvarResposta(documentos, caminho_arquivos, nome_arquivo="resposta.txt"):
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write(f"{len(documentos)}\n")
        for doc in sorted(documentos):
            arquivo.write(f"{caminho_arquivos[doc - 1]}\n")
            
def main():
    caminho_base = sys.argv[1]
    caminho_consulta = sys.argv[2]
    
    with open(caminho_base, 'r', encoding='utf-8') as f:
        caminhos_arquivos = [linha.strip() for linha in f.readlines()]
        
    with open(caminho_consulta, 'r', encoding='utf-8') as f:
        consulta = f.read().strip()

     # Gera o índice invertido
    indice_invertido = geraIndiceInvertido(caminhos_arquivos)

    # Salva o índice invertido
    salvarIndiceInvertido(indice_invertido)

    # Resolve a consulta
    documentos_resultado = resolverConsulta(consulta, indice_invertido, len(caminhos_arquivos))

    # Salva a resposta da consulta
    salvarResposta(documentos_resultado, caminhos_arquivos)  
    
if __name__ == "__main__":
    main()      
                    