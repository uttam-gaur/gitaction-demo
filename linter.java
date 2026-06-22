import java.nio.file.*;
import java.util.*;

/** MiniLint.java - tiny pure-Java linter. Usage: java MiniLint File.java */
public class MiniLint {

    public static void main(String[] args) throws Exception {
        List<String> issues = new ArrayList<>();mzcs vfsbvhfsvbisvsfvbkSKJCBkjsk
        for (String path : args) {
            issues.addAll(check(path));
        }
        if (issues.isEmpty()) {
            System.out.println("No issues found.");
        } else {
            issues.forEach(System.out::println);
        }
        System.exit(issues.isEmpty() ? 0 : 1);
    }

    static List<String> check(String path) throws Exception {
        List<String> issues = new ArrayList<>();
        List<String> lines = Files.readAllLines(Path.of(path));
        Set<String> imported = new LinkedHashSet<>();
        Set<String> usedWords = new HashSet<>();

        for (int i = 0; i < lines.size(); i++) {
            String line = lines.get(i);
            int n = i + 1;
            String trimmed = line.trim();

            if (line.length() > 100) {
                issues.add(path + ":" + n + ": line too long (" + line.length() + " > 100)");
            }
            if (!line.equals(stripTrailing(line))) {
                issues.add(path + ":" + n + ": trailing whitespace");
            }
            if (line.contains("== null") || line.contains("!= null")) {
                issues.add(path + ":" + n + ": prefer Objects.isNull/nonNull over null comparison");
            }
            if (trimmed.startsWith("import ")) {
                String name = trimmed.replace("import", "").replace(";", "").trim();
                imported.add(name.substring(name.lastIndexOf('.') + 1));
            } else {
                usedWords.addAll(Arrays.asList(trimmed.split("[^A-Za-z0-9_]+")));
            }
            if (trimmed.matches(".*catch\\s*\\([^)]*\\)\\s*\\{\\s*}.*")) {
                issues.add(path + ":" + n + ": empty catch block (swallowed exception)");
            }
        }
        for (String imp : imported) {
            long count = usedWords.stream().filter(w -> w.equals(imp)).count();
            if (count == 0) {
                issues.add(path + ": import '" + imp + "' is unused");
            }
        }
        return issues;
    }

    static String stripTrailing(String s) {
        int end = s.length();
        while (end > 0 && Character.isWhitespace(s.charAt(end - 1))) end--;
        return s.substring(0, end);
    }
}
