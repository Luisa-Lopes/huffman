from pathlib import Path
import json
import hashlib


def decodificaHuff(arquivo: Path):
    with open(arquivo, "rb") as f:
        tam_header = int.from_bytes(f.read(4), "big")
        header = json.loads(f.read(tam_header).decode("utf-8"))
        dados_comprimidos = f.read()

    tamanho_original = header["tamanho_original"]
    nome_original = header["nome_original"]

    # Tabela invertida: código (string de bits) -> byte
    tabela = {codigo: int(byte) for byte, codigo in header["codigos"].items()}

    saida = bytearray()

    # Caso de borda: arquivo vazio (não há bits para ler)
    if tamanho_original > 0:
        # Converte cada byte comprimido em 8 caracteres '0'/'1'
        bits = "".join(f"{b:08b}" for b in dados_comprimidos)

        atual = ""
        for bit in bits:
            atual += bit
            if atual in tabela:  # código livre de prefixo: primeiro match é o certo
                saida.append(tabela[atual])
                atual = ""
                # O zero-padding do final é ignorado parando ao atingir o tamanho original
                if len(saida) == tamanho_original:
                    break

    if len(saida) != tamanho_original:
        raise ValueError(
            f"Arquivo corrompido: esperados {tamanho_original} bytes, "
            f"obtidos {len(saida)}"
        )

    pasta_saida = Path("output")
    pasta_saida.mkdir(parents=True, exist_ok=True)
    caminho_saida = pasta_saida / ("decodificado_" + nome_original)
    caminho_saida.write_bytes(bytes(saida))

    print(f"Arquivo gerado: {caminho_saida}")
    print(f"Bytes recuperados: {len(saida)}")
    print(f"SHA-256: {hashlib.sha256(saida).hexdigest()}")