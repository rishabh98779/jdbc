"""Front matter: cover, table of contents, how to use this book."""
from . import *

TOC = [
    ("PART I — UNDERSTANDING THE SYSTEM", [
        ("1", "The Complete Java System: From Data Input to a Working Application", "ch1",
         ["The problem BasinWatch solves", "The verified runtime architecture",
          "The Java Concepts Connection Map", "How to read this book"]),
        ("2", "Java Application Structure and Core Object Concepts", "ch2",
         ["Classes, objects, state and behaviour", "Interfaces and polymorphism",
          "Inheritance where it is justified", "Enums, records and validation",
          "POJO versus JavaBean", "How BasinWatch divides responsibility"]),
        ("3", "How Java Components Communicate", "ch3",
         ["Six distinct communication mechanisms", "Method calls and shared objects",
          "Streams, events, queues and threads", "Database operations as communication",
          "Choosing the right mechanism"]),
    ]),
    ("PART II — JAVA I/O AND PERSISTENT FILES", [
        ("4", "What Is a Stream?", "ch4",
         ["Source, destination and direction", "Byte streams versus character streams",
          "The four I/O hierarchies", "The decorator idea"]),
        ("5", "Reading and Writing Files", "ch5",
         ["File streams and character streams", "Constructors and methods",
          "Complete read and write workflows", "Resource management and exceptions"]),
        ("6", "Buffering, Data Streams and Stream Wrappers", "ch6",
         ["Why buffering exists", "Layering wrappers", "Typed binary records",
          "Reading a typed record back"]),
        ("7", "In-Memory and Piped Streams", "ch7",
         ["Byte-array streams", "Piped streams and threads",
          "The producer–consumer model", "Where BasinWatch uses each"]),
        ("8", "Serialization, Deserialization and Session Persistence", "ch8",
         ["Object serialization and deserialization", "serialVersionUID and transient",
          "Validation, versioning and safety", "How BasinWatch restores a session"]),
        ("9", "How BasinWatch Uses Java I/O", "ch9",
         ["The operational log", "The typed sensor archive",
          "Session saves and the save catalogue", "Reports and file metadata"]),
    ]),
    ("PART III — DATABASES AND JDBC", [
        ("10", "Why Databases and JDBC Exist", "ch10",
         ["Memory, files and structured storage", "Tables, rows and SQL",
          "Why an application uses more than one store", "Where JDBC fits"]),
        ("11", "JDBC Architecture and Drivers", "ch11",
         ["The JDBC architecture", "The four driver types",
          "Connections and the driver's job", "BasinWatch's driver"]),
        ("12", "SQL Execution Through JDBC", "ch12",
         ["Connection, Statement and PreparedStatement", "ResultSet and row mapping",
          "CRUD operations", "The complete execution lifecycle",
          "SQLException and resource cleanup"]),
        ("13", "Database Transactions and Reliable Persistence", "ch13",
         ["Transaction boundaries", "commit and rollback",
          "Consistency between related rows", "BasinWatch's mission transaction"]),
        ("14", "How BasinWatch Uses JDBC and SQLite", "ch14",
         ["The database architecture", "The schema",
          "Repositories and SQL", "Tracing a history record",
          "Why the database is optional"]),
    ]),
    ("PART IV — SWING AND THE USER INTERFACE", [
        ("15", "Swing Fundamentals and Event-Driven Programming", "ch15",
         ["Containers and components", "Layout managers",
          "Listeners and events", "The lecture-note login application",
          "Custom painting"]),
        ("16", "Connecting Application Logic, JDBC and Swing", "ch16",
         ["From a click to a command", "Futures and the event-dispatch thread",
          "Showing database results safely", "Background work and repainting"]),
    ]),
    ("PART V — CONFIGURATION AND RELATED TECHNIQUES", [
        ("17", "Maven, pom.xml and Project Dependencies", "ch17",
         ["What a build tool does", "The pom.xml structure",
          "The build lifecycle", "Packaging a runnable jar",
          "How the JDBC driver reaches the classpath"]),
        ("18", "XML, Schemas, Namespaces, Annotations and JavaBeans", "ch18",
         ["XML as a document tree", "Namespaces", "XML Schema",
          "Annotations as metadata", "POJO, JavaBean and framework wiring"]),
        ("19", "Raw JDBC versus Spring JdbcTemplate", "ch19",
         ["The repetitive JDBC pattern", "JdbcTemplate and RowMapper",
          "DriverManagerDataSource and the DataSource idea",
          "Side-by-side comparison with BasinWatch"]),
    ]),
    ("PART VI — PUTTING EVERYTHING TOGETHER", [
        ("20", "End-to-End BasinWatch Architecture Walkthrough", "ch20",
         ["Scenario A — an observation, fully traced",
          "Scenario B — a dispatch and its transaction",
          "Scenario C — save, exit and restore",
          "Scenario D — reading history into the table",
          "The dependency graph"]),
        ("21", "Final Integration Exercise", "ch21",
         ["The eight questions", "Guided walkthrough of the code",
          "Where each syllabus concept lives", "Design alternatives"]),
    ]),
    ("REVISION, GLOSSARY AND REFERENCE", [
        ("R", "Comparison Tables and Chapter Summaries", "chrev",
         ["Twelve essential comparison tables", "One-page chapter summaries"]),
        ("V", "Viva and Theory Questions", "chviva",
         ["Definitions and distinctions", "Mechanisms and code",
          "Integration and architecture questions"]),
        ("E", "Programming and Tracing Exercises", "chex",
         ["Output prediction", "Debugging and repair",
          "Tracing and architecture interpretation"]),
        ("G", "High-Yield Revision, Glossary and Reference", "chgloss",
         ["Key definitions", "Essential classes and method signatures",
          "Common mistakes", "Glossary", "Source coverage matrix"]),
    ]),
]


def _toc() -> str:
    rows = []
    for part, chapters in TOC:
        rows.append(f'<div class="toc-part">{part}</div>')
        for num, title, anchor, subs in chapters:
            label = {"R": "Revision", "V": "Viva", "E": "Exercises",
                     "G": "Glossary"}.get(num, num)
            rows.append(
                f'<div class="toc-line"><span class="num">{label}</span>'
                f'<span class="t"><a href="#{anchor}">{title}</a></span>'
                f'<span class="dots"></span>'
                f'<span class="pg"><a href="#{anchor}"></a></span></div>')
            for s in subs:
                rows.append(f'<div class="toc-sub"><span>{s}</span>'
                            f'<span class="dots"></span>'
                            f'<span class="pg"><a href="#{anchor}"></a></span></div>')
    return "".join(rows)


HTML = f"""
<!-- ============================= COVER ============================= -->
<div class="cover">
  <div class="cover-band"></div>
  <div class="cover-inner">
    <div class="cover-eyebrow">INTEGRATED VISUAL NOTES · JAVA · THIRD SEMESTER</div>
    <h1>Java Concepts<br><span class="accent">Integrated Visual Notes</span></h1>
    <div class="subtitle">Streams, files, serialization, threads, JDBC, SQLite,
      Swing, Maven and Spring — taught as one connected system.</div>
    <div class="rule"></div>
    <div class="blurb">
      Most Java material teaches each topic in isolation. This book does the opposite.
      It follows <b>one real application</b> — <b>BasinWatch</b>, an offline floodplain
      operations console — from the moment a sensor observation enters a piped stream to
      the moment a restored session reappears on screen. Every technology is explained
      on its own terms first, then placed in the architecture that gives it a purpose.
      <br><br>
      Built for examination preparation, for coding reference, and for the viva in which
      you must explain how your application actually works.
    </div>
  </div>
  <div class="cover-tags">
    <span>Java I/O streams</span><span>File handling</span><span>Serialization</span>
    <span>Piped streams</span><span>Threads &amp; monitors</span>
    <span>JDBC &amp; SQL</span><span>Transactions</span><span>SQLite</span>
    <span>Swing &amp; events</span><span>Maven</span><span>XML &amp; XSD</span>
    <span>Annotations</span><span>JavaBeans</span><span>Spring JdbcTemplate</span>
  </div>
  <div class="cover-foot">
    <span class="r">29 original diagrams</span>
    21 chapters · 6 parts · 1 connected system · BasinWatch case study
  </div>
</div>

<!-- ============================= TOC ============================= -->
<div class="toc" id="toc">
  <h2>Table of Contents</h2>
  <div class="sub">One book, one chapter sequence, one glossary, one revision section.</div>
  {_toc()}
</div>

<!-- ============================= HOW TO USE ============================= -->
<div class="chapter" id="howto">
  <div class="chapter-num">BEFORE YOU BEGIN</div>
  <h2 class="chapter-title">How to use this book</h2>
  <p class="chapter-deck">A short guide to the structure, the labels, and the fastest
  route through the material for a specific purpose.</p>

  <h3><span class="n">1</span>The book has one spine, not two</h3>
  <p>This is a single volume. It is not an I/O book and a database book sharing a cover.
  Part I establishes the architecture of one application. Parts II to V teach the
  technologies that make each part of that architecture work. Part VI returns to the
  whole system and traces real data through it. The revision section at the end is a
  single coordinated set of comparison tables, questions and exercises covering the
  entire scope.</p>

  <h3><span class="n">2</span>What every chapter assumes</h3>
  <p>Chapters are written for a third-semester Computer Science student who can already
  declare a class, write a loop and call a method. No prior exposure to streams, JDBC or
  Swing is assumed. Where a chapter depends on an earlier one, a
  <b>CONNECTION TO ANOTHER CONCEPT</b> box says so explicitly and tells you where to look.</p>

  <h3><span class="n">3</span>The eight labels you will see</h3>
  <p>Every explanatory box in this book carries one of a small set of labels. The label is
  a promise about the kind of claim being made, and the difference between them matters.</p>
  {table(
    ["Label", "What it means", "Trust level"],
    [
      ["<b>FROM THE LECTURE NOTES</b>", "Terminology, definitions and examples that come from the source lecture material.", "Source content"],
      ["<b>CONCEPT EXPLAINED FURTHER</b>", "Additional explanation added by this book to make the concept complete or precise.", "Supplementary"],
      ["<b>BASINWATCH IN PRACTICE</b>", "A claim verified against the actual source code of the BasinWatch repository.", "Verified in code"],
      ["<b>RELATED TECHNIQUE — NOT USED IN BASINWATCH</b>", "A real technique from the syllabus or the wider ecosystem that this particular project does not implement.", "Taught, not used here"],
      ["<b>CONNECTION TO ANOTHER CONCEPT</b>", "An explicit link between this topic and another topic in the book.", "Cross-reference"],
      ["<b>IMPORTANT DISTINCTION</b>", "Two things that are often confused, stated side by side.", "Clarification"],
      ["<b>COMMON MISTAKE</b>", "An error students and programmers actually make, and how to avoid it.", "Warning"],
      ["<b>TECHNICAL CLARIFICATION</b>", "Where a lecture-note statement is dated, incomplete or questionable, with the modern position stated fairly.", "Correction"],
    ], caption="<b>Table 0.1</b> — The explanatory labels used throughout the book.")}
  <p>Two further labels appear inside code walkthroughs: <b>EXAM TIP</b> marks something
  that is frequently asked, and <b>VISUAL WALKTHROUGH</b> introduces a diagram reading order.</p>

  <h3><span class="n">4</span>Where the code comes from</h3>
  <p>Java listings fall into three clearly separated groups, and each listing says which
  group it belongs to:</p>
  <ul>
    <li><b>Verified BasinWatch code</b> — copied from the repository at
      <span class="mono">github.com/Rishu07368/basinwatch</span> and quoted as it actually
      appears, sometimes trimmed to the relevant lines. Captions say
      <i>"from BasinWatch"</i> and name the file.</li>
    <li><b>Lecture-note style examples</b> — small programs in the shape the notes use,
      including the Swing login application. Captions say <i>"lecture-note style"</i>.</li>
    <li><b>Illustrative examples</b> — short programs written for this book to demonstrate
      a syllabus concept the project does not itself exercise. Captions say
      <i>"illustrative"</i>.</li>
  </ul>
  {mistake("""<p>Nothing in this book is presented as verified project behaviour unless the
  source file was read. Where a plausible-sounding claim could not be confirmed — for
  example, that BasinWatch uses Spring, or that it stores passwords — the book says so
  plainly rather than inventing it. If you are reading this to prepare for a viva, that
  discipline is itself worth copying.</p>""")}

  <h3><span class="n">5</span>Four routes through the book</h3>
  {table(
    ["If your goal is…", "Read", "Then"],
    [
      ["Pass an I/O and file-handling examination",
       "Chapters 4, 5, 6, 7, 8, then 9",
       "Revision comparison tables and the I/O viva questions"],
      ["Pass a JDBC and database examination",
       "Chapters 10, 11, 12, 13, then 14",
       "The JDBC comparison tables, transaction questions and SQL exercises"],
      ["Explain your project in a viva",
       "Chapter 1, then 20 and 21",
       "Chapter 2 for object concepts, Chapter 16 for the UI path"],
      ["Understand how it all fits together",
       "Read straight through, Parts I to VI",
       "Finish with Chapter 21 and the high-yield revision section"],
    ], caption="<b>Table 0.2</b> — Four reading routes.")}

  <h3><span class="n">6</span>The BasinWatch repository</h3>
  <p>BasinWatch is an offline Java desktop simulation that monitors a fictional flood
  basin, processes incoming observations, coordinates limited response resources, keeps
  operational history, and presents everything through a Swing interface. It is a
  <i>planning simulation</i>: it does not forecast real floods, control real equipment, or
  connect to real services. It is a deliberately bounded teaching artefact that
  nevertheless uses each technology for a genuine reason.</p>
  <p>The project is built with Java 17 and Maven, uses only standard <span class="mono">java.io</span>,
  <span class="mono">java.util.concurrent</span>, Swing and raw JDBC, and stores its optional
  history in a local SQLite file. That last sentence is worth remembering, because it
  determines which chapters can say <i>"used in BasinWatch"</i> and which must say
  <i>"related technique"</i>.</p>
  {practice("""<p>The repository files referenced throughout are real:
  <span class="mono">src/main/java/com/basinwatch/{app,domain,engine,io,db,learning}</span>.
  When a chapter quotes a method, you can open the file and find it. That is the standard
  this book holds itself to.</p>""")}

  <h3><span class="n">7</span>What this book deliberately does not claim</h3>
  <ul>
    <li>It does not claim that BasinWatch uses Spring, JPA, Hibernate, JavaFX, a web
      framework, or a remote database server. It uses none of them.</li>
    <li>It does not claim that the lecture notes contained every sentence here. Lecture
      content and supplementary explanation are labelled differently, on purpose.</li>
    <li>It does not present illustrative code as tested project code.</li>
    <li>It does not treat thread priority, serialization, or SQL string building as safe
      by default; each is discussed with its real limitations.</li>
  </ul>

  <div class="summary"><span class="tag">START HERE</span>
  <ul>
    <li>Read Chapter 1 before anything else. It gives you the mental model every later
      chapter refers back to.</li>
    <li>Keep Diagram 1 (the architecture) and Diagram 2 (the connection map) nearby.</li>
    <li>When a chapter says <b>CONNECTION TO ANOTHER CONCEPT</b>, follow the link — that is
      where the integrated understanding lives.</li>
  </ul></div>
</div>
</div>
"""
