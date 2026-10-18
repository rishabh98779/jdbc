"""Content helpers: figures, callouts, highlighted code, tables."""
import html as _html
import re

PNG = "assets/png"
SHOTS = "assets/shots"

JAVA_KW = {
    "abstract", "assert", "boolean", "break", "byte", "case", "catch", "char",
    "class", "const", "continue", "default", "do", "double", "else", "enum",
    "extends", "final", "finally", "float", "for", "goto", "if", "implements",
    "import", "instanceof", "int", "interface", "long", "native", "new",
    "package", "private", "protected", "public", "record", "return", "short",
    "static", "strictfp", "super", "switch", "synchronized", "this", "throw",
    "throws", "transient", "try", "var", "void", "volatile", "while", "yield",
    "sealed", "permits",
}
SQL_KW = {
    "SELECT", "INSERT", "INTO", "VALUES", "UPDATE", "SET", "DELETE", "FROM",
    "WHERE", "ORDER", "BY", "LIMIT", "JOIN", "ON", "CREATE", "TABLE", "IF",
    "NOT", "EXISTS", "PRIMARY", "KEY", "FOREIGN", "REFERENCES", "INTEGER",
    "TEXT", "REAL", "NULL", "AND", "OR", "DESC", "ASC", "CHECK", "INDEX",
    "AUTOINCREMENT", "AS", "COUNT",
}
JAVA_TYPES = {
    "String", "Integer", "Double", "Long", "Boolean", "Object", "System",
    "Thread", "Runnable", "Exception", "IOException", "SQLException",
    "Connection", "PreparedStatement", "ResultSet", "Statement", "DriverManager",
    "List", "Map", "ArrayList", "ArrayDeque", "EnumMap", "Entry",
    "Instant", "Path", "Files", "File", "ByteArrayOutputStream",
    "ByteArrayInputStream", "ObjectOutputStream", "ObjectInputStream",
    "BufferedWriter", "BufferedReader", "BufferedOutputStream",
    "BufferedInputStream", "DataOutputStream", "DataInputStream",
    "PipedWriter", "PipedReader", "Writer", "Reader", "InputStream",
    "OutputStream", "StandardCharsets", "StandardOpenOption",
    "StandardCopyOption", "AtomicMoveNotSupportedException",
    "ObjectInputFilter", "InvalidClassException", "ThreadPoolExecutor",
    "ArrayBlockingQueue", "CompletableFuture", "TimeUnit", "AtomicLong",
    "SwingUtilities", "JOptionPane", "UIManager", "SwingWorker", "Timer",
    "JFrame", "JPanel", "JButton", "JTable", "JList", "JLabel", "JComboBox",
    "JSlider", "JCheckBox", "JScrollPane", "JSplitPane", "JFileChooser",
    "AbstractTableModel", "DefaultListModel", "Graphics2D", "ActionListener",
    "MouseAdapter", "WindowAdapter", "BorderLayout", "FlowLayout", "GridLayout",
    "Duration", "Locale", "Random", "Comparator", "Optional", "Collectors",
    "CopyOnWriteArrayList", "ExecutorService", "Executors", "ThreadFactory",
    "RejectedExecutionException", "CompletionException", "Serializable",
    "DataInputStream", "ResponseMission", "BasinModel", "BasinZone",
    "SensorReading", "SensorFeed", "SensorIntake", "EventBuffer", "BasinEngine",
    "DatabaseService", "DatabaseManager", "DatabaseInitializer", "SensorArchive",
    "OperationalJournal", "ReportWriter", "SnapshotStore", "SessionSnapshot",
    "SaveCatalog", "AppPaths", "ResourceAllocator", "MissionType", "RiskLevel",
    "ResourceType", "MissionStatus", "BasinEvent", "SimulationPulse",
    "DispatchRequest", "ZoneSnapshot", "MissionSnapshot", "BasinSnapshot",
    "ActivityEntry", "DatabaseHistoryEntry", "DatabaseHistoryType",
    "EngineDiagnostics", "ThreadDiagnostic", "MainFrame", "BasinMapPanel",
    "DatabaseHistoryPanel", "BasinWatchApp", "OperationalEventRepository",
    "SensorReadingRepository", "MissionRepository", "ResourceUsageRepository",
}


def _highlight(text: str, lang: str = "java") -> str:
    esc = _html.escape(text)
    if lang == "none":
        return esc
    token_re = re.compile(
        r'(?P<cm>//[^\n]*|/\*.*?\*/|--[^\n]*|#[^\n]*)'
        r'|(?P<st>"(?:[^"\\\n]|\\.)*"|\'(?:[^\'\\\n]|\\.)*\')'
        r'|(?P<an>@[A-Za-z_][A-Za-z0-9_]*)'
        r'|(?P<word>[A-Za-z_][A-Za-z0-9_$.]*)', re.S)
    out, pos = [], 0
    for m in token_re.finditer(esc):
        out.append(esc[pos:m.start()])
        g, tok = m.lastgroup, m.group()
        if g == "cm":
            out.append(f'<span class="cm">{tok}</span>')
        elif g == "st":
            out.append(f'<span class="st">{tok}</span>')
        elif g == "an":
            out.append(f'<span class="an">{tok}</span>')
        else:
            plain = _html.unescape(tok)
            base = plain.split(".")[-1]
            if lang == "sql" and plain.upper() in SQL_KW:
                out.append(f'<span class="kw">{tok}</span>')
            elif base in JAVA_KW:
                out.append(f'<span class="kw">{tok}</span>')
            elif base in JAVA_TYPES:
                out.append(f'<span class="ty">{tok}</span>')
            elif lang == "java" and base and base[0].isupper() and len(base) > 2:
                out.append(f'<span class="ty">{tok}</span>')
            else:
                out.append(tok)
        pos = m.end()
    out.append(esc[pos:])
    return "".join(out)


def code(text: str, caption: str = "", lang: str = "java", cls: str = "") -> str:
    text = text.strip("\n")
    hl = _highlight(text, lang)
    cap = f'<div class="codecap">{caption}</div>' if caption else ""
    klass = ("long " + cls).strip()
    return f'<pre class="{klass}">{hl}</pre>{cap}'


def callout(kind: str, tag: str, body: str) -> str:
    return f'<div class="callout {kind}"><span class="tag">{tag}</span>{body}</div>'


def lecture(body):   return callout("c-lecture", "FROM THE LECTURE NOTES", body)
def further(body):   return callout("c-concept", "CONCEPT EXPLAINED FURTHER", body)
def practice(body):  return callout("c-practice", "BASINWATCH IN PRACTICE", body)
def related(body):   return callout("c-related", "RELATED TECHNIQUE — NOT USED IN BASINWATCH", body)
def connect(body):   return callout("c-connect", "CONNECTION TO ANOTHER CONCEPT", body)
def distinct(body):  return callout("c-distinct", "IMPORTANT DISTINCTION", body)
def mistake(body):   return callout("c-mistake", "COMMON MISTAKE", body)
def exam(body):      return callout("c-exam", "EXAM TIP", body)
def clarify(body):   return callout("c-clarify", "TECHNICAL CLARIFICATION", body)
def visual(body):    return callout("c-visual", "VISUAL WALKTHROUGH", body)
def core(body):      return callout("c-core", "CORE CONCEPT", body)


def figure(name: str, number: str, title: str, caption: str = "",
           kind: str = "landscape") -> str:
    src = f"{PNG}/{name}.png"
    cap = (f"<b>Diagram {number} — {title}.</b> {caption}" if caption
           else f"<b>Diagram {number} — {title}.</b>")
    return (f'<figure class="{kind}"><img src="{src}" '
            f'alt="{_html.escape(title)}"><figcaption>{cap}</figcaption></figure>')


def screenshot(name: str, number: str, title: str, caption: str = "",
               kind: str = "landscape") -> str:
    """A figure built from a screenshot of the real running application."""
    src = f"{SHOTS}/{name}.png"
    cap = (f"<b>Screenshot {number} — {title}.</b> {caption}" if caption
           else f"<b>Screenshot {number} — {title}.</b>")
    return (f'<figure class="shot {kind}"><img src="{src}" '
            f'alt="{_html.escape(title)}"><figcaption>{cap}</figcaption></figure>')


def table(headers, rows, caption: str = "", cls: str = "") -> str:
    th = "".join(f"<th>{h}</th>" for h in headers)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
                  for r in rows)
    cap = f"<caption>{caption}</caption>" if caption else ""
    klass = ("big " + cls).strip()
    return (f'<table class="{klass}">{cap}<thead><tr>{th}</tr></thead>'
            f'<tbody>{trs}</tbody></table>')


def keyterms(items) -> str:
    lis = "".join(f"<li>{i}</li>" for i in items)
    return (f'<div class="keyterms"><span class="tag">KEY TERMS</span>'
            f'<ul>{lis}</ul></div>')


def summary(items) -> str:
    lis = "".join(f"<li>{i}</li>" for i in items)
    return (f'<div class="summary"><span class="tag">CHAPTER SUMMARY</span>'
            f'<ul>{lis}</ul></div>')


def defbox(term, text) -> str:
    return (f'<div class="defbox"><span class="tag">DEFINITION</span>'
            f'<p><span class="term">{term}</span> — {text}</p></div>')


def qa(q, a) -> str:
    return f'<div class="qa"><div class="q">{q}</div><div class="a">{a}</div></div>'


def exercise(n, title, body, answer="") -> str:
    ans = f'<div class="answer"><b>Answer.</b> {answer}</div>' if answer else ""
    return (f'<div class="exercise"><div class="h">Exercise {n} '
            f'<span>· {title}</span></div>{body}{ans}</div>')


def trace(title, steps) -> str:
    lis = "".join(f"<li>{s}</li>" for s in steps)
    return f'<div class="trace"><div class="h">{title}</div><ol>{lis}</ol></div>'


def chapter(num, title, deck, anchor=None):
    aid = anchor or f"ch{num}"
    return (f'<div class="chapter" id="{aid}">'
            f'<div class="chapter-num">CHAPTER {num}</div>'
            f'<h2 class="chapter-title">{title}</h2>'
            f'<p class="chapter-deck">{deck}</p>')
