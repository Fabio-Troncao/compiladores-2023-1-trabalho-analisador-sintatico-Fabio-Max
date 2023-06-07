class ErroSintaticoException(Exception):
    def __init__(self, obtida, *esperadas):
        self.obtida = obtida
        self.esperadas = esperadas

    def __str__(self):
        esperadas_str = ', '.join(str(classe) for classe in self.esperadas)
        return f"Classes esperadas: [{esperadas_str}], obtida: {self.obtida}"