
class No:
    def __init__(self, probabilidade, simbolo=None, esquerda=None, direita=None, mensagem=None):
        self.probabilidade = probabilidade
        self.simbolo = simbolo
        self.esquerda = esquerda
        self.direita = direita
        self.mensagem = mensagem

    def eh_folha(self):
        return self.esquerda is None and self.direita is None

    def add_simbolo(self, simbolo=""):
        if self.eh_folha():
            self.simbolo = simbolo
            return

        if self.esquerda is not None:
            self.esquerda.add_simbolo(simbolo + "0")

        if self.direita is not None:
            self.direita.add_simbolo(simbolo + "1")

    def imprimir_arvore(self, nivel=0, lado="Raiz"):
        indentacao = "    " * nivel

        if self.eh_folha():
            print(
                f"{indentacao}{lado}: Folha | "
                f"Mensagem: {self.mensagem} | "
                f"Probabilidade: {self.probabilidade:.4f} | "
                f"Símbolo: {self.simbolo}"
            )
        else:
            print(
                f"{indentacao}{lado}: Nó interno | "
                f"Probabilidade: {self.probabilidade:.4f}"
            )

        if self.esquerda is not None:
            self.esquerda.imprimir_arvore(nivel + 1, "Esquerda")

        if self.direita is not None:
            self.direita.imprimir_arvore(nivel + 1, "Direita")

    def pegar_folhas(self):
        folhas = []

        if self.eh_folha():
            folhas.append(self)
            return folhas

        if self.esquerda is not None:
            folhas.extend(self.esquerda.pegar_folhas())

        if self.direita is not None:
            folhas.extend(self.direita.pegar_folhas())

        return folhas

    def contruir_arvore(ordenado):
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

        return nos 

