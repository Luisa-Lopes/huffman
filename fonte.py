import math
import random
from collections import Counter

def gerar_fonte_sintetica():
    # 1. Entrada das matrículas (limpa caracteres não numéricos caso digitem com barra/traço)
    m1_str = "".join(filter(str.isdigit, input("Digite a matrícula do integrante 1: ")))
    m2_str = "".join(filter(str.isdigit, input("Digite a matrícula do integrante 2: ")))

    mat1 = int(m1_str)
    mat2 = int(m2_str)

    # 2. Cálculo dos parâmetros m, k e r conforme enunciado
    m = (mat1 + mat2) % 100
    k = 4 + (m % 5)
    r = 0.55 + 0.02 * ((m // 5) % 10)

    # 3. Cálculo das probabilidades teóricas p_i e da entropia teórica H(X)
    alfabeto = list(range(k))
    probabilidades = [(r**i * (1 - r)) / (1 - r**k) for i in alfabeto]
    
    h_teorica = -sum(p * math.log2(p) for p in probabilidades)

    # 4. Geração dos 5 x 10^6 bytes (independentes e identicamente distribuídos)
    num_bytes = 5_000_000
    print(f"\nGerando {num_bytes:,} bytes... aguarde alguns segundos.")
    
    amostras = random.choices(alfabeto, weights=probabilidades, k=num_bytes)
    dados_binarios = bytes(amostras)

    nome_arquivo = "fonte_sintetica.bin"
    with open(nome_arquivo, "wb") as f:
        f.write(dados_binarios)

    # 5. Cálculo da entropia empírica (H_chapéu) a partir das frequências reais geradas
    contagem = Counter(dados_binarios)
    h_empirica = -sum(
        (freq / num_bytes) * math.log2(freq / num_bytes)
        for freq in contagem.values()
    )

    # 6. Exibição dos resultados para o relatório
    print("\n--- Resultados para o Relatório ---")
    print(f"Arquivo gerado : {nome_arquivo}")
    print(f"m              : {m}")
    print(f"k              : {k} (alfabeto: 0 a {k-1})")
    print(f"r              : {r:.2f}")
    print(f"H(X) Teórica   : {h_teorica:.6f} bits/símbolo")
    print(f"H^ Empírica    : {h_empirica:.6f} bits/símbolo")
    print(f"Intervalo alvo : [{h_teorica:.6f}, {h_teorica + 1:.6f}) para o L do seu compactador")

if __name__ == "__main__":
    gerar_fonte_sintetica()