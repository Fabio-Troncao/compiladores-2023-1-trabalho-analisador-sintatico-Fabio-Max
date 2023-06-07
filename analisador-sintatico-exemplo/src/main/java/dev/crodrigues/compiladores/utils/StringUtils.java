package dev.crodrigues.compiladores.utils;

import java.util.regex.Pattern;

public final class StringUtils {

    private static Pattern LTRIM = Pattern.compile("^\\s+");

    private StringUtils() {
        throw new IllegalStateException("Utility Class");
    }

    public static String ltrim(String s) {
        return LTRIM
                .matcher(s)
                .replaceAll("");
    }

    public static String indent(String s, int n) {
        return s
                .indent(2 * n)
                .replace("\r\n", "")
                .replace("\n", "");
    }

}
