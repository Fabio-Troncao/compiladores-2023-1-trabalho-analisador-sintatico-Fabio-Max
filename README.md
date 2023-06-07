# Trabalho: Analisador Sintático

Nome dos alunos e números de matrícula:
* Aluno: Fábio Manuel Martins Troncão
* Aluno: Max Alexandre Fragoso de Oliveira
* Disciplina: Compiladores
* Semestre: 2023/1
* Data de entrega: 31/05/2023
* Valor: 4,0

> Orientações: preencher os dados da dupla antes da data de entrega

## Como entregar este trabalho

Faça um fork deste repositório e faça os commits com o código que você utilizou para chegar nos resultados. Serão aceitos os commits até a data de 31/03/2023 às 13:59:59 (antes da aula).

No dia 31/05/2023 haverá uma apresentação expositiva das técnicas utilizadas e resultado.

**Códigos duplicados ou com bastante semelhança terão suas notas zeradas**

## Analisador Sintático

O presente trabalho consiste da construção de um analisador sintático que funcione em uma sintaxe similar à linguagem C, com as seguintes diferenças:

* ```print``` torna-se uma palavra reservada e vira um comando, e deixa de ser uma função
* Esta linguagem possui tipagem dinâmica, com todas as variáveis declaradas com a palavra reservada ```var```, similar ao Javascript
* Diferente da linguagem C padrão, há os valores booleanos ```true``` e ```false```
* O ```null```, que representa a ausência de um valor, é representado nesta linguagem por ```nil```
* Os operadores lógicos **e** e **ou** são expressados, respectivamente, pelas palavras reservadas ```and``` e ```or```

Existem alguns códigos de exemplo no arquivo ```exemplos.md```

## Tópicos de avaliação

* Escaneamento e extração de tokens
* Análise sintática da linguagem
* Detalhamento e justificativa das técnicas utilizadas
* Análise dos códigos entregues
* Apresentação expositiva dos resultados