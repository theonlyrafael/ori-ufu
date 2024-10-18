### Consultas pelo Modelo Booleano - ORI - 2024/1 ###
### Rafael Lopes Fraga - 12211BSI257 ###

import sys
from collections import defaultdict

import spacy

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
        with open(caminho, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
            termos = removerStopwords(conteudo)

            for termo in termos:
                indice_invertido[termo][i] += 1

    return indice_invertido


def salvarIndiceInvertido(indice, nome_arquivo="indice.txt"):
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        for termo, arquivos in sorted(indice.items()):
            ocorrencias = " ".join(
                f"{doc},{frequencia}" for doc, frequencia in sorted(arquivos.items())
            )

            arquivo.write(f"{termo}: {ocorrencias}\n")


def processarConsulta(consulta):
    # Os operadores devem ser preservados.
    # A normalizacao com spaCy sera aplicada somente aos termos.
    return consulta.strip().lower()


def resolverSubconsulta(subconsulta, indice_invertido, num_arquivos):
    """
    Resolve uma parte da consulta que contem somente os operadores AND e NOT.
    """

    termos_positivos = []
    termos_negativos = []

    for parte in subconsulta.split("&"):
        parte = parte.strip()

        if not parte:
            continue

        negado = parte.startswith("!")

        if negado:
            termo_bruto = parte[1:].strip()
        else:
            termo_bruto = parte

        termos_normalizados = removerStopwords(termo_bruto)

        if negado:
            termos_negativos.extend(termos_normalizados)
        else:
            termos_positivos.extend(termos_normalizados)

    universo = set(range(1, num_arquivos + 1))

    if termos_positivos:
        primeiro_termo = termos_positivos[0]

        resultado = set(indice_invertido.get(primeiro_termo, {}))

        for termo in termos_positivos[1:]:
            documentos = set(indice_invertido.get(termo, {}))

            resultado &= documentos

    elif termos_negativos:
        # Consultas somente negativas, como !casa,
        # precisam comecar com todos os documentos.
        resultado = universo.copy()

    else:
        resultado = set()

    for termo in termos_negativos:
        documentos = set(indice_invertido.get(termo, {}))

        resultado -= documentos

    return resultado


def resolverConsulta(consulta, indice_invertido, num_arquivos):
    """
    Resolve primeiro NOT e AND dentro de cada subconsulta.
    Depois, faz a uniao das subconsultas separadas por OR.
    """

    consulta = processarConsulta(consulta)
    resultado = set()

    for subconsulta in consulta.split("|"):
        subconsulta = subconsulta.strip()

        if subconsulta:
            resultado_subconsulta = resolverSubconsulta(
                subconsulta, indice_invertido, num_arquivos
            )

            resultado |= resultado_subconsulta

    return resultado


def salvarResposta(documentos, caminho_arquivos, nome_arquivo="resposta.txt"):
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(f"{len(documentos)}\n")

        for documento in sorted(documentos):
            caminho = caminho_arquivos[documento - 1]
            arquivo.write(f"{caminho}\n")


def main():
    if len(sys.argv) != 3:
        print(f"Uso: python {sys.argv[0]} " "<arquivo_base> <arquivo_consulta>")
        sys.exit(1)

    caminho_base = sys.argv[1]
    caminho_consulta = sys.argv[2]

    with open(caminho_base, "r", encoding="utf-8") as arquivo_base:

        caminhos_arquivos = [linha.strip() for linha in arquivo_base if linha.strip()]

    with open(caminho_consulta, "r", encoding="utf-8") as arquivo_consulta:

        consulta = arquivo_consulta.read().strip()

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
