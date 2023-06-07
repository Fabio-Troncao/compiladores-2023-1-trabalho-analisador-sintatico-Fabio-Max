import re

class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __str__(self):
        return f"Token({self.tipo}, {self.valor})"

class AnalisadorLexico:
    palavra_reservada = ["fun","int", "char", "long", "short", "float", "double", "void",
                         "if", "else", "for", "do", "break", "continue",
                         "struct", "switch", "case", "default", "return", "var",
                         "while", "print", "true", "false", "nil", "this", "or", "and"]

    operadores = r"\|\||&&|==|!=|<|>|<=|>=|\+|-|\*|/|%|--|\+\+|->|!|\.|="

    delimitadores = r"(|)|[|]|{|}|;|,"

    identificadores = r'[a-zA-Z_][a-zA-Z0-9_]*\b'

    inteiros = r'[+-]?\d+'

    ponto_flutuante = r'[+-]?\d+\.\d+'

    constante_textual = r'["\'][^"\']*["\']'

    def __init__(self, arquivo):
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()
                conteudo = re.sub('//.*', ' ', conteudo)
                conteudo = re.sub('(/\*(.|\n)*?\*/)', ' ', conteudo)
                self.tokens = self.tokenizar(conteudo)
                self.indice = 0
                self.token_atual = None

        except FileNotFoundError:
            print(f"Arquivo '{arquivo}' não encontrado.")

    def tokenizar(self, conteudo):
        regex = re.compile(
             r'\d+[a-zA-Z_]*\b|[a-zA-Z_]+[a-zA-Z0-9_]*\b|["\'][^"\']*["\']|[+-]?\d+\.\d+|->|&&|\|\||\-\-|\+\+|[-+*/%&=!><\|]=?|[-+*/%&=!><\|]|\||\(|\)|\[|\]|\{|\}|\.|,|;')
        valores_tokens = regex.findall(conteudo)
        tokens = [self.obter_tipo_token(valor) for valor in valores_tokens]
        tokens.append(Token("Delimitador", "EOF"))
        return tokens

    def obter_tipo_token(self, valor):
        if valor in self.palavra_reservada:
            return Token("Palavra reservada", valor)
        elif re.match(self.operadores, valor):
            return Token("Operador", valor)
        elif valor in self.delimitadores:
            return Token("Delimitador", valor)
        elif re.match(self.inteiros, valor):
            return Token("Inteiro", valor)
        elif re.match(self.ponto_flutuante, valor):
            return Token("Ponto Flutuante", valor)
        elif re.match(self.identificadores, valor):
            return Token("Identificador", valor)
        elif re.match(self.constante_textual, valor):
            return Token("Constante Textual", valor)
        else:
            return Token("Desconhecido", valor)

    def obter_token_atual(self):
        if self.indice < len(self.tokens):
            return self.tokens[self.indice]
        else:
            return None

    def proximo_token(self):
        if self.indice < len(self.tokens):
            self.token_atual = self.tokens[self.indice]
            self.indice += 1
            return self.token_atual
        else:
            self.token_atual = None  
            return self.token_atual

    def verificar_token(self, token, posicao=None):
        if posicao is None:
            posicao = self.indice

        if posicao < len(self.tokens):
            return self.tokens[posicao] == token
        else:
            return False

    def analisar(self):
        resultado = []
        while True:
            try:
                token = self.proximo_token()
                resultado.append((token.tipo, token.valor))
                if token.valor == "EOF":
                    break
                if re.match(r'\d+[a-zA-Z_]+\b|[a-zA-Z_]+[a-zA-Z0-9_]*[^\w\s]', token.valor):
                    raise Exception(f"Token inválido: {token.valor}")
            except Exception as e:
                resultado.append(("Erro Léxico", f"Erro: token inválido ({str(e)})"))
                break

        return resultado

    def mostrar_resultado(self, resultado):
        for tipo, valor in resultado:
            print(f"Tipo: {tipo}\tValor: {valor}")

print("------------ Analisador Léxico ------------")
arquivo = "teste.c"
analisador = AnalisadorLexico(arquivo)
resultado = analisador.analisar()
analisador.mostrar_resultado(resultado)
print("Análise léxica concluída.")