"""
Verificação de integridade do compactador de Huffman.

Uso (na mesma pasta do main.py):
    python verifica.py                  # testa os 4 casos de borda
    python verifica.py a.txt b.bmp ...  # testa os casos de borda + arquivos extras

Para cada arquivo: compacta (-c), descompacta (-d) e compara o SHA-256
do original com o do arquivo recuperado. Gera também resultados_integridade.csv
para colar no relatório.
"""
import csv
import hashlib
import random
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
MAIN = RAIZ / "main.py"
SAIDA = RAIZ / "output"
CASOS = RAIZ / "casos_borda"


def sha256(caminho: Path) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def gerar_casos_borda() -> list[Path]:
    CASOS.mkdir(exist_ok=True)
    rng = random.Random(42)

    # (d) 256 valores de byte com frequências muito próximas (1000 ± 5)
    simbolos = []
    for valor in range(256):
        simbolos.extend([valor] * (1000 + rng.randint(-5, 5)))
    rng.shuffle(simbolos)

    casos = {
        "a_vazio.bin": b"",
        "b_um_byte.bin": b"\x41",
        "c_simbolo_unico_1e6.bin": b"\x41" * 1_000_000,
        "d_256_valores_uniforme.bin": bytes(simbolos),
    }
    caminhos = []
    for nome, conteudo in casos.items():
        p = CASOS / nome
        p.write_bytes(conteudo)
        caminhos.append(p)
    return caminhos


def executar(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(MAIN), *args],
        cwd=RAIZ, capture_output=True, text=True,
    )


def testar(original: Path) -> dict:
    res = {
        "arquivo": original.name,
        "tamanho_original": original.stat().st_size,
        "tamanho_compactado": "",
        "taxa": "",
        "sha_original": sha256(original),
        "sha_recuperado": "",
        "ok": False,
        "erro": "",
    }

    # Remove saídas antigas para não confundir com resultados de execuções anteriores
    candidatos_huf = [SAIDA / (original.stem + ".huf"), SAIDA / (original.name + ".huf")]
    for c in candidatos_huf:
        c.unlink(missing_ok=True)
    (SAIDA / ("decodificado_" + original.name)).unlink(missing_ok=True)

    # 1) compactar
    p = executar(["-c", str(original)])
    if p.returncode != 0:
        res["erro"] = "falha ao compactar: " + p.stderr.strip().splitlines()[-1:][0] if p.stderr.strip() else "falha ao compactar"
        return res

    huf = next((c for c in candidatos_huf if c.exists()), None)
    if huf is None:
        res["erro"] = "arquivo .huf não foi gerado"
        return res

    res["tamanho_compactado"] = huf.stat().st_size
    if res["tamanho_compactado"]:
        res["taxa"] = round(res["tamanho_original"] / res["tamanho_compactado"], 4)

    # 2) descompactar
    p = executar(["-d", str(huf)])
    if p.returncode != 0:
        linhas = p.stderr.strip().splitlines()
        res["erro"] = "falha ao descompactar: " + (linhas[-1] if linhas else "")
        return res

    recuperado = SAIDA / ("decodificado_" + original.name)
    if not recuperado.exists():
        res["erro"] = "arquivo descompactado não foi gerado (main.py chama decodificaHuff?)"
        return res

    # 3) comparar byte a byte via SHA-256
    res["sha_recuperado"] = sha256(recuperado)
    res["ok"] = res["sha_original"] == res["sha_recuperado"]
    if not res["ok"]:
        res["erro"] = "hashes diferentes"
    return res


def main():
    arquivos = gerar_casos_borda() + [Path(a).resolve() for a in sys.argv[1:]]
    resultados = []

    for arq in arquivos:
        print(f"Testando {arq.name} ...", end=" ", flush=True)
        r = testar(arq)
        resultados.append(r)
        print("OK" if r["ok"] else f"FALHOU ({r['erro']})")

    print()
    print(f"{'arquivo':32} {'original':>10} {'compact.':>10} {'taxa':>8}  resultado")
    for r in resultados:
        print(f"{r['arquivo']:32} {r['tamanho_original']:>10} "
              f"{str(r['tamanho_compactado']):>10} {str(r['taxa']):>8}  "
              f"{'OK' if r['ok'] else 'FALHOU'}")

    with open(RAIZ / "resultados_integridade.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(resultados[0].keys()))
        w.writeheader()
        w.writerows(resultados)

    total_ok = sum(r["ok"] for r in resultados)
    print(f"\n{total_ok}/{len(resultados)} arquivos com integridade verificada.")
    sys.exit(0 if total_ok == len(resultados) else 1)


if __name__ == "__main__":
    main()