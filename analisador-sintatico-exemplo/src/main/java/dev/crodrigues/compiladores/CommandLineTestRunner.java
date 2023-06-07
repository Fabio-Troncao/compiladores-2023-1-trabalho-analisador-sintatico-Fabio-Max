package dev.crodrigues.compiladores;

import dev.crodrigues.compiladores.sintatico.AnalisadorSintatico;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class CommandLineTestRunner implements CommandLineRunner {

    private final AnalisadorSintatico analisadorSintatico;

    @Override
    public void run(String... args) throws Exception {
        analisadorSintatico.analisar("314 + 2 - (4 + 52)");
    }

}
