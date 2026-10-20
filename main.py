
from pathlib import Path
from no import No
import math
import json


arquivo_original = Path("input/fonte_binaria_blocos.bin")
dados = arquivo_original.read_bytes();  
extensao = arquivo_original.suffix

print("Tipo:", type(dados))
print("Quantidade de bytes:", len(dados))


dicBytesFreq= {};

for byte in dados[:10]:
    if byte in dicBytesFreq:
        dicBytesFreq[byte] += 1
    else:
       dicBytesFreq[byte] = 1

dicBytesProbabilidade = {}

totalFreq = 0
for byte,freq in dicBytesFreq.items():
    totalFreq += freq

for byte,freq in dicBytesFreq.items():
   dicBytesProbabilidade[byte] = 1/totalFreq * freq


ordenado = dict(sorted(dicBytesProbabilidade.items(), key=lambda item: item[1]))

nos = []

for men, prob in ordenado.items():
    no = No(probabilidade=prob, mensagem=men)
    nos.append(no);


while len(nos) > 1:

    menor = 2
    segundoMenor = 2

    menor_no = None
    segundoMenor_No = None

    for no in nos:
        if no.probabilidade < menor:
            menor = no.probabilidade
            menor_no = no

    nos.remove(menor_no)

    for no in nos:
        if no.probabilidade < segundoMenor:
            segundoMenor = no.probabilidade
            segundoMenor_No = no

    nos.remove(segundoMenor_No)

    soma = menor_no.probabilidade + segundoMenor_No.probabilidade

    no = No(
        probabilidade=soma,
        esquerda=menor_no,
        direita=segundoMenor_No
    )

    nos.append(no)

raiz = nos[0]

raiz.add_simbolo()
raiz.imprimir_arvore()

folhas = raiz.pegar_folhas()

comprimento_medio = 0

for folha in folhas:
    comprimento_medio += len(folha.simbolo)*folha.probabilidade
    print(
        "Mensagem:", folha.mensagem,
        "| Código:", folha.simbolo,
        "| Probabilidade:", folha.probabilidade
    )

bits_codificados = ""

tabela_codigos = {}

for byte in dados[:10]:
    for folha in folhas:
        tabela_codigos[folha.mensagem] = folha.simbolo
        if folha.mensagem == byte:
            bits_codificados += folha.simbolo

print(tabela_codigos)
entropia = 0

for prob in dicBytesProbabilidade.values():
    entropia -= prob * math.log2(prob)


padding = (8 - len(bits_codificados) % 8) % 8

bits_codificados += "0" * padding

print("Codificação: ", bits_codificados)
print("Comprimento médio: ", comprimento_medio)
print("Taxa de compressão", len(dados[:10])/len(bits_codificados))
print("Entropia estimada:", entropia, "bits/símbolo")

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






        
        














