
import argparse 
from pathlib import Path
from codifica import codificaHuff

def main():
    parser = argparse.ArgumentParser(prog="main")
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("-c", "--comprimir", type=Path, metavar="ARQUIVO")
    grupo.add_argument("-d", "--descomprimir", type=Path, metavar="ARQUIVO")

    args = parser.parse_args()

    if args.comprimir:
        codifica(args.comprimir)
    else:
        decodifica(args.descomprimir)

def codifica(arquivo: Path):
    codificaHuff(arquivo)

def decodifica(arquivo: Path):
    print(f"Descomprimindo {arquivo}")

if __name__ == "__main__":
    main()




        
        














