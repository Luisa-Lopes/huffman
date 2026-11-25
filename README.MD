# Codificação de Huffman

Projeto acadêmico de compressão sem perdas usando o algoritmo de Huffman.

## Como funciona

O programa lê um arquivo binário, calcula a frequência dos símbolos,
constrói a árvore de Huffman, gera uma tabela de códigos e grava o resultado
em um arquivo `.huf`.

## Estrutura

- `main.py`: calcula frequências, cria os códigos e grava o arquivo comprimido.
- `no.py`: implementa os nós e operações da árvore de Huffman.
- `input/`: contém o arquivo binário de entrada.
- `output/`: recebe o arquivo gerado.
- `projeto.pdf`: enunciado do projeto.

## Requisitos

- Python 3.10 ou superior

## Como executar

Na pasta do projeto, execute:

```bash
python main.py
```
