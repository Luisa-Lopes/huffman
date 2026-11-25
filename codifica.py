
from pathlib import Path
from no import No
import math
import json


def calcFrequencia(dados):
    dicBytesFreq = {}

    for byte in dados:
        if byte in dicBytesFreq:
            dicBytesFreq[byte] += 1
        else:
            dicBytesFreq[byte] = 1

    dicBytesProbabilidade = {}

    totalFreq = len(dados)

    if totalFreq == 0:
        return ({}, {})

    for byte, freq in dicBytesFreq.items():
        dicBytesProbabilidade[byte] = freq / totalFreq

    ordenado = dict(sorted(dicBytesProbabilidade.items(), key=lambda item: item[1]))

    return (ordenado, dicBytesProbabilidade)


def calcComprimentoMedio(folhas):
    comprimento_medio = 0
    
    for folha in folhas:
        comprimento_medio += len(folha.simbolo)*folha.probabilidade
        print(
                "Mensagem:", folha.mensagem,
                "| Código:", folha.simbolo,
                "| Probabilidade:", folha.probabilidade
        )

    return comprimento_medio     
   
    
def criarTabela(dados, folhas):
    tabela_codigos = {folha.mensagem: folha.simbolo for folha in folhas}
    bits_codificados = "".join(tabela_codigos[byte] for byte in dados)

    return (tabela_codigos, bits_codificados)

def calcEntropia(dicBytesProbabilidade):
    entropia = 0

    for prob in dicBytesProbabilidade.values():
        entropia -= prob * math.log2(prob)

    return entropia


def criacaoArquivo(bits_codificados,arquivo_original,extensao,dados,tabela_codigos):
    dados_comprimidos = bytes(
            int(bits_codificados[i:i+8], 2)
            for i in range(0, len(bits_codificados), 8)
        )
    
    header = {
        "nome_original": arquivo_original.name,
        "extensao": extensao,
        "tamanho_original": len(dados),
        "codigos": {
            str(byte): codigo
            for byte, codigo in tabela_codigos.items()
        }
    }
    
    header_bytes = json.dumps(header).encode("utf-8")
    
    pasta_saida = Path("output")
    pasta_saida.mkdir(parents=True, exist_ok=True)
    
    caminho_saida = pasta_saida / (arquivo_original.stem + ".huf")
    
    with open(caminho_saida, "wb") as arquivo:
        # Grava o tamanho do header em 4 bytes
        arquivo.write(len(header_bytes).to_bytes(4, "big"))
    
        # Grava o header
        arquivo.write(header_bytes)
    
        # Grava os dados codificados, já convertidos para bytes
        arquivo.write(dados_comprimidos)
     
def codificaHuff(arquivo_original: Path):
    dados = arquivo_original.read_bytes();  
    extensao = arquivo_original.suffix

    print("Tipo:", type(dados))
    print("Quantidade de bytes:", len(dados))

    ordenado, dicBytesProbabilidade = calcFrequencia(dados)

    if dados:
        nos = No.contruir_arvore(ordenado=ordenado)
        raiz = nos[0]
        raiz.add_simbolo()
        folhas = raiz.pegar_folhas()

        # Uma árvore com uma única folha gera caminho vazio. Use um bit
        # para que cada ocorrência do único byte tenha representação.
        if len(folhas) == 1:
            folhas[0].simbolo = "0"

        raiz.imprimir_arvore()
        comprimento_medio = calcComprimentoMedio(folhas=folhas)
    else:
        folhas = []
        comprimento_medio = 0

    tabela_codigos, bits_codificados = criarTabela(dados, folhas)

    entropia = calcEntropia(dicBytesProbabilidade)

    padding = (8 - len(bits_codificados) % 8) % 8

    bits_codificados += "0" * padding

    print("Codificação: ", bits_codificados)
    print("Comprimento médio: ", comprimento_medio)
    if bits_codificados:
        print("Taxa de compressão", len(dados) / len(bits_codificados))
    else:
        print("Taxa de compressão: indefinida (nenhum bit foi codificado)")

    print("Entropia estimada:", entropia, "bits/símbolo")

    criacaoArquivo(bits_codificados,arquivo_original,extensao,dados,tabela_codigos)







        
        














