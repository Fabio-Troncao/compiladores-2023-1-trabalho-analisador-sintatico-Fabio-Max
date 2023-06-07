package dev.crodrigues.compiladores.lexico;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class Token {

    ClasseToken classe;
    String lexema;
    int tamanhoMatch;

    public enum ClasseToken {
        CONST_NUMERICA,
        OPERADOR_SOMA,
        OPERADOR_SUBTR,
        OPERADOR_MULTIPL,
        OPERADOR_DIV,
        DELIM_ABRIR_PARENTESES,
        DELIM_FECHAR_PARENTESES,
        FIM_ARQUIVO
    }

}
