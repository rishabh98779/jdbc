"""Part III diagrams: persistence choice, JDBC architecture, SQL execution, transactions, schema."""
from diagramkit import *  # noqa
from diagramkit import Canvas, SEM

SVG = "/workspace/book/assets/svg"
PNG = "/workspace/book/assets/png"


def d10_three_persistence():
    c = Canvas(1180, 700)
    c.title(40, 44, "Diagram 11 — In-memory state, persistent files and a database",
            "Three different answers to \"where does the data live?\" — and why a real application wants all three.")

    cols = [
        (40, "IN-MEMORY STATE", "green", [
            "Lives inside the running JVM",
            "Fastest: a field read is nanoseconds",
            "Structured as objects: BasinModel, BasinZone",
            "Supports rich behaviour and invariants",
            "Lost the moment the process exits",
            "BasinWatch: the live basin picture",
        ]),
        (420, "PERSISTENT FILES", "amber", [
            "Lives on the file system",
            "Whole-file or append access",
            "Format chosen by the programmer",
            "No query language, no indexes",
            "Survives restart; portable and inspectable",
            "BasinWatch: log, archive, snapshot, report",
        ]),
        (800, "RELATIONAL DATABASE", "red", [
            "Lives in tables with rows and columns",
            "Queried with SQL (SELECT / INSERT / …)",
            "Indexes make selective search fast",
            "Concurrent access and transactions",
            "Needs a driver; may need a server",
            "BasinWatch: optional SQLite history",
        ]),
    ]
    for x, head, sem, items in cols:
        c.band(x, 76, 340, 40, head, sem, size=12.5)
        y = 128
        for i, item in enumerate(items):
            c.rect(x, y, 340, 44, fill=PAPER, stroke=BORDER, rx=7, sw=1.2)
            c.circle(x + 22, y + 22, 5.5, fill=SEM[sem][2], stroke=SEM[sem][2])
            words = item.split(" ")
            lines, cur = [], ""
            for w in words:
                if len(cur) + len(w) > 40:
                    lines.append(cur); cur = w
                else:
                    cur = (cur + " " + w).strip()
            lines.append(cur)
            c.lines(x + 38, y + 20, lines[:2], size=11, fill=BODY, lh=14)
            y += 52
        y += 6
        c.box(x, y, 340, 96, "COST OF LOSING IT",
              {"green": ["Everything — the basin restarts from defaults"],
               "amber": ["Nothing, but replaying history by hand is slow"],
               "red": ["Nothing essential — files already hold the record"]}[sem],
              sem="slate", title_size=11, sub_size=10.2, pad=9)

    c.note(40, 550, 1100,
           ["WHY MORE THAN ONE?  They are not competing for the same job. Files keep an audit trail and a recoverable",
            "session. The database answers a different question — \"show me the last 200 readings of this zone, newest first\" —",
            "without scanning a whole file by hand. BasinWatch makes the database optional so the application still runs without it."],
           sem="teal", size=11.5)
    c.save("d10_three_persistence", SVG, PNG, 1.9)


def d11_jdbc_architecture():
    c = Canvas(1180, 860)
    c.title(40, 44, "Diagram 13 — JDBC architecture: who does what",
            "Your code speaks to one standard interface. A driver translates it to one database.")

    # left: app
    c.frame(40, 84, 320, 300, "APPLICATION CODE", "purple")
    c.box(64, 116, 272, 60, "com.basinwatch.db", ["SensorReadingRepository · MissionRepository",
                                                  "OperationalEventRepository · ResourceUsageRepository"],
          sem="purple", title_size=12, sub_size=9.8, mono_title=True)
    c.box(64, 190, 272, 58, "DatabaseService", ["bounded single-thread executor",
                                                "off the Swing event thread"],
          sem="purple", title_size=12, sub_size=10)
    c.box(64, 262, 272, 58, "DatabaseManager", ["builds jdbc:sqlite:<path>",
                                                "DriverManager.getConnection"],
          sem="purple", title_size=12, sub_size=10)
    c.box(64, 334, 272, 34, "java.sql.* interfaces only", None, sem="slate",
          title_size=11, rx=8)

    # middle: JDBC API
    c.frame(400, 84, 300, 300, "JDBC API  (java.sql)", "teal")
    for i, (n, d) in enumerate([
            ("DriverManager", "opens a connection from a URL"),
            ("Connection", "a session with the database"),
            ("Statement / PreparedStatement", "carries SQL to the database"),
            ("ResultSet", "a cursor over returned rows"),
            ("SQLException", "the standard failure type")]):
        c.box(424, 116 + i * 52, 252, 44, n, d, sem="teal", rx=7, title_size=11,
              sub_size=9.4, pad=7)

    # right: driver
    c.frame(740, 84, 400, 300, "JDBC DRIVER  (from pom.xml)", "green")
    c.box(764, 116, 352, 72, "org.xerial:sqlite-jdbc 3.50.3.0",
          ["Registered as java.sql.Driver via META-INF/services",
           "Maven downloads it; the shade plugin packs it into the jar"],
          sem="green", title_size=11.6, sub_size=9.8)
    c.box(764, 200, 352, 58, "translates standard calls",
          ["prepareStatement(SQL) → SQLite prepared statement",
           "setString / setDouble / setInt → bound values"],
          sem="green", title_size=11.4, sub_size=9.8)
    c.box(764, 270, 352, 58, "native SQLite engine",
          ["embedded C library loaded in-process",
           "no server, no port, no network"],
          sem="amber", title_size=11.4, sub_size=9.8)
    c.box(764, 340, 352, 34, "data/basinwatch.db", None, sem="slate",
          title_size=11, rx=8, mono_title=True)

    # arrows
    c.arrow(340, 200, 396, 200, color=PURPLE, sw=2.1)
    c.label(368, 190, "JDBC calls", size=10, fill=PURPLE)
    c.arrow(704, 200, 760, 200, color=TEAL, sw=2.1)
    c.label(732, 190, "driver API", size=10, fill=TEAL)
    c.arrow(940, 388, 940, 404, color=GREEN, sw=2.1)

    c.box(40, 412, 1100, 66, "THE KEY IDEA",
          ["JDBC is an interface, not a database. Your code is written against java.sql, so the driver — not your code —",
           "knows whether the database is SQLite, PostgreSQL or Oracle. Changing database means changing a driver and a URL."],
          sem="navy", title_size=12.5, sub_size=11.5, title_fill=NAVY, sub_fill=BODY)

    # driver types
    c.text(40, 528, "The four JDBC driver types", size=15, fill=NAVY, weight="bold")
    types = [
        ("Type 1", "JDBC–ODBC bridge", "Translates JDBC into ODBC calls.\nNeeds a native ODBC driver.\nEffectively removed from modern Java.",
         "not used", "slate"),
        ("Type 2", "Native-API, partly Java", "Calls the database vendor's\nnative client library through JNI.\nNeeds that library installed.",
         "not used", "slate"),
        ("Type 3", "Network-protocol, all Java", "Talks to a middleware server\nthat translates to the database.\nAdds a network hop.",
         "not used", "slate"),
        ("Type 4", "Direct / thin, pure Java", "Speaks the database's own\nprotocol from Java code.\nNo extra install for the caller.",
         "SQLite driver", "green"),
    ]
    x = 40
    for name, title, desc, tag, sem in types:
        c.rect(x, 546, 260, 150, fill=PAPER, stroke=SEM[sem][2], rx=9, sw=1.5)
        c.rect(x, 546, 260, 32, fill=SEM[sem][0], stroke=SEM[sem][2], rx=9, sw=1.5)
        c.rect(x, 566, 260, 12, fill=SEM[sem][0], stroke=SEM[sem][0], rx=0, sw=0)
        c.text(x + 13, 568, name, size=12, fill=INK, weight="bold")
        c.text(x + 246, 568, tag, size=10, fill=SEM[sem][2], anchor="end",
               weight="bold")
        c.text(x + 13, 600, title, size=11.5, fill=INK, weight="bold")
        for i, ln in enumerate(desc.split("\n")):
            c.text(x + 13, 622 + i * 15, ln, size=10.2, fill=BODY)
        x += 273

    c.note(40, 712, 1100,
           ["TECHNICAL CLARIFICATION: sqlite-jdbc is used here as a Type 4-style, self-contained driver — application code",
            "needs no separate client library. Internally it ships and loads a native SQLite engine, so \"pure Java\" describes the",
            "caller's experience, not the absence of native code. There is also no server: SQLite is a file, not a service."],
           sem="amber", size=11.3)
    c.save("d11_jdbc_architecture", SVG, PNG, 1.9)


def d12_sql_execution_lifecycle():
    c = Canvas(1180, 900)
    c.title(40, 44, "Diagram 14 — The complete JDBC execution lifecycle",
            "Ten steps from a repository method to mapped objects, following SensorReadingRepository.findRecent().")

    steps = [
        ("1", "Load / register the driver", "DriverManager finds org.sqlite.JDBC through META-INF/services. In practice this is automatic once the jar is on the classpath.", "green"),
        ("2", "Open a Connection", "DatabaseManager.openConnection() calls DriverManager.getConnection(\"jdbc:sqlite:<path>\") and runs PRAGMA busy_timeout / foreign_keys.", "teal"),
        ("3", "Create a statement", "connection.prepareStatement(SQL) compiles the SQL once and returns a PreparedStatement.", "teal"),
        ("4", "Bind parameters", "statement.setInt(1, limit) — values are sent separately from the SQL text, so they can never be re-parsed as SQL.", "purple"),
        ("5", "Execute", "executeQuery() for SELECT (returns a ResultSet) or executeUpdate() for INSERT/UPDATE/DELETE (returns an int).", "purple"),
        ("6", "Read the ResultSet", "while (results.next()) moves the cursor one row at a time; getString / getDouble read by column name.", "amber"),
        ("7", "Map rows to objects", "Each row becomes an immutable DatabaseHistoryEntry — the JDBC world stops here.", "amber"),
        ("8", "Close ResultSet, then statement", "try-with-resources closes them in reverse order, automatically, even if an exception is thrown.", "red"),
        ("9", "Close the Connection", "The outer try-with-resources returns the connection to the pool or, here, releases the SQLite file handle.", "red"),
        ("10", "Handle SQLException", "Any failure is a checked SQLException. DatabaseService converts it into a status message and a failed future.", "red"),
    ]
    y = 78
    for num, head, body, sem in steps:
        c.rect(40, y, 1100, 72, fill=PAPER, stroke=BORDER, rx=8, sw=1.2)
        c.rect(40, y, 54, 72, fill=SEM[sem][0], stroke=SEM[sem][2], rx=8, sw=1.2)
        c.rect(80, y, 14, 72, fill=SEM[sem][0], stroke=SEM[sem][0], rx=0, sw=0)
        c.circle(67, y + 36, 15, fill=SEM[sem][2], stroke=SEM[sem][2])
        c.text(67, y + 42, num, size=14, fill=PAPER, anchor="middle",
               weight="bold")
        c.text(112, y + 28, head, size=13, fill=INK, weight="bold")
        c.text(112, y + 50, body, size=10.6, fill=BODY)
        if num != "10":
            c.arrow(67, y + 72, 67, y + 80, color=MUTED, sw=1.4)
        y += 80

    c.save("d12_sql_execution_lifecycle", SVG, PNG, 1.9)


def d13_prepared_statement_binding():
    c = Canvas(1180, 760)
    c.title(40, 44, "Diagram 16 — PreparedStatement parameter binding",
            "The SQL text and the data travel separately. That is both a correctness and a security property.")

    c.frame(40, 78, 530, 300, "THE SQL TEMPLATE  (compile once)", "teal")
    c.rect(64, 118, 482, 116, fill=CANVAS, stroke=BORDER, rx=8)
    c.mtext(80, 146, "INSERT INTO sensor_readings", size=13)
    c.mtext(80, 172, "    (timestamp, zone, water_level,", size=13)
    c.mtext(80, 198, "     rainfall, risk_level)", size=13)
    c.mtext(80, 224, "VALUES (?, ?, ?, ?, ?)", size=13, fill=TEAL)
    c.text(64, 258, "Five placeholders. The database parses this text once.", size=11,
           fill=MUTED)
    c.text(64, 282, "Placeholders are data slots, never string concatenation.", size=11,
           fill=MUTED)
    c.text(64, 320, "Repository constant:  private static final String INSERT = \"\"\"…\"\"\";",
           size=10.4, fill=BODY, font=MONO)
    c.text(64, 344, "A text block keeps the SQL readable without escaping.", size=10.4,
           fill=MUTED)

    c.frame(610, 78, 530, 300, "THE BINDING  (values supplied at run time)", "purple")
    binds = [
        ("1", "setString(1, timestamp.toString())", "String", "teal"),
        ("2", "setString(2, zone.id())", "String", "teal"),
        ("3", "setDouble(3, zone.waterLevelMeters())", "double", "purple"),
        ("4", "setDouble(4, reading.rainfallMillimeters())", "double", "purple"),
        ("5", "setString(5, zone.risk().name())", "String", "teal"),
    ]
    y = 112
    for n, call, typ, sem in binds:
        c.rect(634, y, 482, 40, fill=PAPER, stroke=BORDER, rx=7, sw=1.1)
        c.circle(656, y + 20, 12, fill=SEM[sem][2], stroke=SEM[sem][2])
        c.text(656, y + 25, n, size=11, fill=PAPER, anchor="middle", weight="bold")
        c.mtext(678, y + 25, call, size=10.6)
        c.chip(1058, y + 8, 48, 24, typ, sem=sem, size=9.5)
        y += 46
    c.text(634, 356, "Types are explicit, so a number can never be sent as text by accident.",
           size=10.6, fill=MUTED)

    c.arrow(575, 228, 605, 228, color=MUTED, sw=1.6, head=False)
    c.arrow(605, 228, 575, 228, color=MUTED, sw=1.6, head=False)

    c.box(40, 402, 1100, 106, "WHY NOT BUILD THE SQL WITH + ?",
          ["String sql = \"… WHERE zone = '\" + userInput + \"'\";  ← the classic SQL-injection hole.",
           "A PreparedStatement sends the template and the values on separate channels: the database already knows the shape",
           "of the statement, so a value like  ' OR 1=1 --  is treated as a literal string, not as SQL grammar."],
          sem="red", title_size=12.5, sub_size=11, title_fill=INK, sub_fill=BODY)

    c.box(40, 524, 1100, 82, "BASINWATCH BATCHING: ResourceUsageRepository.insert",
          ["statement.setString(1, entry.getKey().name()); statement.setInt(2, entry.getValue()); …",
           "statement.addBatch();   ← accumulate  ·   statement.executeBatch();   ← send all at once"],
          sem="slate", title_size=12.5, sub_size=11, title_fill=INK, sub_fill=BODY)

    c.note(40, 622, 1100,
           ["LIMIT is also bound, not concatenated:  statement.setInt(1, limit).  The value is still validated first",
            "(1…500) so that a programming error is caught before it reaches the database."],
           sem="teal", size=11.3)
    c.save("d13_prepared_statement_binding", SVG, PNG, 1.9)


def d14_statement_types():
    c = Canvas(1180, 700)
    c.title(40, 44, "Diagram 15 — Statement, PreparedStatement and CallableStatement",
            "One interface family, three levels of capability.")

    c.box(40, 82, 1100, 60, "interface java.sql.Statement", None, sem="navy",
          rx=10, title_size=14, mono_title=True)
    c.arrow(350, 142, 350, 176)
    c.arrow(590, 142, 590, 176)
    c.arrow(830, 142, 830, 176)

    boxes = [
        (40, "Statement", "teal", [
            "SQL text supplied per call",
            "execute(sql) / executeQuery(sql)",
            "No parameters, no caching",
            "Use: one-off DDL, PRAGMA",
            "BasinWatch: DatabaseInitializer",
            "  statement.executeUpdate(sql)",
        ]),
        (400, "PreparedStatement", "purple", [
            "SQL pre-compiled once",
            "? placeholders + setX() binders",
            "Reusable, safer, usually faster",
            "addBatch() / executeBatch()",
            "BasinWatch: every repository",
            "  insert / findRecent / deleteBefore",
        ]),
        (760, "CallableStatement", "slate", [
            "Calls a stored procedure",
            "prepareCall(\"{call proc(?)})\")",
            "registerOutParameter for results",
            "Depends on database support",
            "SQLite has no stored procedures",
            "RELATED TECHNIQUE — not used here",
        ]),
    ]
    for x, name, sem, items in boxes:
        c.box(x, 176, 320, 44, name, None, sem=sem, rx=9, title_size=13,
              mono_title=True)
        c.rect(x, 228, 320, 190, fill=PAPER, stroke=BORDER, rx=9, sw=1.2)
        for i, it in enumerate(items):
            is_last = i >= 4
            c.text(x + 16, 256 + i * 30, it, size=11,
                   fill=SEM[sem][2] if is_last else BODY,
                   weight="bold" if is_last else "normal",
                   font=MONO if it.startswith("  ") else SANS)

    c.box(40, 444, 1100, 76, "RESULT-SHAPED DIFFERENCE",
          ["executeQuery() → ResultSet    (SELECT, the caller reads rows)",
           "executeUpdate() → int          (INSERT / UPDATE / DELETE, the caller reads how many rows changed)"],
          sem="teal", title_size=12.5, sub_size=11, title_fill=INK, sub_fill=BODY)

    c.note(40, 542, 1100,
           ["In BasinWatch, Statement appears exactly where there are no parameters to bind — creating tables and",
            "setting PRAGMAs at startup. Everywhere a value comes from the application, PreparedStatement is used instead."],
           sem="amber", size=11.3)
    c.save("d14_statement_types", SVG, PNG, 1.9)


def d15_transaction():
    c = Canvas(1180, 820)
    c.title(40, 44, "Diagram 17 — Transactions: several changes that must succeed or fail together",
            "MissionRepository.recordDispatch() commits three writes as one unit.")

    # commit path
    c.frame(40, 78, 530, 380, "PATH A — ALL THREE WRITES SUCCEED", "green")
    steps = [
        ("openConnection()", "a fresh SQLite connection", "teal"),
        ("setAutoCommit(false)", "start an explicit transaction", "purple"),
        ("INSERT INTO missions", "the mission row (id, type, zone, status…)", "green"),
        ("INSERT INTO resource_usage", "one row per allocated resource type", "green"),
        ("INSERT INTO operational_events", "the MISSION DISPATCH audit row", "green"),
        ("commit()", "all three become permanent together", "green"),
    ]
    y = 112
    for t, s, sem in steps:
        c.box(64, y, 482, 46, t, s, sem=sem, rx=8, title_size=11.4, sub_size=10,
              pad=8)
        c.arrow(305, y + 46, 305, y + 54, color=GREEN, sw=1.5)
        y += 54

    # rollback path
    c.frame(610, 78, 530, 380, "PATH B — A WRITE FAILS", "red")
    rsteps = [
        ("openConnection()", "a fresh SQLite connection", "teal"),
        ("setAutoCommit(false)", "start an explicit transaction", "purple"),
        ("INSERT INTO missions", "succeeds inside the transaction", "green"),
        ("INSERT INTO resource_usage", "throws SQLException", "red"),
        ("catch → rollback()", "the mission row is undone too", "red"),
        ("throw ex", "the failure reaches DatabaseService", "red"),
    ]
    y = 112
    for t, s, sem in rsteps:
        c.box(634, y, 482, 46, t, s, sem=sem, rx=8, title_size=11.4, sub_size=10,
              pad=8)
        c.arrow(875, y + 46, 875, y + 54, color=RED if sem == "red" else GREEN,
                sw=1.5)
        y += 54

    c.box(40, 476, 1100, 96, "WHY THIS MATTERS HERE",
          ["Without a transaction the database could contain a mission row whose resource rows were never written, or",
           "resource rows pointing at a mission that does not exist. Either state would make the history lie about what",
           "actually happened. The foreign key resource_usage.mission_id REFERENCES missions(id) also protects this."],
          sem="navy", title_size=12.5, sub_size=11, title_fill=NAVY, sub_fill=BODY)

    c.box(40, 588, 1100, 96, "THE GUARD CLAUSE IN updateStatus()",
          ["UPDATE missions SET status = ?, completed_at = ? WHERE id = ? AND status = 'ACTIVE'",
           "if (changed != 1) throw new SQLException(\"The active mission record was not found: \" + mission.id());",
           "Updating only an ACTIVE row makes the operation idempotent-safe: a second completion cannot silently succeed."],
          sem="slate", title_size=12.5, sub_size=11, title_fill=INK, sub_fill=BODY,
          mono_title=False)

    c.note(40, 700, 1100,
           ["The rollback helper never hides the original failure: rollback errors are added as suppressed exceptions",
            "(original.addSuppressed(rollbackError)), so a rollback problem cannot mask the real cause."],
           sem="teal", size=11.3)
    c.save("d15_transaction", SVG, PNG, 1.9)


def d16_schema():
    c = Canvas(1180, 760)
    c.title(40, 44, "Diagram 19 — The BasinWatch SQLite schema",
            "Four tables created by DatabaseInitializer at startup. One real foreign key.")

    c.box(40, 82, 300, 200, "sensor_readings", None, sem="teal", rx=9,
          title_size=13, mono_title=True)
    for i, ln in enumerate(["id INTEGER PK AUTOINCREMENT",
                            "timestamp TEXT NOT NULL",
                            "zone TEXT NOT NULL",
                            "water_level REAL NOT NULL",
                            "rainfall REAL NOT NULL",
                            "risk_level TEXT NOT NULL",
                            "INDEX idx_sensor_readings_time"]):
        c.mtext(56, 116 + i * 22, ln, size=10)

    c.box(40, 320, 300, 180, "operational_events", None, sem="purple", rx=9,
          title_size=13, mono_title=True)
    for i, ln in enumerate(["id INTEGER PK AUTOINCREMENT",
                            "timestamp TEXT NOT NULL",
                            "event_type TEXT NOT NULL",
                            "zone TEXT   (nullable)",
                            "message TEXT NOT NULL",
                            "INDEX idx_events_time"]):
        c.mtext(56, 354 + i * 22, ln, size=10)

    c.box(620, 82, 320, 200, "missions", None, sem="green", rx=9,
          title_size=13, mono_title=True)
    for i, ln in enumerate(["id TEXT PRIMARY KEY",
                            "mission_type TEXT NOT NULL",
                            "zone TEXT NOT NULL",
                            "status TEXT NOT NULL",
                            "created_at TEXT NOT NULL",
                            "completed_at TEXT  (nullable)",
                            "INDEX idx_missions_created"]):
        c.mtext(636, 116 + i * 22, ln, size=10)

    c.box(620, 320, 320, 180, "resource_usage", None, sem="amber", rx=9,
          title_size=13, mono_title=True)
    for i, ln in enumerate(["id INTEGER PK AUTOINCREMENT",
                            "resource_type TEXT NOT NULL",
                            "amount INTEGER CHECK (amount > 0)",
                            "mission_id TEXT NOT NULL → missions(id)",
                            "timestamp TEXT NOT NULL",
                            "INDEX idx_resource_usage_time"]):
        c.mtext(636, 354 + i * 22, ln, size=10)

    c.arrow(620, 430, 400, 430, color=AMBER, sw=2.2)
    c.label(510, 420, "FOREIGN KEY", size=10, fill=AMBER, weight="bold")

    c.frame(40, 528, 1100, 132, "RELATIONSHIPS AND RULES", "slate")
    c.text(64, 566, "missions (1) ──→ (many) resource_usage", size=12.5, fill=INK,
           weight="bold", font=MONO)
    c.text(64, 592, "Every allocated resource row must reference an existing mission. PRAGMA foreign_keys = ON enforces it.",
           size=11, fill=BODY)
    c.text(64, 616, "sensor_readings and operational_events are independent append-only histories — they reference no other table.",
           size=11, fill=BODY)
    c.text(64, 640, "All four tables use CREATE TABLE IF NOT EXISTS, so startup is safe to repeat.", size=11,
           fill=BODY)

    c.note(40, 676, 1100,
           ["TEXT timestamps are stored as ISO-8601 strings (Instant.toString()). SQLite has no native date type; the",
            "repository uses julianday(timestamp) < julianday(?) for the retention DELETE so the comparison is still a date comparison."],
           sem="amber", size=11.2)
    c.save("d16_schema", SVG, PNG, 1.9)


def d17_db_dataflow():
    c = Canvas(1180, 780)
    c.title(40, 44, "Diagram 18 — How a reading reaches SQLite and comes back to the screen",
            "Two directions, one repository, and never on the Swing event thread.")

    # write path
    c.band(40, 78, 1100, 36, "DIRECTION 1 — WRITE  ·  accepted event → database row", "purple", size=12.5)
    wsteps = [
        ("ResponseWorker", "process(event)", "purple"),
        ("BasinEngine.persistDatabase", "compares before / after snapshots", "purple"),
        ("DatabaseService.recordSensor", "enqueue(…) on a 1-thread executor", "red"),
        ("ensureInitialized()", "retry at most every 10 s", "red"),
        ("SensorReadingRepository.insert", "PreparedStatement + executeUpdate", "red"),
        ("SQLite basinwatch.db", "row appended", "green"),
    ]
    x = 40
    for i, (t, s, sem) in enumerate(wsteps):
        c.box(x, 128, 168, 74, t, s, sem=sem, rx=8, title_size=11, sub_size=9.6,
              pad=8)
        if i < len(wsteps) - 1:
            c.arrow(x + 168, 165, x + 180, 165, color=MUTED, sw=1.6)
        x += 180

    c.note(40, 216, 1100,
           ["The caller returns immediately. recordSensor() only puts a lambda on a bounded queue (capacity 2 048) —",
            "if that queue is full the update is rejected with a visible message instead of blocking the worker."],
           sem="red", size=11.2)

    # read path
    c.band(40, 300, 1100, 36, "DIRECTION 2 — READ  ·  button click → table on screen", "teal", size=12.5)
    rsteps = [
        ("DatabaseHistoryPanel", "\"Refresh history\" / combo box change", "teal"),
        ("engine.loadDatabaseHistory", "returns CompletableFuture<List<…>>", "teal"),
        ("DatabaseService.loadHistory", "switch on DatabaseHistoryType", "red"),
        ("Repository.findRecent(200)", "SELECT … ORDER BY id DESC LIMIT ?", "red"),
        ("ResultSet → DatabaseHistoryEntry", "rows mapped to immutable values", "amber"),
        ("whenComplete → invokeLater", "tableModel.setEntries(entries)", "teal"),
    ]
    x = 40
    for i, (t, s, sem) in enumerate(rsteps):
        c.box(x, 350, 168, 74, t, s, sem=sem, rx=8, title_size=11, sub_size=9.6,
              pad=8)
        if i < len(rsteps) - 1:
            c.arrow(x + 168, 387, x + 180, 387, color=MUTED, sw=1.6)
        x += 180

    c.box(40, 446, 1100, 90, "THE STALE-RESULT GUARD",
          ["DatabaseHistoryPanel keeps an AtomicLong requestNumber. Each refresh increments it and captures the value.",
           "When the future completes, the callback compares its captured number with the current one; if they differ, the",
           "result is discarded. A slow earlier query can therefore never overwrite the display of a newer one."],
          sem="slate", title_size=12.2, sub_size=10.8, title_fill=INK, sub_fill=BODY)

    c.box(40, 556, 1100, 76, "BOUNDARY RULE",
          ["Every database call happens on the basin-database thread or the basin-control thread.",
           "Swing is touched only inside SwingUtilities.invokeLater(...) — the single rule that keeps the interface responsive."],
          sem="navy", title_size=12.5, sub_size=11, title_fill=NAVY, sub_fill=BODY)

    c.note(40, 654, 1100,
           ["Notice the asymmetry: writes are fire-and-forget; reads return a future the panel can wait on without blocking.",
            "That is what makes the optional database safe to add to an application that must keep running without it."],
           sem="teal", size=11.2)
    c.save("d17_db_dataflow", SVG, PNG, 1.9)


def d18_db_failure_isolation():
    c = Canvas(1180, 640)
    c.title(40, 44, "Diagram 20 — Database failure isolation",
            "The database is optional. When it fails, the simulation must not notice anything except a message.")

    c.box(40, 84, 520, 64, "WHAT FAILS", "SQLite file locked · directory not writable · driver missing · disk full",
          sem="red", title_size=13, sub_size=11)
    c.box(620, 84, 520, 64, "WHAT MUST KEEP WORKING",
          "observation intake · risk assessment · dispatch · file archive · journal · reports · saves",
          sem="green", title_size=13, sub_size=11)
    c.arrow(560, 116, 616, 116, color=MUTED, sw=1.8, head=False)
    c.arrow(616, 116, 560, 116, color=MUTED, sw=1.8, head=False)

    c.frame(40, 176, 1100, 220, "THE MECHANISM, STEP BY STEP", "slate")
    steps = [
        ("SQLException thrown", "any repository call fails"),
        ("initialized = false", "the next call will try to initialise again"),
        ("databaseFailed(msg, ex)", "status becomes \"Database unavailable · …\""),
        ("failureReporter.accept", "BasinEngine records a DATABASE WARNING activity entry"),
        ("journal.append", "the warning is also written to operations.log"),
        ("simulation continues", "no exception escapes into the event-processing path"),
        ("retry after 10 s", "ensureInitialized() attempts recovery on a later call"),
    ]
    y = 212
    for i, (t, s) in enumerate(steps):
        c.rect(64, y, 1052, 24, fill=CANVAS if i % 2 == 0 else PAPER,
               stroke=CANVAS, rx=4, sw=0)
        c.text(78, y + 17, f"{i+1}", size=11, fill=MUTED, weight="bold")
        c.text(104, y + 17, t, size=11.4, fill=INK, weight="bold")
        c.text(360, y + 17, s, size=11, fill=BODY)
        y += 25

    c.box(40, 412, 1100, 88, "WHY THIS IS A DESIGN CHOICE, NOT LAZINESS",
          ["Making the database mandatory would mean that a corrupt SQLite file stops a flood simulation from running.",
           "By isolating it, the application keeps its primary contract — observe, assess, dispatch, and record to files —",
           "while the database remains an added convenience that can be switched off by simply being unavailable."],
          sem="navy", title_size=12.5, sub_size=11, title_fill=NAVY, sub_fill=BODY)

    c.note(40, 516, 1100,
           ["VERIFIED BY TEST: InvariantSuite.continuesWhenDatabaseIsUnavailable() points the service at an unusable",
            "location and asserts that a complete engine session still runs. The behaviour is tested, not just documented."],
           sem="green", size=11.3)
    c.save("d18_db_failure_isolation", SVG, PNG, 1.9)


ALL = [d10_three_persistence, d11_jdbc_architecture, d12_sql_execution_lifecycle,
       d13_prepared_statement_binding, d14_statement_types, d15_transaction,
       d16_schema, d17_db_dataflow, d18_db_failure_isolation]
