from AnalisadorLexico import AnalisadorLexico, Token

class ErroSintaticoException(Exception):
    def __init__(self, token_atual, classe_esperada=None):
        self.token_atual = token_atual
        self.classe_esperada = classe_esperada

    def __str__(self):
        if self.classe_esperada is not None:
            return f"Erro sintático: Classe esperada: {self.classe_esperada}, obtida: {self.token_atual}"
        else:
            return f"Erro sintático: Token inesperado: {self.token_atual}"

class AnalisadorSintatico:
    def __init__(self, analisador_lexico):
        self.analisador_lexico = analisador_lexico
        self.proximo_token()

    def proximo_token(self):
        self.token_atual = self.analisador_lexico.proximo_token()

    def analisar(self):
        self.program()
    
    def program(self):
        while self.token_atual and self.token_atual.valor != "EOF":
            self.declaration()
            
            
    def declaration(self):
        if self.token_atual.tipo == "Palavra reservada" and self.token_atual.valor == "fun":
            self.funDecl()
        elif self.token_atual.tipo == "Palavra reservada" and self.token_atual.valor == "var":
            self.varDecl()
        else:
            self.statement()

    def funDecl(self):
        self.checarToken("Palavra reservada", "fun")
        self.function()

    def varDecl(self):
        self.checarToken("Palavra reservada", "var")
        self.checarToken("Identificador", self.token_atual.valor)
        
        if self.checarToken("Operador", "="):
            self.expression()
        
        self.checarToken("Delimitador", ";")

    def statement(self):
        if self.token_atual.tipo == "Palavra reservada":
            if self.token_atual.valor == "print":
                self.printStmt()
            elif self.token_atual.valor == "return":
                self.returnStmt()
            elif self.token_atual.valor == "if":
                self.ifStmt()
            elif self.token_atual.valor == "while":
                self.whileStmt()
            elif self.token_atual.valor == "for":
                self.forStmt()
        elif self.token_atual.tipo == "Delimitador" and self.token_atual.valor == "{":
            self.block()
        else:
            self.exprStmt()

    def exprStmt(self):
        self.expression()
        if self.token_atual is not None and self.token_atual.tipo == "Delimitador" and self.token_atual.valor == ";":
            self.checarToken("Delimitador", ";")
        else:
            raise ErroSintaticoException(self.token_atual)

    def forStmt(self):
        self.checarToken("Palavra reservada", "for")
        self.checarToken("Delimitador", "(")
        if self.token_atual.tipo == "Palavra reservada" and self.token_atual.valor == "var":
            self.varDecl()
        elif self.token_atual.tipo != "Delimitador" or self.token_atual.valor != ";":
            self.exprStmt()
        self.checarToken("Delimitador", ";")
        if self.token_atual.tipo != "Delimitador" and self.token_atual.valor != ";":
            self.expression()
        self.checarToken("Delimitador", ";")
        if self.token_atual.tipo != "Delimitador" and self.token_atual.valor != ")":
            self.expression()
        self.checarToken("Delimitador", ")")
        self.statement()

    def ifStmt(self):
        self.checarToken("Palavra reservada", "if")
        self.checarToken("Delimitador", "(")
        self.expression()
        self.checarToken("Delimitador", ")")
        self.statement()

        if self.token_atual is not None and self.token_atual.tipo == "Palavra reservada" and self.token_atual.valor == "else":
            self.checarToken("Palavra reservada", "else")
            self.statement()

    def printStmt(self):
        self.checarToken("Palavra reservada", "print")
        self.expression()
        self.checarToken("Delimitador", ";")
        
    def returnStmt(self):
        self.checarToken("Palavra reservada", "return")
        if self.token_atual.tipo != "Delimitador" or self.token_atual.valor != ";":
            self.expression()
        self.checarToken("Delimitador", ";")
        
    def whileStmt(self):
        self.checarToken("Palavra reservada", "while")
        self.checarToken("Delimitador", "(")
        self.expression()
        if self.token_atual.tipo != "Delimitador" or self.token_atual.valor != ")":
            self.expression()
        self.checarToken("Delimitador", ")")
        self.statement()

    def block(self):
        self.checarToken("Delimitador", "{")
        while self.token_atual is not None and self.token_atual.valor != "}":
            self.declaration()
        self.checarToken("Delimitador", "}")

    def expression(self):
        self.assignment()

    def assignment(self):
        if self.token_atual.tipo == "Delimitador" and self.token_atual.valor == "(":
            self.checarToken("Delimitador", "(")
            self.call()
            self.checarToken("Operador", ".")
            self.checarToken("Identificador", self.token_atual.valor)
            self.checarToken("Operador", "=")
            self.assignment()
        else:
            self.logic_or()

        if self.token_atual is not None and self.token_atual.tipo == "Operador" and self.token_atual.valor == "=":
            self.checarToken("Operador", "=")
            self.assignment()

    # def assignment(self):
    #     self.logic_or()
    #     if self.token_atual.tipo == "Identificador":
    #         self.checarToken("Identificador", self.token_atual.valor)
    #     elif self.token_atual.tipo == "Operador" and self.token_atual.valor == "=":
    #         self.checarToken("Operador", "=")
    #         self.assignment()
  
    def logic_or(self):
        self.logic_and()
        while self.token_atual and self.token_atual.tipo == "Palavra reservada" and self.token_atual.valor == "or":
            self.checarToken("Palavra reservada", "or")
            self.logic_and()

    def logic_and(self):
        self.equality()
        while self.token_atual and self.token_atual.tipo == "Palavra reservada" and self.token_atual.valor == "and":
            self.checarToken("Palavra reservada", "and")
            self.equality()

    def equality(self):
        self.comparison()
        while self.token_atual and self.token_atual.tipo == "Operador" and (self.token_atual.valor == "!=" or self.token_atual.valor == "=="):
            if self.token_atual.valor == "!=":
                self.checarToken("Operador", "!=")
            elif self.token_atual.valor == "==":
                self.checarToken("Operador", "==")
            self.comparison()

    def comparison(self):
        self.term()
        while self.token_atual and self.token_atual.tipo == "Operador" and (self.token_atual.valor in [">", ">=", "<", "<="]):
            if self.token_atual.valor == ">":
                self.checarToken("Operador", ">")
            elif self.token_atual.valor == ">=":
                self.checarToken("Operador", ">=")
            elif self.token_atual.valor == "<":
                self.checarToken("Operador", "<")
            elif self.token_atual.valor == "<=":
                self.checarToken("Operador", "<=")
            self.term()

    def term(self):
        self.factor()
        while self.token_atual and self.token_atual.tipo == "Operador" and self.token_atual.valor in ["-", "+"]:
            if self.token_atual.valor == "-":
                self.checarToken("Operador", "-")
            elif self.token_atual.valor == "+":
                self.checarToken("Operador", "+")
            self.factor()

    def factor(self):
        self.unary()
        while self.token_atual and self.token_atual.tipo == "Operador" and self.token_atual.valor in ["/", "*"]:
            if self.token_atual.valor == "/":
                self.checarToken("Operador", "/")
            elif self.token_atual.valor == "*":
                self.checarToken("Operador", "*")
            self.unary()

    def unary(self):
        if self.token_atual and self.token_atual.tipo == "Operador":
            if self.token_atual.valor == "!":
                self.checarToken("Operador", "!")
                self.unary()
            elif self.token_atual.valor == "-":
                self.checarToken("Operador", "-")
                self.unary()
        else:
            self.call()

    def call(self):
        self.primary()
        while self.token_atual and (self.token_atual.tipo == "Delimitador" and self.token_atual.valor == "(" or self.token_atual.tipo == "Operador" and self.token_atual.valor == "."):
            if self.token_atual.tipo == "Delimitador" and self.token_atual.valor == "(":
                self.checarToken("Delimitador", "(")
                self.arguments()
                self.checarToken("Delimitador", ")")
            elif self.token_atual.tipo == "Operador" and self.token_atual.valor == ".":
                self.checarToken("Operador", ".")
                self.checarToken("Identificador", self.token_atual.valor)

    def primary(self):
        if self.token_atual is None:
            raise ErroSintaticoException("Fim do arquivo inesperado")

        if self.token_atual.valor in ["true", "false", "nil", "this"]:
            self.checarToken("Palavra reservada", self.token_atual.valor)
        elif self.token_atual.tipo in ["Inteiro", "Ponto Flutuante", "Constante Textual", "Identificador", "Delimitador", "Operador"]:
            self.checarToken(self.token_atual.tipo, self.token_atual.valor)
        elif self.token_atual.valor == "(":
            self.checarToken("Delimitador", "(")
            self.expression()
            self.checarToken("Delimitador", ")")
        elif self.token_atual.valor == "super":
            self.checarToken("Palavra reservada", "super")
            self.checarToken("Delimitador", ".")
            self.checarToken("Identificador", self.token_atual.valor)
        else:
            raise ErroSintaticoException(self.token_atual, "Token inválido")

    def function(self):
        if self.token_atual.tipo != "Identificador":
            raise ErroSintaticoException(
                self.token_atual, "Identificador", self.token_atual.valor)
        self.checarToken("Identificador", self.token_atual.valor)
        self.checarToken("Delimitador", "(")
        if self.token_atual.tipo != "Delimitador" or self.token_atual.valor != ")":
            self.parameters()
        self.checarToken("Delimitador", ")")
        self.block()

    def parameters(self):
        if self.token_atual.tipo == "Identificador":
            self.checarToken("Identificador", self.token_atual.valor)
            
            while self.token_atual.tipo == "Delimitador" and self.token_atual.valor == ",":
                self.checarToken("Delimitador", ",")
                
                if self.token_atual.tipo == "Identificador":
                    self.checarToken("Identificador", self.token_atual.valor)
                else:
                    raise ErroSintaticoException(self.token_atual, "Identificador")             
        else:
            raise ErroSintaticoException(self.token_atual, "Identificador")

    def arguments(self):
        self.expression()
        while self.token_atual.tipo == "Delimitador" and self.token_atual.valor == ",":
            self.checarToken("Delimitador", ",")
            self.expression()

    def checarToken(self, tipo_esperado, classe_esperada=None):
        if self.token_atual is None:
            raise ErroSintaticoException("Fim do arquivo inesperado")

        if self.token_atual.tipo == tipo_esperado and (classe_esperada is None or self.token_atual.valor == classe_esperada):
            print("Token processado:", self.token_atual)
            self.proximo_token()
            return True
        else:
            raise ErroSintaticoException(self.token_atual, classe_esperada)


#     def executar_analise_sintatica(self):
#         try:
#             self.analisar()
#             print("Análise sintática concluída sem erros.")
#         except ErroSintaticoException as e:
#             print("Erro sintático:", e)


# analisador_lexico = AnalisadorLexico("teste.c")
# analisador_sintatico = AnalisadorSintatico(analisador_lexico)
# analisador_sintatico.executar_analise_sintatica()

if __name__ == '__main__':
    print("------------ Analisador Sintático ------------")
    analisador_lexico = AnalisadorLexico("teste.c")
    analisador_sintatico = AnalisadorSintatico(analisador_lexico)
    analisador_sintatico.analisar()
    print("Análise sintática concluída.")