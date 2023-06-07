package dev.crodrigues.compiladores.lexico.regra;

import dev.crodrigues.compiladores.lexico.Token;

import java.util.List;
import java.util.Optional;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public interface Regra {

    List<Pattern> regras();
    Token criarToken(Matcher matcher);

    default Optional<Token> tokenizar(String conteudo) {
        return regras()
                .stream()
                .map(pattern -> pattern.matcher(conteudo))
                .filter(Matcher::find)
                .map(this::criarToken)
                .findFirst();
    }

}
