"""Part IV-VI diagrams: Swing/EDT, JDBC-to-Swing, login example, Maven, XML/Spring, integration."""
from diagramkit import *  # noqa
from diagramkit import Canvas, SEM

SVG = "/workspace/book/assets/svg"
PNG = "/workspace/book/assets/png"


def d19_swing_component_tree():
    c = Canvas(1180, 780)
    c.title(40, 44, "Diagram 21 — Swing component containment and the event-dispatch thread",
            "A Swing window is a tree of components. Only one thread is allowed to touch that tree.")

    # containment tree
    c.frame(40, 78, 640, 420, "CONTAINMENT TREE  —  MainFrame extends JFrame", "teal")
    c.box(70, 112, 580, 40, "JFrame  (MainFrame)   —  content pane uses BorderLayout", None,
          sem="teal", rx=8, title_size=11.5)
    y = 168
    children = [
        ("NORTH", "header panel", "toolbar buttons: Start observations · Advance · Inject storm · Save · Restore · Report"),
        ("CENTER", "JSplitPane (workSplit)", "left: BasinMapPanel + response panel   ·   right: missions + inspector"),
        ("SOUTH", "footer panel", "statusLabel — the single place engine status messages appear"),
        ("child", "DatabaseHistoryPanel", "JComboBox + JButton + JTable (AbstractTableModel)"),
        ("child", "BasinMapPanel", "custom paintComponent: rounded zone tiles + risk colours"),
    ]
    for tag, name, detail in children:
        c.rect(70, y, 580, 54, fill=PAPER, stroke=BORDER, rx=7, sw=1.2)
        c.chip(82, y + 14, 66, 26, tag, sem="purple", size=10)
        c.text(162, y + 24, name, size=11.6, fill=INK, weight="bold")
        c.text(162, y + 42, detail, size=10, fill=MUTED)
        c.line(120, y - 12 if y == 168 else y - 4, 120, y, stroke=BORDER, sw=1.2)
        y += 62

    # EDT
    c.frame(710, 78, 430, 420, "THE EVENT-DISPATCH THREAD (EDT)", "purple")
    c.box(736, 112, 378, 56, "single thread, one queue",
          "Swing posts every input event and every repaint request here", sem="purple",
          title_size=12, sub_size=10)
    c.box(736, 184, 378, 100, "RULES THAT KEEP THE UI ALIVE",
          ["1. Never do I/O or JDBC on the EDT",
           "2. Never loop or sleep on the EDT",
           "3. Background work posts results back",
           "   with SwingUtilities.invokeLater(...)"],
          sem="slate", title_size=11.6, sub_size=10.2)
    c.box(736, 300, 378, 84, "WHAT WOULD HAPPEN WITHOUT THE RULE",
          ["A slow query or a blocking readLine() would freeze",
           "paints, clicks and the window itself until it finished.",
           "The operating system would mark the window \"not responding\"."],
          sem="red", title_size=11.4, sub_size=10)
    c.box(736, 400, 378, 82, "HOW BASINWATCH OBEYS IT",
          ["engine.addSnapshotListener(s -> invokeLater(() -> updateSnapshot(s)))",
           "engine.closeAsync().whenComplete((v, f) -> invokeLater(() -> dispose()))",
           "history futures complete, then invokeLater updates the JTable"],
          sem="green", title_size=11.4, sub_size=9.8)

    c.box(40, 516, 1100, 76, "THE HAND-OFF, IN BOTH DIRECTIONS",
          ["EDT → background:  a button listener calls an engine command, which returns a CompletableFuture.",
           "background → EDT:  the future's whenComplete callback wraps the UI update in SwingUtilities.invokeLater."],
          sem="navy", title_size=12.5, sub_size=11, title_fill=NAVY, sub_fill=BODY)

    c.note(40, 612, 1100,
           ["A javax.swing.Timer fires refreshDiagnostics() every 900 ms on the EDT. Because it runs on the EDT it must",
            "stay cheap: it reads an immutable EngineDiagnostics record and sets label text. It never queries the database."],
           sem="amber", size=11.2)
    c.save("d19_swing_component_tree", SVG, PNG, 1.9)


def d20_swing_event_flow():
    c = Canvas(1180, 836)
    c.title(40, 44, "Diagram 22 — Swing event handling: from a click to a changed screen",
            "Following \"Dispatch response\" through listeners, futures and repaints.")

    stages = [
        ("1", "User clicks the button", "The operating system delivers a mouse event to the window.", "teal", "EDT"),
        ("2", "Swing dispatches the event", "The EDT runs every ActionListener registered on that JButton.", "teal", "EDT"),
        ("3", "Listener asks the engine", "engine.dispatch(selectedZoneId, missionType) — returns a boolean, not a future.", "purple", "EDT"),
        ("4", "Engine queues the event", "eventBuffer.offerAll(List.of(new DispatchRequest(...))) — never blocks for long.", "green", "EDT"),
        ("5", "A worker consumes it", "ResponseWorker.take() returns the request; BasinModel.process() applies it.", "purple", "worker"),
        ("6", "Model state changes", "ResourceAllocator.tryReserve() decrements stock; a ResponseMission is created.", "purple", "worker"),
        ("7", "Side effects run", "journal.append(...) · databaseService.recordDispatch(...) · archiveWorker.submit(...)", "amber", "worker"),
        ("8", "An immutable snapshot is published", "publishSnapshot() calls each registered listener with a BasinSnapshot.", "teal", "worker"),
        ("9", "The listener posts to the EDT", "SwingUtilities.invokeLater(() -> updateSnapshot(snapshot))", "purple", "→ EDT"),
        ("10", "The UI repaints", "Labels, JList models and BasinMapPanel.update() + repaint() run on the EDT.", "teal", "EDT"),
    ]
    y = 78
    for num, head, body, sem, tag in stages:
        c.rect(40, y, 1100, 62, fill=PAPER, stroke=BORDER, rx=8, sw=1.2)
        c.circle(72, y + 31, 15, fill=SEM[sem][2], stroke=SEM[sem][2])
        c.text(72, y + 37, num, size=13, fill=PAPER, anchor="middle", weight="bold")
        c.text(104, y + 26, head, size=12.4, fill=INK, weight="bold")
        c.text(104, y + 45, body, size=10.4, fill=BODY)
        c.chip(1000, y + 18, 120, 26, tag, sem="slate", size=10)
        if num != "10":
            c.arrow(72, y + 62, 72, y + 70, color=MUTED, sw=1.4)
        y += 70

    c.note(40, 784, 1100, ["Notice steps 1–4 and 9–10 happen on the EDT; steps 5–8 happen on a worker thread."],
           sem="purple", size=11)
    c.save("d20_swing_event_flow", SVG, PNG, 1.9)


def d21_login_example():
    c = Canvas(1180, 760)
    c.title(40, 44, "Diagram 23 — The lecture-note Swing login application",
            "A small, self-contained example: text fields, a button, an event listener and a database check.")

    c.frame(40, 78, 520, 400, "THE SUPPLIED LOGIN WINDOW", "teal")
    c.rect(70, 112, 460, 250, fill=CANVAS, stroke=BORDER, rx=10)
    c.rect(70, 112, 460, 34, fill=NAVY, stroke=NAVY, rx=10)
    c.rect(70, 132, 460, 14, fill=NAVY, stroke=NAVY, rx=0, sw=0)
    c.text(300, 134, "Login", size=12, fill=PAPER, anchor="middle", weight="bold")
    c.text(100, 186, "Username", size=11.5, fill=INK, weight="bold")
    c.rect(100, 194, 400, 32, fill=PAPER, stroke=TEAL, rx=6, sw=1.3)
    c.text(110, 215, "operator", size=11.5, fill=MUTED)
    c.text(100, 254, "Password", size=11.5, fill=INK, weight="bold")
    c.rect(100, 262, 400, 32, fill=PAPER, stroke=TEAL, rx=6, sw=1.3)
    c.text(110, 283, "••••••••", size=11.5, fill=MUTED)
    c.rect(100, 312, 400, 34, fill=TEAL, stroke=TEAL, rx=7, sw=1.3)
    c.text(300, 334, "Sign in", size=12.5, fill=PAPER, anchor="middle",
           weight="bold")
    c.text(300, 386, "JTextField × 2  ·  JButton  ·  JLabel for the result",
           size=10.6, fill=MUTED, anchor="middle")

    c.frame(590, 78, 550, 400, "WHAT THE ORIGINAL PROGRAM ACTUALLY DOES", "purple")
    steps = [
        ("Build the window", "a JFrame with a JPanel and a null or grid layout"),
        ("Register the listener", "signInButton.addActionListener(this) or a lambda"),
        ("actionPerformed(event)", "runs on the EDT when the button is pressed"),
        ("Read the fields", "String user = userField.getText(); String pass = new String(passField.getPassword());"),
        ("Query the database", "typically a SELECT against a users table"),
        ("Compare the result", "if a matching row exists → show a welcome message"),
        ("Report the outcome", "resultLabel.setText(\"Login successful\") or an error dialog"),
        ("Failure handling", "a SQLException or a missing driver is the classic failure here"),
    ]
    y = 112
    for i, (t, s) in enumerate(steps):
        c.rect(614, y, 502, 40, fill=PAPER, stroke=BORDER, rx=7, sw=1.1)
        c.circle(634, y + 20, 11, fill=PURPLE, stroke=PURPLE)
        c.text(634, y + 24, str(i + 1), size=10.5, fill=PAPER, anchor="middle",
               weight="bold")
        c.text(654, y + 17, t, size=11, fill=INK, weight="bold")
        c.text(654, y + 33, s, size=9.8, fill=MUTED)
        y += 46

    c.box(40, 496, 1100, 96, "THE SAME PATTERN, SCALED UP",
          ["Login: click → listener → SQL query → compare → show message.",
           "BasinWatch: click → listener → engine command → worker → model + SQL → snapshot → invokeLater → repaint.",
           "The shape is identical. BasinWatch adds threads, a bounded queue and immutable snapshots so that the interface",
           "stays responsive while work continues in the background."],
          sem="navy", title_size=12.5, sub_size=11, title_fill=NAVY, sub_fill=BODY)

    c.note(40, 608, 1100,
           ["COMMON MISTAKE in the lecture version: doing the database query inside actionPerformed() on the EDT. It works",
            "for one quick local query, but it freezes the window for the duration. A password should also be compared as a",
            "hash, never stored or transmitted as plain text — a clarification the notes do not make."],
           sem="amber", size=11.2)
    c.save("d21_login_example", SVG, PNG, 1.9)


def d22_maven_build():
    c = Canvas(1180, 800)
    c.title(40, 44, "Diagram 25 — Maven: from pom.xml to a runnable jar",
            "Dependencies, plugins and build phases for the actual BasinWatch pom.xml.")

    # pom
    c.frame(40, 78, 340, 460, "pom.xml  (project object model)", "purple")
    entries = [
        ("groupId / artifactId / version", "com.basinwatch / basinwatch / 1.0.0"),
        ("properties", "maven.compiler.release = 17"),
        ("", "sqlite-jdbc.version = 3.50.3.0"),
        ("dependencies", "org.xerial:sqlite-jdbc:${…}"),
        ("build → maven-compiler-plugin", "release 17"),
        ("build → maven-jar-plugin", "manifest mainClass = BasinWatchApp"),
        ("build → maven-shade-plugin", "phase: package, goal: shade"),
        ("shade transformers", "ServicesResourceTransformer"),
        ("", "ManifestResourceTransformer"),
    ]
    y = 112
    for name, val in entries:
        if not name:
            c.text(64, y + 16, val, size=10, fill=MUTED)
            y += 26
            continue
        c.rect(64, y, 292, 42, fill=PAPER, stroke=BORDER, rx=6, sw=1.1)
        c.text(76, y + 17, name, size=10.4, fill=INK, weight="bold")
        c.text(76, y + 33, val, size=9.6, fill=MUTED)
        y += 48

    # lifecycle
    c.frame(410, 78, 400, 460, "LIFECYCLE  ·  mvn package", "green")
    phases = [
        ("validate", "check the pom is well formed"),
        ("compile", "javac all of src/main/java at release 17"),
        ("test", "run src/test/java — BasinWatch uses a plain main()"),
        ("package", "jar-plugin builds the thin jar"),
        ("", "shade-plugin runs in this phase"),
        ("verify / install", "the shaded jar replaces the thin jar"),
    ]
    y = 116
    for name, note in phases:
        if not name:
            c.text(434, y + 14, note, size=9.8, fill=GREEN)
            y += 30
            continue
        c.box(434, y, 352, 52, name, note, sem="green", rx=7, title_size=11.6,
              sub_size=9.8, pad=8)
        c.arrow(610, y + 52, 610, y + 62, color=GREEN, sw=1.5)
        y += 62

    # output
    c.frame(840, 78, 300, 460, "OUTPUT", "amber")
    c.box(864, 116, 252, 96, "target/basinwatch-1.0.0.jar",
          ["an uber-jar containing", "your classes + SQLite JDBC +", "a Main-Class manifest entry"],
          sem="amber", title_size=10.6, sub_size=9.8)
    c.box(864, 228, 252, 92, "run it",
          ["java -jar target/basinwatch-1.0.0.jar", "no classpath juggling,", "no manual driver setup"],
          sem="green", title_size=10.6, sub_size=9.8)
    c.box(864, 336, 252, 100, "why shade matters here",
          ["JDBC discovers drivers through", "META-INF/services. Without the", "ServicesResourceTransformer the", "driver would not be found."],
          sem="red", title_size=10.6, sub_size=9.6)
    c.box(864, 452, 252, 70, "local repository",
          ["~/.m2/repository caches", "sqlite-jdbc after the first build"],
          sem="slate", title_size=10.6, sub_size=9.6)

    c.box(40, 556, 1100, 96, "HOW DEPENDENCIES REACH THE RUNNING APPLICATION",
          ["pom.xml declares the dependency → Maven downloads the jar into ~/.m2 → the compiler puts it on the classpath →",
           "the shade plugin merges it into the output jar → at run time DriverManager can find the driver class →",
           "without the driver, jdbc:sqlite:… cannot be opened, and DatabaseService would report the database as unavailable."],
          sem="navy", title_size=12.5, sub_size=11, title_fill=NAVY, sub_fill=BODY)

    c.note(40, 668, 1100,
           ["The pom.xml also shows a second, optional path: the thin jar from maven-jar-plugin is useful when running from an",
            "IDE or with an explicit classpath. The shaded jar is what DEPLOYMENT.md ships to a machine without Maven."],
           sem="teal", size=11.2)
    c.save("d22_maven_build", SVG, PNG, 1.9)


def d23_xml_namespaces_schema():
    c = Canvas(1180, 780)
    c.title(40, 44, "Diagram 26 — XML, namespaces and XML Schema",
            "Markup for configuration and data, with names to avoid collisions and a schema to define the rules.")

    c.frame(40, 78, 530, 260, "XML  ·  a tree of labelled elements", "teal")
    c.rect(64, 112, 482, 210, fill=CANVAS, stroke=BORDER, rx=8)
    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<basinwatch xmlns="http://example.org/basinwatch">',
        '  <station id="G-MIL" zone="MIL">',
        '    <rainfall unit="mm">17.5</rainfall>',
        '    <rise unit="cm">3.2</rise>',
        '  </station>',
        '</basinwatch>',
    ]
    for i, ln in enumerate(xml):
        c.mtext(80, 138 + i * 24, ln, size=10.6,
                fill=TEAL if i in (1, 2, 6) else INK)
    c.text(64, 344, "An element has a name, attributes and content. Order and nesting carry meaning.",
           size=10.8, fill=MUTED)

    c.frame(610, 78, 530, 260, "NAMESPACES  ·  two vocabularies, one document", "purple")
    c.rect(634, 112, 482, 210, fill=CANVAS, stroke=BORDER, rx=8)
    ns = [
        '<app:station xmlns:app="http://example.org/basinwatch"',
        '             xmlns:geo="http://example.org/geo">',
        '  <app:rainfall unit="mm">17.5</app:rainfall>',
        '  <geo:location lat="51.5" lon="-0.12"/>',
        '</app:station>',
    ]
    for i, ln in enumerate(ns):
        c.mtext(650, 140 + i * 26, ln, size=10.2)
    c.text(634, 320, "app:rainfall and geo:location are different names from different vocabularies —",
           size=10.6, fill=MUTED)
    c.text(634, 338, "no collision even if both vocabularies define a rainfall element.",
           size=10.6, fill=MUTED)

    c.frame(40, 366, 530, 300, "XML SCHEMA (XSD)  ·  rules for a document", "green")
    xsd = [
        '<xs:element name="station">',
        '  <xs:complexType>',
        '    <xs:sequence>',
        '      <xs:element name="rainfall" type="xs:decimal"/>',
        '      <xs:element name="rise"     type="xs:decimal"/>',
        '    </xs:sequence>',
        '    <xs:attribute name="id" type="xs:string" use="required"/>',
        '  </xs:complexType>',
        '</xs:element>',
    ]
    for i, ln in enumerate(xsd):
        c.mtext(64, 400 + i * 22, ln, size=10.2)
    c.text(64, 606, "A schema states which elements may appear, in what order, how many times, and which",
           size=10.6, fill=MUTED)
    c.text(64, 624, "attributes are required. It turns \"looks like XML\" into \"is valid for this vocabulary\".",
           size=10.6, fill=MUTED)
    c.text(64, 650, "XSD files are themselves XML documents, so they use namespaces too.",
           size=10.6, fill=MUTED)

    c.frame(610, 366, 530, 300, "WHERE THIS BELONGS IN A JAVA PROJECT", "amber")
    items = [
        ("Maven pom.xml", "the one XML file every Maven project really needs"),
        ("Spring XML configuration", "beans, data sources and wiring declared in markup"),
        ("Web descriptors", "web.xml, deployment descriptors, SOAP/WSDL contracts"),
        ("Data interchange", "XML payloads validated against an XSD"),
        ("Annotations vs XML", "the same intent expressed two ways — see Chapter 18"),
        ("BasinWatch", "uses pom.xml only; no Spring XML and no custom XML data"),
    ]
    y = 404
    for name, note in items:
        c.rect(634, y, 482, 40, fill=PAPER, stroke=BORDER, rx=7, sw=1.1)
        c.text(648, y + 17, name, size=11, fill=INK, weight="bold")
        c.text(648, y + 33, note, size=9.8,
               fill=RED if name == "BasinWatch" else MUTED)
        y += 44

    c.note(40, 690, 1100,
           ["IMPORTANT DISTINCTION: pom.xml is XML that Maven reads at build time. It is not read by the application at run",
            "time. BasinWatch reads no XML when it runs, so the XML and XSD material is examinable background and a",
            "RELATED TECHNIQUE — NOT USED IN BASINWATCH, except for the pom.xml itself."],
           sem="amber", size=11.2)
    c.save("d23_xml_namespaces_schema", SVG, PNG, 1.9)


def d24_pojo_vs_bean():
    c = Canvas(1180, 660)
    c.title(40, 44, "Diagram 3 — POJO versus JavaBean",
            "Two ways of describing a plain Java class. One is a style; the other is a convention with rules.")

    c.frame(40, 78, 530, 380, "POJO  ·  Plain Old Java Object", "teal")
    c.rect(64, 112, 482, 176, fill=CANVAS, stroke=BORDER, rx=8)
    code = [
        "public record SensorReading(",
        "        long tick,",
        "        String stationId,",
        "        String zoneId,",
        "        double rainfallMillimeters,",
        "        double observedRiseCentimeters)",
        "        implements BasinEvent { }",
    ]
    for i, ln in enumerate(code):
        c.mtext(80, 140 + i * 22, ln, size=10.6,
                fill=TEAL if i == 0 else INK)
    c.text(64, 306, "Rules: none. Any ordinary class with fields and behaviour is a POJO.", size=10.8, fill=MUTED)
    c.text(64, 326, "BasinWatch uses records — immutable POJOs with generated accessors.", size=10.8, fill=MUTED)
    c.text(64, 352, "Records are ideal for values that cross a boundary and never change:", size=10.8, fill=MUTED)
    c.text(64, 370, "SensorReading, ZoneSnapshot, MissionSnapshot, DatabaseHistoryEntry.", size=10.8, fill=MUTED)
    c.box(64, 386, 482, 56, "GOOD FOR",
          ["immutable events, snapshots and DTOs — no boilerplate, no accidental mutation"],
          sem="slate", title_size=11, sub_size=10.4)

    c.frame(610, 78, 530, 380, "JAVABEAN  ·  a POJO following a convention", "purple")
    c.rect(634, 112, 482, 176, fill=CANVAS, stroke=BORDER, rx=8)
    code2 = [
        "public class SensorReading {",
        "    private long tick;",
        "    public long getTick() { return tick; }",
        "    public void setTick(long t) { this.tick = t; }",
        "    public SensorReading() { }   // no-arg ctor",
        "    // implements Serializable",
        "}",
    ]
    for i, ln in enumerate(code2):
        c.mtext(650, 140 + i * 22, ln, size=10.6,
                fill=PURPLE if i == 0 else INK)
    c.text(634, 306, "Rules: public no-argument constructor · private fields ·", size=10.8, fill=MUTED)
    c.text(634, 326, "getX/setX accessors · often implements Serializable.", size=10.8, fill=MUTED)
    c.text(634, 352, "Frameworks (Spring, JSP/EL, ORM tools, XML decoders) rely on these", size=10.8, fill=MUTED)
    c.text(634, 370, "rules to create and populate objects by reflection.", size=10.8, fill=MUTED)
    c.box(634, 386, 482, 56, "GOOD FOR",
          ["framework-managed objects that must be created and filled by name"],
          sem="slate", title_size=11, sub_size=10.4)

    c.note(40, 476, 1100,
           ["IMPORTANT DISTINCTION: every JavaBean is a POJO, but not every POJO is a JavaBean. A record is a POJO and is",
            "definitely not a JavaBean — it has no no-argument constructor and no setX methods. BasinWatch's Saved* classes",
            "sit in between: private-package plain classes with a no-argument constructor for serialization, but no getters.",
            "They work because ObjectInputStream restores fields directly rather than through accessors."],
           sem="amber", size=11.2)
    c.save("d24_pojo_vs_bean", SVG, PNG, 1.9)


def d25_raw_vs_spring():
    c = Canvas(1180, 840)
    c.title(40, 44, "Diagram 28 — Raw JDBC versus Spring JdbcTemplate",
            "Same database, same SQL, same JDBC underneath. Different amounts of boilerplate above it.")

    # raw side
    c.frame(40, 78, 530, 420, "RAW JDBC  ·  what BasinWatch actually uses", "teal")
    c.rect(64, 112, 482, 240, fill=CANVAS, stroke=BORDER, rx=8)
    raw = [
        "try (Connection connection = database.openConnection();",
        "     PreparedStatement statement =",
        "             connection.prepareStatement(sql)) {",
        "    statement.setInt(1, limit);",
        "    try (ResultSet results = statement.executeQuery()) {",
        "        List<DatabaseHistoryEntry> entries = new ArrayList<>();",
        "        while (results.next()) {",
        "            entries.add(new DatabaseHistoryEntry(",
        "                    Instant.parse(results.getString(\"timestamp\")),",
        "                    \"SENSOR\",",
        "                    results.getString(\"zone\"), …));",
        "        }",
        "        return List.copyOf(entries);",
        "    }",
        "}",
    ]
    for i, ln in enumerate(raw):
        c.mtext(76, 134 + i * 15.6, ln, size=9.4)
    c.text(64, 380, "15 lines. You own the connection, the statement, the ResultSet,", size=10.4, fill=MUTED)
    c.text(64, 398, "the parameter binding, the row mapping and every close().", size=10.4, fill=MUTED)
    c.box(64, 418, 482, 66, "STRENGTHS",
          ["Total control · no framework dependency · explicit resource handling",
           "Explicit transactions in MissionRepository.recordDispatch()"],
          sem="green", title_size=11, sub_size=10)

    # spring side
    c.frame(610, 78, 530, 420, "SPRING JDBC  ·  lecture-note approach", "purple")
    c.rect(634, 112, 482, 240, fill=CANVAS, stroke=BORDER, rx=8)
    sp = [
        "// configuration",
        "@Bean",
        "public DataSource dataSource() {",
        "    DriverManagerDataSource ds = new DriverManagerDataSource();",
        "    ds.setDriverClassName(\"org.sqlite.JDBC\");",
        "    ds.setUrl(\"jdbc:sqlite:data/basinwatch.db\");",
        "    return ds;",
        "}",
        "",
        "// query",
        "return jdbcTemplate.query(",
        "        \"SELECT … FROM sensor_readings ORDER BY id DESC LIMIT ?\",",
        "        rowMapper, limit);",
    ]
    for i, ln in enumerate(sp):
        c.mtext(646, 134 + i * 15.6, ln, size=9.4,
                fill=PURPLE if ln.startswith(("@Bean", "return jdbcTemplate")) else INK)
    c.text(634, 380, "The template opens and closes the connection, creates the", size=10.4, fill=MUTED)
    c.text(634, 398, "statement, binds arguments and calls next() for you.", size=10.4, fill=MUTED)
    c.box(634, 418, 482, 66, "STRENGTHS",
          ["Far less repetitive code · automatic resource cleanup",
           "A RowMapper keeps the mapping in one small class"],
          sem="green", title_size=11, sub_size=10)

    c.box(40, 516, 1100, 96, "WHAT DOES NOT CHANGE",
          ["Spring JdbcTemplate is not a replacement for JDBC — it is a wrapper around it. Underneath, a Connection is still",
           "opened, a PreparedStatement is still created, parameters are still bound, a ResultSet is still read, and the same",
           "SQLException hierarchy still applies. Learning JDBC first is what makes the abstraction understandable."],
          sem="navy", title_size=12.5, sub_size=11, title_fill=NAVY, sub_fill=BODY)

    c.table(40, 628, [260, 420, 420],
            [["", "Raw JDBC (BasinWatch)", "JdbcTemplate (lecture notes)"],
             ["Boilerplate", "high — you write the try-with-resources", "low — the template handles it"],
             ["Control", "complete, including transactions", "good, with TransactionTemplate for explicit control"],
             ["Dependencies", "JDK only", "Spring JDBC plus a DataSource implementation"]],
            row_h=40, size=11)
    c.save("d25_raw_vs_spring", SVG, PNG, 1.9)


def d26_annotation_bean_wiring():
    c = Canvas(1180, 720)
    c.title(40, 44, "Diagram 27 — Annotations, JavaBeans and dependency wiring",
            "How a framework learns what your classes mean without reading a configuration file.")

    c.frame(40, 78, 480, 300, "ANNOTATIONS  ·  metadata attached to code", "purple")
    items = [
        ("@Override", "asks the compiler to check a real override", "used in BasinWatch"),
        ("@FunctionalInterface", "the interface has exactly one abstract method", "used in BasinWatch"),
        ("@Serial", "marks serialization members", "used in BasinWatch"),
        ("@Deprecated", "this API should not be used", "general"),
        ("@Entity / @Table", "this class maps to a database table", "JPA — not used"),
        ("@Autowired / @Component", "the framework should create and inject this", "Spring — not used"),
    ]
    y = 112
    for name, note, tag in items:
        c.rect(64, y, 432, 40, fill=PAPER, stroke=BORDER, rx=7, sw=1.1)
        c.mtext(76, y + 18, name, size=10.4, fill=PURPLE)
        c.text(76, y + 33, note, size=9.6, fill=MUTED)
        c.chip(380, y + 8, 104, 24, tag.split(" — ")[0] if "used" in tag else tag,
               sem="green" if tag == "used in BasinWatch" else "slate", size=8.6)
        y += 44

    c.frame(550, 78, 590, 300, "WHAT A FRAMEWORK DOES WITH THEM", "teal")
    steps = [
        "1. Scan the classpath for annotated classes",
        "2. Read the metadata with reflection",
        "3. Create the objects (needs a no-arg constructor — JavaBean rule)",
        "4. Inject dependencies by type or by name (setters or fields)",
        "5. Manage their lifecycle and scope",
        "6. Wire them into a graph the application can request",
    ]
    y = 116
    for s in steps:
        c.rect(574, y, 542, 38, fill=CANVAS if steps.index(s) % 2 == 0 else PAPER,
               stroke=CANVAS, rx=6, sw=0)
        c.text(588, y + 24, s, size=11, fill=BODY)
        y += 42
    c.text(574, 372, "This is why annotations and JavaBeans appear in the same lecture:",
           size=10.8, fill=MUTED)
    c.text(574, 390, "one marks the class, the other gives the framework a way to build it.",
           size=10.8, fill=MUTED)

    c.box(40, 400, 1100, 92, "THE SAME INTENT, TWO STYLES",
          ["XML configuration:   <bean id=\"dataSource\" class=\"…DriverManagerDataSource\">  <property …/>  </bean>",
           "Annotation style:    @Configuration class AppConfig { @Bean public DataSource dataSource() { … } }",
           "Both describe the same object graph. Annotations are checked by the compiler and live beside the code;",
           "XML is editable without recompiling and centralises configuration in one file."],
          sem="navy", title_size=12.5, sub_size=10.8, title_fill=NAVY, sub_fill=BODY)

    c.note(40, 508, 1100,
           ["RELATED TECHNIQUE — NOT USED IN BASINWATCH: BasinWatch wires its objects by hand. BasinEngine creates the",
            "DatabaseService, which creates the DatabaseManager, which is passed to each repository constructor. This is",
            "constructor injection done manually — the same idea as a framework, with no framework. It is why the project has",
            "no Spring dependency at all, and why the wiring is visible in ordinary Java."],
           sem="amber", size=11.2)
    c.save("d26_annotation_bean_wiring", SVG, PNG, 1.9)


def d27_end_to_end_sequence():
    c = Canvas(1240, 980)
    c.title(40, 44, "Diagram 24 — End-to-end sequence: one sensor reading, fully traced",
            "A single observation followed through every layer that the book teaches.")
    c.text(1200, 44, "CENTREPIECE", size=11, fill=MUTED, anchor="end",
           weight="bold", spacing="1.2")

    lanes = [
        ("SensorFeed\n(thread)", 120, "green"),
        ("PipedWriter→Reader\n(intake thread)", 310, "green"),
        ("EventBuffer\n(monitor)", 500, "purple"),
        ("ResponseWorker\n(thread)", 690, "purple"),
        ("BasinModel\n+ Allocator", 880, "purple"),
        ("File I/O\n+ DatabaseService", 1070, "amber"),
        ("Swing EDT\n(UI)", 1180, "teal"),
    ]
    for name, x, sem in lanes:
        for i, ln in enumerate(name.split("\n")):
            c.text(x, 92 + i * 15, ln, size=10.4, fill=SEM[sem][2], anchor="middle",
                   weight="bold")
        c.line(x, 122, x, 940, stroke=BORDER, sw=1.2, dash="4 4")

    def msg(y, x1, x2, text, color=TEAL, dash=None, num=None):
        c.arrow(x1, y, x2, y, color=color, sw=1.9, dash=dash)
        mx = (x1 + x2) / 2
        c.label(mx, y - 7, text, size=9.6, fill=color, bg=PAPER)
        if num:
            c.circle(x1 - 16 if x1 < x2 else x2 - 16, y, 9.5, fill=color, stroke=color)
            c.text(x1 - 16 if x1 < x2 else x2 - 16, y + 3.6, str(num), size=9,
                   fill=PAPER, anchor="middle", weight="bold")

    steps = [
        (160, 110, 290, "write(reading.encode())  +  '\\n'", GREEN, None, 1),
        (196, 290, 290, "readLine() blocks until a full line exists", GREEN, None, None),
        (232, 290, 290, "SensorReading.parse(line)  —  validates ranges", GREEN, None, 2),
        (268, 290, 470, "eventBuffer.put(event)", PURPLE, None, 3),
        (304, 470, 470, "wait() if full · notifyAll() after add", PURPLE, None, None),
        (340, 650, 470, "eventBuffer.take()", PURPLE, None, 4),
        (376, 650, 830, "model.process(event)  (synchronized)", PURPLE, None, 5),
        (412, 830, 830, "zone.apply(reading) → new water level + risk", PURPLE, None, None),
        (448, 830, 650, "List<String> messages", PURPLE, None, 6),
        (484, 650, 1010, "journal.append(entry)   (BufferedWriter)", AMBER, None, 7),
        (520, 650, 1010, "archiveWorker.submit(reading)", AMBER, None, 8),
        (556, 650, 1010, "databaseService.recordSensor(…)", AMBER, None, 9),
        (592, 1010, 1010, "PreparedStatement.executeUpdate()", RED, None, None),
        (628, 650, 1160, "publishSnapshot() → invokeLater(updateSnapshot)", TEAL, None, 10),
        (664, 1160, 1160, "labels, lists and map repaint", TEAL, None, None),
        (700, 650, 470, "eventBuffer.complete()", PURPLE, None, 11),
    ]
    for y, x1, x2, text, color, dash, num in steps:
        if x1 == x2:
            c.rect(x1 - 5, y - 16, 10, 32, fill=SEM["slate"][0], stroke=color, rx=4,
                   sw=1.2)
            if x1 > 1000:
                c.text(x1 - 16, y + 3, text, size=9.4, fill=color, anchor="end")
            else:
                c.text(x1 + 14, y + 3, text, size=9.4, fill=color)
        else:
            msg(y, x1, x2, text, color, dash, num)

    c.box(40, 748, 1100, 100, "WHAT SURVIVES A RESTART, AND WHAT DOES NOT",
          ["Survives:  the journal lines (operations.log) · the typed archive (sensors.bin) · the SQLite rows · a saved session (.bws).",
           "Does not survive:  the EventBuffer contents · running threads · the ResourceAllocator object · the SensorFeed tick counter,",
           "unless the session was saved — in which case tick, zones, stock and active missions are rebuilt from the snapshot."],
          sem="navy", title_size=12.2, sub_size=10.6, title_fill=NAVY, sub_fill=BODY)

    c.note(40, 862, 1100,
           ["Every arrow is a real method call or a real stream write in the repository. The dashed vertical lines are time, not",
            "wires — the only genuine long-lived connections are the pipe (SensorFeed ↔ SensorIntake) and the shared objects."],
           sem="teal", size=11.1)
    c.save("d27_end_to_end_sequence", SVG, PNG, 1.9)


def d28_dependency_graph():
    c = Canvas(1180, 880)
    c.title(40, 44, "Diagram 4 — Component dependency graph",
            "Who creates whom, and which direction dependencies are allowed to point.")

    def node(x, y, w, h, name, sub, sem):
        c.box(x, y, w, h, name, sub, sem=sem, rx=9, title_size=11.4, sub_size=9.4,
              pad=9)

    node(40, 84, 230, 66, "app.BasinWatchApp", "main() · bootstrap", "teal")
    node(300, 84, 230, 66, "app.MainFrame", "JFrame · UI only", "teal")
    node(560, 84, 230, 66, "app.BasinMapPanel", "JPanel · painting", "teal")
    node(820, 84, 300, 66, "app.DatabaseHistoryPanel", "JTable · reads via engine", "teal")

    node(300, 200, 230, 70, "engine.BasinEngine", "lifecycle · wiring · futures", "purple")
    node(40, 200, 230, 70, "engine.EventBuffer", "bounded monitor", "purple")
    node(560, 200, 230, 70, "engine.SensorFeed", "Thread · PipedWriter", "purple")
    node(820, 200, 300, 70, "engine.SensorIntake / ArchiveWorker", "Runnable / Thread", "purple")

    node(40, 320, 230, 74, "domain.BasinModel", "aggregate · invariants", "green")
    node(300, 320, 230, 74, "domain.BasinZone", "water + risk", "green")
    node(560, 320, 230, 74, "domain.ResourceAllocator", "synchronized stock", "green")
    node(820, 320, 300, 74, "domain.BasinEvent / Snapshot records", "immutable values", "green")

    node(40, 444, 230, 74, "io.AppPaths / SaveCatalog", "paths + metadata", "amber")
    node(300, 444, 230, 74, "io.OperationalJournal", "BufferedWriter", "amber")
    node(560, 444, 230, 74, "io.SensorArchive", "DataOutputStream", "amber")
    node(820, 444, 300, 74, "io.SnapshotStore / SessionSnapshot", "ObjectOutputStream", "amber")

    node(300, 568, 230, 74, "db.DatabaseService", "1-thread executor", "red")
    node(560, 568, 230, 74, "db.DatabaseManager", "Connection factory", "red")
    node(820, 568, 300, 74, "db.*Repository", "PreparedStatement + ResultSet", "red")

    def dep(x1, y1, x2, y2, color=MUTED):
        c.arrow(x1, y1, x2, y2, color=color, sw=1.5, head_size=8)

    dep(300, 150, 300, 198, TEAL)
    dep(415, 150, 590, 198, TEAL)
    dep(880, 150, 880, 198, TEAL)
    dep(415, 270, 150, 318, PURPLE)
    dep(500, 270, 600, 318, PURPLE)
    dep(640, 270, 660, 318, PURPLE)
    dep(940, 270, 940, 318, PURPLE)
    dep(400, 270, 340, 318, PURPLE)
    dep(360, 394, 340, 442, GREEN)
    dep(400, 394, 620, 442, GREEN)
    dep(430, 394, 400, 442, GREEN)
    dep(430, 270, 150, 442, PURPLE)
    dep(430, 270, 900, 442, PURPLE)
    dep(430, 270, 415, 566, PURPLE)
    dep(660, 642, 660, 640, RED)
    dep(530, 640, 660, 640, RED)
    dep(415, 642, 415, 642, RED)
    c.arrow(660, 642, 660, 640, color=RED, head=False)

    c.frame(40, 672, 1100, 148, "DEPENDENCY RULES", "slate")
    c.text(64, 706, "app  →  engine  →  domain, io, db", size=12, fill=INK,
           weight="bold", font=MONO)
    c.text(64, 730, "io and db never import app or engine. domain imports nothing from the other packages.", size=11, fill=BODY)
    c.text(64, 754, "Repositories are constructed by DatabaseService, which is constructed by BasinEngine — manual constructor injection.", size=11, fill=BODY)
    c.text(64, 778, "Dependencies point one way. That is why the model can be tested with no database, no files and no window.", size=11, fill=BODY)
    c.text(64, 802, "InvariantSuite exploits exactly this: it drives BasinModel, SnapshotStore and DatabaseService directly.", size=11, fill=TEAL, weight="bold")

    c.save("d28_dependency_graph", SVG, PNG, 1.9)


def d29_revision_map():
    c = Canvas(1180, 880)
    c.title(40, 44, "Diagram 29 — Final visual summary of the complete Java system",
            "The whole book on one page: from an incoming byte to a restored session.")

    # pipeline
    c.band(40, 78, 1100, 34, "THE RUNTIME PIPELINE  ·  data in, decisions out", "navy", size=12.5)
    pl = [
        ("SOURCE", "synthetic sensor\nreading", "green"),
        ("TRANSPORT", "piped character\nstreams", "green"),
        ("VALIDATE", "parse + range\nchecks", "amber"),
        ("QUEUE", "bounded buffer\nwait/notifyAll", "purple"),
        ("PROCESS", "model update +\natomic reservation", "purple"),
        ("PERSIST", "text log · binary\narchive · SQLite", "amber"),
        ("PRESENT", "immutable snapshot\n→ Swing EDT", "teal"),
        ("RECOVER", "versioned snapshot\n→ restored model", "teal"),
    ]
    x = 40
    for i, (tag, name, sem) in enumerate(pl):
        c.rect(x, 126, 124, 92, fill=SEM[sem][0], stroke=SEM[sem][2], rx=9, sw=1.4)
        c.text(x + 62, 148, tag, size=9, fill=SEM[sem][2], anchor="middle",
               weight="bold", spacing="0.7")
        for j, ln in enumerate(name.split("\n")):
            c.text(x + 62, 172 + j * 15, ln, size=10.4, fill=INK, anchor="middle")
        if i < len(pl) - 1:
            c.arrow(x + 124, 172, x + 137, 172, color=MUTED, sw=1.7)
        x += 137

    # four pillars
    c.band(40, 246, 1100, 34, "THE FOUR TECHNOLOGY PILLARS AND WHAT EACH ONE OWNS", "navy", size=12.5)
    pillars = [
        (40, "JAVA I/O  ·  Chapters 4–9", "teal", [
            "byte vs character streams",
            "buffering and wrapper layers",
            "data streams: typed records",
            "byte-array: in-memory payloads",
            "piped streams: thread hand-off",
            "serialization: state capture",
            "File metadata for discovery",
        ]),
        (320, "JDBC & SQL  ·  Chapters 10–14", "red", [
            "DriverManager + driver",
            "Connection lifecycle",
            "PreparedStatement binding",
            "ResultSet row mapping",
            "SQLException handling",
            "commit / rollback",
            "optional-database isolation",
        ]),
        (600, "SWING & EVENTS  ·  Chapters 15–16", "purple", [
            "JFrame / JPanel / JTable",
            "layouts: Border, Grid, Split",
            "ActionListener → command",
            "AbstractTableModel",
            "custom paintComponent",
            "event-dispatch thread rule",
            "invokeLater hand-off",
        ]),
        (880, "CONFIG & RELATED  ·  Chapters 17–19", "amber", [
            "Maven pom.xml + lifecycle",
            "dependencies → classpath",
            "shade → runnable jar",
            "XML, namespaces, XSD",
            "annotations as metadata",
            "POJO vs JavaBean",
            "JdbcTemplate as an abstraction",
        ]),
    ]
    for x, head, sem, items in pillars:
        c.band(x, 296, 260, 34, head, sem, size=10.6)
        y = 340
        for it in items:
            c.rect(x, y, 260, 30, fill=PAPER, stroke=BORDER, rx=6, sw=1)
            c.circle(x + 17, y + 15, 4, fill=SEM[sem][2], stroke=SEM[sem][2])
            c.text(x + 29, y + 19, it, size=10, fill=BODY)
            y += 34

    # connecting questions
    c.band(40, 596, 1100, 34, "THE QUESTIONS THAT CONNECT THE PILLARS  ·  the ones examiners actually ask", "navy", size=12.5)
    qs = [
        "Why does an application need both file logs and a database?",
        "What is the role of a JDBC driver, and why can it be swapped?",
        "How does PreparedStatement bind values, and why does that stop SQL injection?",
        "How does a character stream differ from a byte stream, and when is each right?",
        "How does a piped stream relate to multithreading?",
        "How do database results reach a GUI without freezing it?",
        "Why does Spring JdbcTemplate not remove the need for JDBC?",
        "How do Maven dependencies relate to database-driver availability?",
    ]
    y = 646
    for i, q in enumerate(qs):
        col = i % 2
        row = i // 2
        bx = 40 + col * 560
        by = y + row * 46
        c.rect(bx, by, 540, 38, fill=CANVAS, stroke=BORDER, rx=7, sw=1)
        c.circle(bx + 20, by + 19, 11, fill=NAVY, stroke=NAVY)
        c.text(bx + 20, by + 23, str(i + 1), size=10, fill=PAPER, anchor="middle",
               weight="bold")
        c.text(bx + 38, by + 23, q, size=10.4, fill=BODY)

    c.box(40, 830, 1100, 40, "Read the pillars as one system: I/O carries and stores, JDBC queries and preserves, Swing presents, configuration makes it run.",
          None, sem="teal", title_size=11.6, rx=8)
    c.save("d29_revision_map", SVG, PNG, 1.9)


ALL = [d19_swing_component_tree, d20_swing_event_flow, d21_login_example,
       d22_maven_build, d23_xml_namespaces_schema, d24_pojo_vs_bean,
       d25_raw_vs_spring, d26_annotation_bean_wiring, d27_end_to_end_sequence,
       d28_dependency_graph, d29_revision_map]
