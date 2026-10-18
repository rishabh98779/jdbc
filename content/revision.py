"""Revision, Viva, Exercises, Glossary and Reference."""
from . import *

R = []
V = []
E = []
G = []

# ======================================================================
# R — COMPARISON TABLES AND CHAPTER SUMMARIES
# ======================================================================
R.append("""
<div class="chapter" id="chrev">
  <div class="chapter-num">REVISION</div>
  <h2 class="chapter-title">Comparison Tables and Chapter Summaries</h2>
  <p class="chapter-deck">The twelve comparisons that carry the most marks, followed by a
  one-page summary of every chapter in the book.</p>
""")

R.append("""
<h3><span class="n">R.1</span>The twelve essential comparisons</h3>
<p>Each of these is a question an examiner can ask directly. Learn the table, but more importantly learn
the <i>axis</i> of each comparison — that is what the question is really testing.</p>

<h4 class="plain">1. Byte streams versus character streams</h4>
""")

R.append(table(
  ["", "Byte stream", "Character stream"],
  [
    ["Roots", "<span class='mono'>InputStream</span>, <span class='mono'>OutputStream</span>", "<span class='mono'>Reader</span>, <span class='mono'>Writer</span>"],
    ["Unit", "8-bit byte", "16-bit character"],
    ["Encoding", "None", "A charset converts characters to bytes"],
    ["Line methods", "None", "<span class='mono'>readLine()</span>, <span class='mono'>newLine()</span>"],
    ["Use for", "Binary data, typed values, serialized objects", "Text a human will read"],
    ["Project example", "<span class='mono'>SensorArchive</span>, <span class='mono'>SnapshotStore</span>", "<span class='mono'>OperationalJournal</span>, <span class='mono'>ReportWriter</span>"],
  ],
  caption="<b>Table R.1</b> — The byte/character decision."))

R.append("""
<h4 class="plain">2. The file and memory stream classes</h4>
""")

R.append(table(
  ["Purpose", "Byte input", "Byte output", "Character input", "Character output"],
  [
    ["A file", "<span class='mono'>FileInputStream</span>", "<span class='mono'>FileOutputStream</span>", "<span class='mono'>FileReader</span>", "<span class='mono'>FileWriter</span>"],
    ["Memory", "<span class='mono'>ByteArrayInputStream</span>", "<span class='mono'>ByteArrayOutputStream</span>", "<span class='mono'>StringReader</span>", "<span class='mono'>StringWriter</span>"],
    ["Another thread", "<span class='mono'>PipedInputStream</span>", "<span class='mono'>PipedOutputStream</span>", "<span class='mono'>PipedReader</span>", "<span class='mono'>PipedWriter</span>"],
    ["Adding a capability", "<span class='mono'>FilterInputStream</span>", "<span class='mono'>FilterOutputStream</span>", "<span class='mono'>FilterReader</span>", "<span class='mono'>FilterWriter</span>"],
  ],
  caption="<b>Table R.2</b> — The four-by-four grid of stream classes."))

R.append("""
<h4 class="plain">3. Buffered versus unbuffered streams</h4>
""")

R.append(table(
  ["", "Unbuffered", "Buffered"],
  [
    ["Reads per 8 KB", "One system call per <span class='mono'>read()</span>", "One system call per buffer refill"],
    ["Line methods", "Not available", "<span class='mono'>readLine()</span> and <span class='mono'>newLine()</span>"],
    ["<span class='mono'>flush()</span> matters?", "No — data goes straight out", "Yes — data may sit in the array"],
    ["Risk if not closed", "Minor", "Silent data loss of buffered content"],
    ["Project use", "Never used alone for files", "Every file stream in the project"],
  ],
  caption="<b>Table R.3</b> — Buffering, and why it is not optional."))

R.append("""
<h4 class="plain">4. Data streams versus object serialization</h4>
""")

R.append(table(
  ["", "DataInputStream / DataOutputStream", "ObjectInputStream / ObjectOutputStream"],
  [
    ["What is written", "Primitives and strings, in a fixed order", "An object graph, with class descriptors"],
    ["Format defined by", "You — the sequence of calls", "The JDK"],
    ["Readable if the class changes?", "Only if the order is unchanged", "Yes, with an explicit <span class='mono'>serialVersionUID</span>"],
    ["Constructor called on read?", "Not applicable", "<b>No</b> — which is why validation must be explicit"],
    ["Security concern", "Low — no classes are named in the stream", "<b>High</b> — the stream names classes to instantiate"],
    ["Project example", "<span class='mono'>SensorArchive</span>", "<span class='mono'>SnapshotStore</span>"],
  ],
  caption="<b>Table R.4</b> — Two ways to persist structured data."))

R.append("""
<h4 class="plain">5. The six communication mechanisms</h4>
""")

R.append(table(
  ["Mechanism", "Direction", "Blocks?", "Crosses threads?", "Project example"],
  [
    ["Method call", "two-way", "briefly", "no", "<span class='mono'>model.process(event)</span>"],
    ["Monitor", "two-way", "on the lock", "yes", "<span class='mono'>ResourceAllocator.tryReserve</span>"],
    ["Stream", "one-way", "when full or empty", "usually", "The pipe; all file access"],
    ["Queue", "one-way", "when full or empty", "yes", "<span class='mono'>EventBuffer</span>"],
    ["Callback", "inverted", "no", "may arrive anywhere", "Snapshot, status and database listeners"],
    ["Database operation", "request/response", "yes unless offloaded", "yes", "Writes queued, reads as futures"],
  ],
  caption="<b>Table R.5</b> — Choosing a communication mechanism."))

R.append("""
<h4 class="plain">6. File persistence versus database persistence</h4>
""")

R.append(table(
  ["", "File", "Database"],
  [
    ["Structure", "Whatever format you invent", "Tables, columns and declared types"],
    ["Selective read", "Read and filter everything", "<span class='mono'>WHERE</span> plus an index"],
    ["Aggregation", "Application code", "SQL aggregate functions"],
    ["Concurrency", "Effectively one writer", "Locking and isolation levels"],
    ["Atomic multi-part change", "Write to a temporary file and rename", "A transaction"],
    ["Readable without tooling", "Yes, for text formats", "No — needs a client"],
    ["Restores full application state", "Yes, via a snapshot", "Only by replaying or reconstructing"],
    ["Project use", "Log, archive, snapshot, reports", "Optional history in SQLite"],
  ],
  caption="<b>Table R.6</b> — The two persistence mechanisms and what each is good at."))

R.append("""
<h4 class="plain">7. Statement, PreparedStatement and CallableStatement</h4>
""")

R.append(table(
  ["", "Statement", "PreparedStatement", "CallableStatement"],
  [
    ["Values", "Concatenated into the SQL text", "Bound with typed setters", "Bound as input or registered as output"],
    ["Pre-parsed", "No", "<b>Yes</b>", "Yes"],
    ["Injection-safe", "<b>No</b>", "<b>Yes</b>", "<b>Yes</b>"],
    ["Reusable efficiently", "No", "<b>Yes</b>", "Yes"],
    ["Project use", "Schema DDL in <span class='mono'>DatabaseInitializer</span>", "Every repository method", "Not used — no stored procedures"],
  ],
  caption="<b>Table R.7</b> — The three statement types."))

R.append("""
<h4 class="plain">8. The four JDBC driver types</h4>
""")

R.append(table(
  ["Type", "Approach", "Status today"],
  [
    ["1 — JDBC–ODBC bridge", "Native ODBC driver called through Java", "<b>Removed</b> from the JDK"],
    ["2 — Native-API", "Calls the vendor's native client library", "Rarely used; needs native libraries"],
    ["3 — Network protocol", "Talks to a middleware server", "Largely converged with type 4"],
    ["4 — Thin driver", "Pure Java, speaks the database protocol directly", "<b>The modern default</b>; SQLite's driver is type 4"],
  ],
  caption="<b>Table R.8</b> — The four driver types."))

R.append("""
<h4 class="plain">9. Execution methods and their results</h4>
""")

R.append(table(
  ["Method", "Returns", "Use for"],
  [
    ["<span class='mono'>executeQuery()</span>", "<span class='mono'>ResultSet</span>", "<span class='mono'>SELECT</span>"],
    ["<span class='mono'>executeUpdate()</span>", "<span class='mono'>int</span> — rows affected", "<span class='mono'>INSERT</span>, <span class='mono'>UPDATE</span>, <span class='mono'>DELETE</span>, DDL"],
    ["<span class='mono'>execute()</span>", "<span class='mono'>boolean</span> — is a ResultSet available", "When the kind of statement is unknown"],
    ["<span class='mono'>executeBatch()</span>", "<span class='mono'>int[]</span> — counts per statement", "Bulk operations"],
  ],
  caption="<b>Table R.9</b> — The four execution methods."))

R.append("""
<h4 class="plain">10. Raw JDBC versus Spring JdbcTemplate</h4>
""")

R.append(table(
  ["", "Raw JDBC", "JdbcTemplate"],
  [
    ["Connection handling", "Written by hand", "Delegated to the template"],
    ["Resource closing", "try-with-resources at every site", "Automatic"],
    ["Parameter binding", "Typed setters, hand-written", "From the argument list"],
    ["Row mapping", "A loop in the method", "A <span class='mono'>RowMapper</span> lambda"],
    ["Exceptions", "<span class='mono'>SQLException</span> (checked)", "<span class='mono'>DataAccessException</span> (unchecked)"],
    ["Dependencies", "The driver only", "Spring Core, Spring JDBC, the driver"],
    ["Used in BasinWatch?", "<b>Yes</b>", "<b>No</b>"],
  ],
  caption="<b>Table R.10</b> — Two levels of JDBC abstraction."))

R.append("""
<h4 class="plain">11. POJO versus JavaBean</h4>
""")

R.append(table(
  ["", "POJO", "JavaBean"],
  [
    ["Convention", "None", "No-argument constructor, private fields, public get/set accessors"],
    ["Serializable", "Not required", "Conventionally yes"],
    ["Can be a record?", "Yes", "<b>No</b> — records have no no-argument constructor or setters"],
    ["Purpose of the convention", "None needed", "Allows a framework to create and populate by reflection"],
    ["Project example", "<span class='mono'>SensorReading</span>, <span class='mono'>ZoneSnapshot</span>", "None — no framework is used"],
  ],
  caption="<b>Table R.11</b> — POJO and JavaBean."))

R.append("""
<h4 class="plain">12. Swing event handling essentials</h4>
""")

R.append(table(
  ["Concept", "Meaning", "Project example"],
  [
    ["Event-dispatch thread", "The single thread for events and painting", "Every listener in <span class='mono'>MainFrame</span>"],
    ["Listener", "An object registered to receive an event", "<span class='mono'>ActionListener</span> on each button"],
    ["Functional interface", "One abstract method, so a lambda works", "<span class='mono'>ActionListener</span>, <span class='mono'>Runnable</span>"],
    ["Layout manager", "Decides where children go", "<span class='mono'>BorderLayout</span> and <span class='mono'>JSplitPane</span>"],
    ["Custom painting", "Override <span class='mono'>paintComponent</span>", "<span class='mono'>BasinMapPanel</span>"],
    ["Off-EDT hand-off", "<span class='mono'>SwingUtilities.invokeLater</span>", "Every engine callback"],
    ["Table model", "Supplies data to a <span class='mono'>JTable</span>", "<span class='mono'>HistoryTableModel</span>"],
  ],
  caption="<b>Table R.12</b> — The twelve comparisons, and the last one."))

R.append("""
<h3><span class="n">R.2</span>One-page chapter summaries</h3>
<p>Each entry is the smallest complete statement of what a chapter established. If any line is not
familiar, that is the chapter to reread.</p>
""")

R.append(table(
  ["Ch.", "In one paragraph"],
  [
    ["<b>1</b>", "BasinWatch is a single-process offline floodplain console in six layers: operator and interface, engine commands, domain and engine, sensor input path, file persistence, and an optional JDBC layer. Six threads do background work and publish immutable snapshots to the event-dispatch thread. Technologies meet at exactly two boundaries: the accepted event and the published snapshot."],
    ["<b>2</b>", "Encapsulation is enforced with access modifiers; one interface unifies three event types; polymorphism is expressed as pattern matching; inheritance is used only where a framework contract requires it; enums carry their own data; records provide validated immutable values; a JavaBean adds conventions a framework needs and a record cannot have."],
    ["<b>3</b>", "Components communicate in six distinct ways: method call, shared object under a monitor, stream, queue with condition waiting, listener callback, and database operation. Each has different blocking and threading behaviour. A method call must never block on external work; condition waits must be loops that hold the monitor and use <span class='mono'>notifyAll</span>."],
    ["<b>4</b>", "A stream is an ordered one-directional sequence consumed incrementally. Four abstract roots: <span class='mono'>InputStream</span>, <span class='mono'>OutputStream</span>, <span class='mono'>Reader</span>, <span class='mono'>Writer</span>. Bytes preserve data exactly; characters pass through a charset and are right for text. <span class='mono'>read()</span> returns <span class='mono'>int</span> so that -1 can mean end of stream."],
    ["<b>5</b>", "A <span class='mono'>Path</span> names a file; only a stream reads it. Opening for output truncates unless append is requested. A complete write is create, open, write, flush, close; a complete read is check, open with an explicit charset, loop on <span class='mono'>readLine() != null</span>, close. <span class='mono'>flush()</span> pushes data onward; <span class='mono'>close()</span> flushes and releases."],
    ["<b>6</b>", "A buffer turns many small operations into few large ones. Wrapper classes add one capability each by taking another stream in their constructor. <span class='mono'>readLine()</span> exists only on <span class='mono'>BufferedReader</span>. Data streams write primitives in a fixed order that <i>is</i> the schema, so the read order must match exactly; a usable binary format has a magic number, a version and self-describing strings."],
    ["<b>7</b>", "Byte-array streams use the whole stream API with no device. A pipe is a matched writer/reader pair with a bounded buffer, intended for two threads; it provides back-pressure and a natural end-of-stream signal. Shutdown order is stop the producer, close the writer, join the consumer, close the queue."],
    ["<b>8</b>", "Serialization writes an object graph; deserialization reconstructs it without calling constructors. <span class='mono'>transient</span> and <span class='mono'>static</span> fields are skipped; an explicit <span class='mono'>serialVersionUID</span> prevents unrelated recompiles from invalidating saves. Because constructors are bypassed, a reader needs four defences: bound the size, filter the classes, check the version, validate the result. BasinWatch writes to a temporary file and moves it into place."],
    ["<b>9</b>", "Four file mechanisms answer four questions: the log records what happened, the archive records exact measurements, the snapshot restores state, the report communicates. All paths derive from <span class='mono'>AppPaths</span>. None of the four can substitute for another, because the format determines which questions the file can answer."],
    ["<b>10</b>", "Data lives in memory, in files, or in a database; the decisive difference is selective access through indexes. BasinWatch uses all three because different questions need different mechanisms. A table declares columns, types and constraints; an index makes a query fast; JDBC is the interface layer that lets Java talk to any database."],
    ["<b>11</b>", "JDBC splits into fixed interfaces in <span class='mono'>java.sql</span> and a vendor driver that implements them. A driver recognises URLs, opens connections, translates calls and translates results back. There are four driver types; the pure-Java thin driver is the modern default. BasinWatch builds its URL in one place and reports availability as a boolean."],
    ["<b>12</b>", "A query involves a Connection, a Statement and possibly a ResultSet, all closed. <span class='mono'>PreparedStatement</span> is the default: safer against injection, pre-parsed and reusable. Placeholders are 1-based and each needs a typed setter. <span class='mono'>executeQuery</span> returns rows, <span class='mono'>executeUpdate</span> returns a count. Map rows into your own objects inside the loop."],
    ["<b>13</b>", "A transaction groups operations so all take effect or none do; the ACID properties are atomicity, consistency, isolation and durability. JDBC is in autocommit mode by default; <span class='mono'>setAutoCommit(false)</span> begins a transaction you control. A transaction belongs to a connection, so every statement in it must share that connection. BasinWatch records a dispatch in one transaction, and runs all database work on one thread so isolation anomalies cannot arise."],
    ["<b>14</b>", "Four classes form the database layer: connection management, schema creation, service coordination, and per-table SQL. Four tables carry readings, missions, resource usage and events, each with a timestamp. Schema creation is idempotent. The database is optional because availability is a boolean, writes are queued on their own thread, and reads on an unavailable database return an empty list."],
    ["<b>15</b>", "Swing is event-driven: handlers are declared and the framework calls them. Components are containers or simple components, arranged by layout managers. All event handling and painting run on the event-dispatch thread, which is why a slow handler freezes the window. The lecture-note login application validates input, reads the password as a char array and starts on the EDT; its hard-coded credential is a UI exercise, not a security design."],
    ["<b>16</b>", "A listener asks the engine and returns; slow work runs on a background thread; the result arrives as a future; and the callback posts to the EDT before touching any component. A complete click-to-table path crosses the EDT, the database thread and the EDT again. A <span class='mono'>JTable</span> renders whatever its <span class='mono'>TableModel</span> supplies, and the model must fire a change event."],
    ["<b>17</b>", "A build tool resolves dependencies, compiles, tests and packages. Maven identifies libraries by groupId, artifactId and version. BasinWatch has exactly one dependency. The driver reaches the runtime classpath as a Maven dependency and registers itself through a service file, which the shade plugin's <span class='mono'>ServicesResourceTransformer</span> must preserve in the uber jar."],
    ["<b>18</b>", "XML is a tree of elements, attributes and text; a document is well-formed if it follows the syntax and valid if it conforms to a schema. A namespace URI is an identifier, not an address. Annotations are metadata whose retention policy decides whether a framework can read them at runtime. A JavaBean's conventions exist so a framework can instantiate and populate it reflectively; BasinWatch wires by hand instead."],
    ["<b>19</b>", "Raw JDBC forces the same resource handling into every method; <span class='mono'>JdbcTemplate</span> performs it for you and asks only for SQL and a <span class='mono'>RowMapper</span>. A <span class='mono'>DataSource</span> supplies connections; <span class='mono'>DriverManagerDataSource</span> does not pool and is for teaching and tests. JdbcTemplate is built on the same <span class='mono'>java.sql</span> interfaces, so it removes repetition rather than JDBC. BasinWatch uses raw JDBC only."],
    ["<b>20</b>", "Four scenarios take genuinely different routes: an observation crosses the pipe and fans out to three persistence mechanisms; a dispatch is the only transactional path; a save-and-restore is defensive on the way in; a history read writes nothing. The dependency graph is acyclic, with the domain at the bottom and the interface at the top."],
    ["<b>21</b>", "Eight questions explain any class: purpose, communication, data received, mechanism, effect, survival, failure, and the lecture alternative. Every syllabus concept has a home in the project, and the three most defensible design alternatives are raw JDBC versus JdbcTemplate, files versus a database, and hand wiring versus a dependency-injection framework."],
  ],
  caption="<b>Table R.13</b> — Every chapter in one paragraph.", cls="big"))

R.append("</div>")

# ======================================================================
# V — VIVA AND THEORY QUESTIONS
# ======================================================================
V.append("""
<div class="chapter" id="chviva">
  <div class="chapter-num">VIVA AND THEORY</div>
  <h2 class="chapter-title">Viva and Theory Questions</h2>
  <p class="chapter-deck">Fifty questions with answers, grouped from definitions through mechanisms to
  integration. The last group is the one that separates understanding from memorisation.</p>
""")

V.append("""
<h3><span class="n">V.1</span>Definitions and distinctions</h3>
""")

V.append(qa("Q1. What is a stream?",
"A one-directional, ordered sequence of data with a source or a destination, consumed or produced incrementally rather than all at once. The incrementality is the point: it lets you handle data larger than memory, and data that has no end yet."))

V.append(qa("Q2. State the difference between a byte stream and a character stream.",
"A byte stream carries 8-bit units and applies no interpretation, so it preserves data exactly. A character stream carries 16-bit characters and converts them through a charset, so it is correct for text a human will read. Using a character stream on binary data corrupts it, because byte sequences invalid in the charset are replaced."))

V.append(qa("Q3. Why does <span class='mono'>read()</span> return an <span class='mono'>int</span> rather than a <span class='mono'>byte</span>?",
"Because the end of a stream needs a marker distinct from every legal data value. All 256 byte values are legal data, so widening the return type to <span class='mono'>int</span> makes room for <span class='mono'>-1</span> to mean end of stream."))

V.append(qa("Q4. What is the difference between <span class='mono'>flush()</span> and <span class='mono'>close()</span>?",
"<span class='mono'>flush()</span> pushes buffered data to the destination and leaves the stream usable. <span class='mono'>close()</span> flushes and then releases the underlying resource; further writes after closing throw. Calling <span class='mono'>close()</span> twice is safe."))

V.append(qa("Q5. What is a filter stream?",
"A stream that wraps another stream, taking it as a constructor argument, and adds one capability — buffering, typed reads, object serialization or character decoding. It is the decorator pattern applied to I/O, and it is what makes stream chains composable."))

V.append(qa("Q6. Define serialization and deserialization.",
"Serialization converts an object into a byte sequence containing its class identity and its non-transient field values, recursing into referenced objects. Deserialization reverses the process, reconstructing the object graph."))

V.append(qa("Q7. What do <span class='mono'>transient</span> and <span class='mono'>static</span> mean for serialization?",
"Neither is written to the stream. A <span class='mono'>transient</span> field is skipped deliberately and restores to its default value; a <span class='mono'>static</span> field belongs to the class rather than the instance, so it is not instance state and is not serialized."))

V.append(qa("Q8. What is <span class='mono'>serialVersionUID</span> for?",
"It is the explicit version identity of a serializable class. Without it, the compiler derives one from the class's structure, so adding a method or a field can change it and make previously saved files unreadable with <span class='mono'>InvalidClassException</span>. Declaring it makes compatibility deliberate."))

V.append(qa("Q9. What is a JavaBean, and how does it differ from a POJO?",
"A JavaBean is a POJO that follows conventions — a public no-argument constructor, private fields, public <span class='mono'>get</span>/<span class='mono'>set</span> accessors and usually <span class='mono'>Serializable</span> — so a framework can create and populate it by reflection. Every JavaBean is a POJO; not every POJO is a JavaBean. A record can never be a JavaBean, because it has no no-argument constructor and no setters."))

V.append(qa("Q10. What is JDBC?",
"The Java Database Connectivity API: a set of interfaces in <span class='mono'>java.sql</span> plus a driver-registration mechanism, letting Java code open connections, send SQL and read results without depending on a particular database product."))

V.append(qa("Q11. What is a primary key?",
"The column or columns that uniquely identify each row in a table. It prevents duplicate identities and is the target of references from other tables."))

V.append(qa("Q12. What is an index and why does it matter?",
"An auxiliary structure that lets the database find rows by particular columns without examining every row. It is the reason a selective query is cheap, and it is the main capability a database has that a plain file does not."))

V.append(qa("Q13. What is a transaction?",
"A group of database operations treated as one unit: either all of them take effect or none does. It is what prevents a partially completed change from being visible."))

V.append(qa("Q14. What do the ACID properties mean?",
"Atomicity: all or nothing. Consistency: the database moves between valid states, honouring its constraints. Isolation: concurrent transactions do not see each other's partial work. Durability: a committed change survives a failure."))

V.append(qa("Q15. What is the event-dispatch thread?",
"The single thread on which Swing performs event handling and painting. All component access must happen there, which is why a long-running handler freezes the interface and why callbacks from other threads must post their work to it."))

V.append("""
<h3><span class="n">V.2</span>Mechanisms and code</h3>
""")

V.append(qa("Q16. Why does an application need both file-based logs and a database?",
"Because they answer different questions. A log records what happened, in order, and is readable with a text editor but must be scanned to be queried. A database stores structured rows that can be filtered, ordered and aggregated cheaply through indexes. The log is an audit trail; the database is an index over the same events."))

V.append(qa("Q17. What is the role of a JDBC driver?",
"Four things: recognise its own URLs, open a connection to the database, translate JDBC calls into the database's own protocol, and translate results back into <span class='mono'>ResultSet</span> rows. Everything you call on a <span class='mono'>Connection</span> is implemented by the driver, not by the JDK."))

V.append(qa("Q18. Which JDBC driver type does BasinWatch use, and why does that matter?",
"A type 4 thin driver, <span class='mono'>org.xerial:sqlite-jdbc</span>. It is pure Java, so it needs no native library and no middleware — just a jar on the classpath. That is why the project's entire database configuration is one Maven dependency and one URL string."))

V.append(qa("Q19. How does <span class='mono'>PreparedStatement</span> bind values, and why is that safe?",
"Placeholders written as <span class='mono'>?</span> are numbered from one, and each is filled by a typed setter such as <span class='mono'>setDouble(4, value)</span>. The SQL text is sent to the database and parsed before any value is supplied, so the parser has already decided what is a statement and what is a value. No value can therefore become part of the statement's structure, which is what defeats SQL injection."))

V.append(qa("Q20. What is the difference between <span class='mono'>executeQuery()</span> and <span class='mono'>executeUpdate()</span>?",
"<span class='mono'>executeQuery()</span> runs a statement that produces rows and returns a <span class='mono'>ResultSet</span>. <span class='mono'>executeUpdate()</span> runs a statement that changes rows and returns the number of rows affected as an <span class='mono'>int</span>."))

V.append(qa("Q21. Why must a result set be consumed inside the block that created it?",
"Because it is tied to its statement and its connection, and both are closed at the end of that block. Returning a <span class='mono'>ResultSet</span> from a method that closes its connection produces an object that fails on the first <span class='mono'>next()</span>. The fix is to map each row into your own object inside the loop."))

V.append(qa("Q22. How does a character stream differ from a byte stream in terms of the data it can represent?",
"Neither represents more data — both are sequences of units. The difference is interpretation: a byte stream preserves exact 8-bit values with no mapping, while a character stream applies a charset, so the same character may occupy one or several bytes on disk. Character streams are therefore lossless for text and destructive for binary data."))

V.append(qa("Q23. How does a piped stream relate to multithreading?",
"A pipe is a matched writer/reader pair intended for two different threads: one writes characters, the other reads them, and the pipe's bounded buffer transfers between them. It gives a one-directional contract with back-pressure and a natural end-of-stream signal when the writer closes. Using both ends in one thread is a deadlock, because the reader waits for data only that same thread could write."))

V.append(qa("Q24. What is a condition wait, and what are the four rules for writing one correctly?",
"A condition wait is <span class='mono'>wait()</span> used to pause a thread until a predicate becomes true. The four rules: wait inside a loop that re-tests the predicate, because a woken thread is not guaranteed its condition now holds; hold the object's monitor, since <span class='mono'>wait()</span> requires it; use <span class='mono'>notifyAll()</span> rather than <span class='mono'>notify()</span>, because waiters may have different predicates; and release the monitor while waiting, which <span class='mono'>wait()</span> does and <span class='mono'>sleep()</span> does not."))

V.append(qa("Q25. Why does BasinWatch use a pipe between the feed and the intake rather than a shared list?",
"Because the pipe is a much narrower contract. A shared list would give both threads access to every element and to the list's own methods, so a bug in either could corrupt it. The pipe gives each thread one operation — write a character sequence, read a character sequence — and provides back-pressure for free, since the writer blocks when the buffer is full."))

V.append(qa("Q26. What is the difference between <span class='mono'>writeUTF</span> and <span class='mono'>writeChars</span>?",
"<span class='mono'>writeUTF</span> writes a two-byte length followed by modified UTF-8 bytes, so the string is self-describing and can be read back without knowing its length. <span class='mono'>writeChars</span> writes two bytes per character with no length prefix, so the reader must already know how many characters to read."))

V.append(qa("Q27. Why does a data stream require the read order to match the write order?",
"Because the format contains no field metadata: the sequence of calls <i>is</i> the schema. A <span class='mono'>readDouble()</span> where a <span class='mono'>readInt()</span> was written does not throw — it consumes eight bytes that were never a double and returns a plausible but wrong value. Versioning the format explicitly is the defence."))

V.append(qa("Q28. What four defences does BasinWatch apply when restoring a session?",
"Bound the input size before opening the stream; install an <span class='mono'>ObjectInputFilter</span> that approves only the project's own packages and a small set of JDK packages; check the format version written in the header; and validate the restored domain state, because deserialization bypasses constructors."))

V.append(qa("Q29. Why is the session snapshot written to a temporary file and then moved?",
"So that an interrupted save cannot corrupt an existing snapshot. The temporary file is written completely, then moved into place with <span class='mono'>ATOMIC_MOVE</span>, which replaces the target in one step. A crash mid-save leaves the previous good file intact and an orphaned temporary file."))

V.append(qa("Q30. Why does <span class='mono'>DatabaseManager.isAvailable</span> return a boolean rather than throwing?",
"Because the database is optional. Returning a boolean lets every caller test a value rather than handling an exception to discover availability, and it lets a read return an empty list on an unavailable database so the interface's code path is identical either way."))

V.append("""
<h3><span class="n">V.3</span>Integration and architecture</h3>
""")

V.append(qa("Q31. How do database results reach a GUI?",
"In four steps. A listener on the event-dispatch thread asks the engine for an operation and returns immediately with a <span class='mono'>CompletableFuture</span>. The query runs on the database thread. The future completes there, running its callback on that same thread. The callback wraps its component access in <span class='mono'>SwingUtilities.invokeLater</span>, so the table model is updated on the event-dispatch thread."))

V.append(qa("Q32. Why does Spring JdbcTemplate not eliminate the need for JDBC itself?",
"Because it is built on JDBC. It obtains connections from a <span class='mono'>DataSource</span>, creates <span class='mono'>PreparedStatement</span>s, binds parameters, iterates <span class='mono'>ResultSet</span>s and closes everything — all through the same <span class='mono'>java.sql</span> interfaces. It removes the repetition, not the protocol, and everything you know about parameter binding, result-set iteration and transactions still applies."))

V.append(qa("Q33. How do Maven dependencies relate to database-driver availability?",
"A driver is declared in <span class='mono'>pom.xml</span> by groupId, artifactId and version. Maven resolves it and places it on the compile and runtime classpaths. The driver registers itself through <span class='mono'>META-INF/services/java.sql.Driver</span>, and the shade plugin must be configured with <span class='mono'>ServicesResourceTransformer</span> so that file survives being merged into an uber jar. Without it the classes are present but the registration is lost, and <span class='mono'>DriverManager</span> reports no suitable driver."))

V.append(qa("Q34. Why is it a mistake to let the interface do the work?",
"Three consequences. The event-dispatch thread is blocked for the duration, so the window freezes. The logic cannot be tested without constructing a window. And SQL or file handling spreads across the interface code, so a change to the schema or the file format touches many classes. The project's rule — the interface asks, the engine decides, a worker executes, a snapshot reports — avoids all three."))

V.append(qa("Q35. How does the model stay consistent while workers mutate it and the interface reads it?",
"By publishing immutable snapshots. <span class='mono'>BasinSnapshot</span> and its parts are records whose constructors copy every collection with <span class='mono'>List.copyOf</span> and <span class='mono'>Map.copyOf</span>. The interface therefore reads a value that cannot change underneath it, so no locking is needed on the event-dispatch thread."))

V.append(qa("Q36. Why does the domain package depend on nothing?",
"Because that is what makes it testable and reusable. With no import of Swing, files, SQL or threads, the model can be exercised in a plain unit test with no setup, and the same model could be driven by a different interface or by an automated harness. It is also why the dependency graph has no cycles."))

V.append(qa("Q37. Where exactly do the I/O, JDBC and Swing technologies meet in this application?",
"At two boundaries. The first is the accepted event: after the model processes an event, the engine fans out to the journal, the archive worker and the database queue. The second is the published snapshot: the engine hands an immutable value to every registered listener, whose first action is to post to the event-dispatch thread. Everywhere else the layers are deliberately ignorant of one another."))

V.append(qa("Q38. Why does the application need a transaction when recording a dispatch?",
"Because three related writes must succeed or fail together: the mission row, the resource-usage rows and the audit event. Without a transaction, a failure after the mission insert would leave a running mission with resources that were never deducted, so the resource board would be permanently wrong and the history would not explain why."))

V.append(qa("Q39. Why must every write in a transaction use the same connection?",
"Because a transaction belongs to a connection, not to a statement. Calling <span class='mono'>commit()</span> on one connection has no effect on work done on another, so three repositories each opening their own connection would create three separate transactions and atomicity would be lost — while the code still looked correct."))

V.append(qa("Q40. Why is isolation not a problem in this application?",
"Because all database work runs on a single-threaded executor. There is exactly one writer, so there is never a second transaction to interfere with the first, and no isolation level or locking policy needs to be reasoned about."))

V.append(qa("Q41. What happens to the application if the database is unavailable?",
"Four things, and all four matter. The application still starts, because availability is checked rather than assumed. The history panel shows an empty list and a status message. Every write becomes a no-op because <span class='mono'>enqueue</span> returns early. And the file layer is entirely unaffected, so the log, archive, snapshot and reports are still produced."))

V.append(qa("Q42. Why does a reading reach the database only when the model changed?",
"Because <span class='mono'>BasinZone.apply</span> rejects a reading whose tick is not newer than the last one applied, returning false. The engine writes to the database only when the model changed, so a duplicate or out-of-order observation is not recorded as though it had taken effect. The stale guard in the domain is therefore what makes the history accurate."))

V.append(qa("Q43. Explain the shutdown sequence and why the order matters.",
"Stop the producer, close the writer, join the intake thread, close the queue. Closing the writer is what makes the consumer's <span class='mono'>readLine()</span> return null and its loop end. Joining the consumer before closing the queue ensures accepted events are drained rather than discarded. Closing the writer before stopping the producer would make the producer throw a spurious error, and never closing the writer would leave the consumer blocked forever."))

V.append(qa("Q44. Why is inheritance used so little in this project?",
"Because composition is more flexible and less coupled. The two uses are both framework contracts: <span class='mono'>SensorFeed extends Thread</span> because a feed genuinely owns a thread's lifecycle and needs a name and priority, and the Swing panels extend <span class='mono'>JPanel</span> and <span class='mono'>JFrame</span> because Swing requires it. Everywhere else, objects are composed — <span class='mono'>BasinEngine</span> has an executor, a buffer and a service rather than being one."))

V.append(qa("Q45. What is the difference between <span class='mono'>invokeLater</span> and <span class='mono'>invokeAndWait</span>?",
"<span class='mono'>invokeLater</span> queues a runnable on the event-dispatch thread and returns immediately, so the calling thread continues. <span class='mono'>invokeAndWait</span> queues it and blocks until the event-dispatch thread has run it — which is a deadlock if called from the event-dispatch thread itself. BasinWatch uses <span class='mono'>invokeLater</span> exclusively."))

V.append(qa("Q46. Why does the project not use <span class='mono'>SwingWorker</span>?",
"Because the engine must work without a user interface, so its operations cannot depend on a Swing type. Returning <span class='mono'>CompletableFuture</span> keeps the engine independent of Swing and lets the interface choose how to consume the result. <span class='mono'>SwingWorker</span> is more convenient inside a UI; a future is more flexible outside one."))

V.append(qa("Q47. Is a database always better than a file?",
"No. For a single-user desktop application a database adds a dependency, a schema and a failure mode. BasinWatch treats its database as optional precisely because the file layer already satisfies the essential requirements. The database earns its place by enabling selective queries and aggregation, not by being more modern."))

V.append(qa("Q48. Why does BasinWatch not use Spring?",
"Because for an application of this size the trade is unfavourable. There are six packages and roughly two dozen classes, wired by hand through constructors. Spring would add several dependencies, a component scan and a class of runtime errors in exchange for saving perhaps thirty lines of wiring. It would also make the database layer depend on a framework, when the project's aim is to show raw JDBC."))

V.append(qa("Q49. What is the single most important design decision in the project, and why?",
"The publication of immutable snapshots. It is what allows background threads to mutate the model while the event-dispatch thread renders it, with no locking in the interface and no possibility of a torn read. It is also what keeps the interface's job small — render a value, collect intent, report an outcome."))

V.append(qa("Q50. If you had to change one thing about this architecture, what would it be?",
"A defensible answer names a real trade-off rather than a fault. For example: the database schema declares the mission relationship as a plain column rather than a foreign key, which means a deleted mission could orphan its resource rows; enabling <span class='mono'>PRAGMA foreign_keys</span> and declaring the constraint would fix it. Or: history is retained indefinitely, so a retention or archival policy would be needed before the database grew without bound. Naming a specific consequence is what makes the answer credible."))

V.append("</div>")

# ======================================================================
# E — PROGRAMMING AND TRACING EXERCISES
# ======================================================================
E.append("""
<div class="chapter" id="chex">
  <div class="chapter-num">EXERCISES</div>
  <h2 class="chapter-title">Programming and Tracing Exercises</h2>
  <p class="chapter-deck">Thirty exercises in four groups: predicting output, repairing code, tracing
  data through the system, and interpreting the architecture. Answers are given so you can check
  yourself, but attempt each one first.</p>
""")

E.append("""
<h3><span class="n">E.1</span>Output prediction</h3>
""")

E.append(exercise(1, "What does this print?",
"""<pre>try (ByteArrayOutputStream buffer = new ByteArrayOutputStream();
     DataOutputStream out = new DataOutputStream(buffer)) {
    out.writeInt(4);
    out.writeUTF("AB");
    out.writeDouble(1.0);
    out.flush();
    System.out.println(buffer.size());
}</pre>""",
"The size is <b>16</b> bytes. <span class='mono'>writeInt</span> contributes 4, <span class='mono'>writeUTF(\"AB\")</span> contributes 2 length bytes plus 2 character bytes, and <span class='mono'>writeDouble</span> contributes 8. The lesson is to count from the format rather than guess: a data stream has no field metadata, so these sizes are the only thing that makes the layout predictable."))

E.append(exercise(2, "What does this print?",
"""<pre>String line;
int count = 0;
try (BufferedReader reader = new BufferedReader(new StringReader("a\\nb\\nc"))) {
    while ((line = reader.readLine()) != null) {
        count++;
    }
}
System.out.println(count);</pre>""",
"<b>3</b>. The string contains two newline characters and therefore three lines: <span class='mono'>a</span>, <span class='mono'>b</span> and <span class='mono'>c</span>. The final line has no trailing newline, and <span class='mono'>readLine()</span> still returns it — the fourth call then returns null."))

E.append(exercise(3, "What does this print, and why is it surprising?",
"""<pre>PipedWriter writer = new PipedWriter();
PipedReader reader = new PipedReader(writer);
writer.write("hello");
writer.close();
System.out.println(reader.read());
System.out.println((char) reader.read());</pre>""",
"It prints <span class='mono'>104</span> then <span class='mono'>e</span>. The surprise is that <span class='mono'>read()</span> on a character stream returns the character's numeric code, not the character — which is exactly why the return type is <span class='mono'>int</span>. Casting to <span class='mono'>char</span> is what makes it readable. Also note that both ends are used in the same thread here, which works only because the data was written before it was read; a pipe used concurrently in one thread would deadlock."))

E.append(exercise(4, "What does this print?",
"""<pre>System.out.println(Math.min(8.0, Math.max(0.0, 5.0 + (10.0 * 0.0014 + 4.0 / 100.0) * 0.58)));</pre>""",
"<b>5.03132</b>. The rainfall contribution is 10.0 × 0.0014 = 0.014; the observed rise is 4.0 / 100 = 0.04; their sum is 0.054; multiplied by the reinforced-levee factor 0.58 gives 0.03132; added to 5.0 gives 5.03132, which is already inside the 0 to 8 clamp. This is exactly the arithmetic in <span class='mono'>BasinZone.apply</span>."))

E.append(exercise(5, "What does this print?",
"""<pre>ObjectInputFilter filter = info -> {
    Class<?> type = info.serialClass();
    if (type == null) return ObjectInputFilter.Status.ALLOWED;
    return type.getName().startsWith("com.basinwatch.")
            ? ObjectInputFilter.Status.ALLOWED
            : ObjectInputFilter.Status.REJECTED;
};
System.out.println(filter.checkInput(new ObjectInputFilter.FilterInfo() {
    public Class<?> serialClass() { return java.util.ArrayList.class; }
    public long arrayLength() { return 0; }
    public long depth() { return 0; }
    public long references() { return 0; }
    public long streamBytes() { return 0; }
}));</pre>""",
"<b>REJECTED</b>. <span class='mono'>java.util.ArrayList</span> does not start with <span class='mono'>com.basinwatch.</span>, so the filter refuses it. This is the point of the exercise: a filter that permits only one package would break ordinary serialization of collections, which is why BasinWatch's real filter also allows <span class='mono'>java.lang</span>, <span class='mono'>java.util</span> and <span class='mono'>java.time</span>."))

E.append(exercise(6, "How many statements execute, and how many commits?",
"""<pre>connection.setAutoCommit(false);
try (PreparedStatement a = connection.prepareStatement("INSERT ...");
     PreparedStatement b = connection.prepareStatement("UPDATE ...")) {
    a.executeUpdate();
    b.executeUpdate();
    connection.commit();
}</pre>""",
"Two statements execute and <b>one</b> commit occurs. With autocommit off, neither statement is durable until <span class='mono'>commit()</span> is called; both become visible together at that moment. If the second statement threw, a rollback would discard the first as well — which is the whole purpose of the transaction."))

E.append(exercise(7, "What is wrong with this loop, and what does it print?",
"""<pre>try (PreparedStatement ps = connection.prepareStatement(
        "SELECT zone_id FROM sensor_readings LIMIT ?")) {
    ps.setString(1, "10");
    try (ResultSet rows = ps.executeQuery()) {
        while (rows.next()) {
            System.out.println(rows.getString(1));
        }
    }
}</pre>""",
"The parameter is bound with <span class='mono'>setString</span> for a <span class='mono'>LIMIT</span>, which expects a number. Depending on the driver this either fails or produces an implicit conversion; the correct call is <span class='mono'>setInt(1, 10)</span>. This is the value of typed setters: the type is part of the statement's contract, and using the wrong setter hides a mistake that a numeric type would have caught."))

E.append("""
<h3><span class="n">E.2</span>Debugging and repair</h3>
""")

E.append(exercise(8, "Repair this method.",
"""<pre>public String readFirstLine(Path path) {
    BufferedReader reader = new BufferedReader(new FileReader(path));
    return reader.readLine();
}</pre>""",
"""Three problems: the reader is never closed, the charset is the platform default, and the method declares no checked exception. A corrected version:<pre>public String readFirstLine(Path path) throws IOException {
    try (BufferedReader reader = Files.newBufferedReader(path, StandardCharsets.UTF_8)) {
        return reader.readLine();
    }
}</pre>Note that returning from inside a try-with-resources still closes the resource."""))

E.append(exercise(9, "Repair this loop.",
"""<pre>String line = reader.readLine();
while (line != null) {
    process(line);
    line = reader.readLine();
}</pre>""",
"""This is actually correct — it reads before the loop and again at the end, which is the classic pre-read form. The repair is not about correctness but about clarity and duplication: <pre>String line;
while ((line = reader.readLine()) != null) {
    process(line);
}</pre>The single-expression form makes it impossible for the two read sites to diverge, which is the real risk in the original."""))

E.append(exercise(10, "Repair this queue method.",
"""<pre>public synchronized BasinEvent take() {
    if (events.isEmpty()) {
        wait();
    }
    return events.removeFirst();
}</pre>""",
"""Three defects: <span class='mono'>wait()</span> is not inside a loop, so a spurious wake-up or a competing consumer can empty the deque again; the method does not declare <span class='mono'>InterruptedException</span>; and a closed empty buffer would wait forever. Corrected:<pre>public synchronized BasinEvent take() throws InterruptedException {
    while (events.isEmpty() &amp;&amp; !closed) {
        waitingConsumers++;
        try {
            wait();
        } finally {
            waitingConsumers--;
        }
    }
    if (events.isEmpty()) {
        return null;                 // closed and drained
    }
    BasinEvent event = events.removeFirst();
    notifyAll();
    return event;
}</pre>"""))

E.append(exercise(11, "Repair this shutdown.",
"""<pre>public void close() throws IOException {
    eventBuffer.close();
    feedWriter.close();
    sensorFeed.requestStop();
}</pre>""",
"The order is wrong on two counts. Closing the queue before the consumer has drained it discards events already read from the pipe, and closing the writer before stopping the producer makes the producer throw a spurious <span class='mono'>IOException</span> on its next write. Corrected order: <span class='mono'>requestStop()</span>, then <span class='mono'>feedWriter.close()</span>, then join the intake thread, then <span class='mono'>eventBuffer.close()</span>."))

E.append(exercise(12, "Repair this SQL.",
"""<pre>String sql = "SELECT * FROM operational_events WHERE zone_id = '"
           + zoneId + "' ORDER BY occurred_at DESC";</pre>""",
"""Two problems. The value is concatenated into the statement, so it can alter the statement's structure — SQL injection. And <span class='mono'>SELECT *</span> makes the code depend on the column order, which a schema change can silently break. Corrected:<pre>String sql = "SELECT occurred_at, event_type, zone_id, detail "
           + "FROM operational_events WHERE zone_id = ? "
           + "ORDER BY occurred_at DESC";
try (PreparedStatement ps = connection.prepareStatement(sql)) {
    ps.setString(1, zoneId);
    try (ResultSet rows = ps.executeQuery()) { ... }
}</pre>"""))

E.append(exercise(13, "Repair this transaction.",
"""<pre>public void record(Connection a, ResponseMission mission) throws SQLException {
    try (Connection b = database.openConnection()) {
        b.setAutoCommit(false);
        missions.insert(b, mission, Instant.now());
        resourceUsage.insert(b, mission.id(), ResourceType.PUMP, 1, Instant.now());
        b.commit();
    }
}</pre>""",
"The method accepts a connection <span class='mono'>a</span> and then ignores it, opening a second connection <span class='mono'>b</span>. If the caller intended to enlist this work in an existing transaction on <span class='mono'>a</span>, atomicity is lost — the work is committed independently. The repair is to use the connection that was passed in, and not to commit if the caller owns the transaction boundary."))

E.append(exercise(14, "Repair this Swing update.",
"""<pre>engine.addSnapshotListener(snapshot -> {
    mapPanel.setSnapshot(snapshot);
    mapPanel.repaint();
});</pre>""",
"""The listener may be invoked from a worker thread, and <span class='mono'>setSnapshot</span> and <span class='mono'>repaint</span> both touch a Swing component. The repair wraps the whole body:<pre>engine.addSnapshotListener(snapshot ->
        SwingUtilities.invokeLater(() -> {
            mapPanel.setSnapshot(snapshot);
            mapPanel.repaint();
        }));</pre>Note that the wrapper goes around <i>both</i> statements, not just the repaint."""))

E.append(exercise(15, "Repair this table update.",
"""<pre>void setEntries(List&lt;DatabaseHistoryEntry&gt; entries) {
    this.entries = entries;
}</pre>""",
"""Two problems. The list is stored by reference, so a later change on the database thread could be visible to the event-dispatch thread mid-paint. And the table is never told the data changed, so it would keep displaying the old rows. Corrected:<pre>void setEntries(List&lt;DatabaseHistoryEntry&gt; entries) {
    this.entries = List.copyOf(entries);
    fireTableDataChanged();
}</pre>"""))

E.append("""
<h3><span class="n">E.3</span>Tracing and data flow</h3>
""")

E.append(exercise(16, "Trace a malformed record.",
"<p>A line arrives from the pipe reading <span class='mono'>READ|abc|MIL-ST-2|MIL|12.4|3.1</span>. Describe every consequence.</p>",
"<span class='mono'>SensorReading.parse</span> splits the line into six fields and finds the <span class='mono'>READ</span> marker, so the field-count check passes. <span class='mono'>Long.parseLong(\"abc\")</span> then throws <span class='mono'>NumberFormatException</span>, which the method catches and rethrows as <span class='mono'>IllegalArgumentException</span>. <span class='mono'>SensorIntake</span> catches that, reports a warning through the warning consumer, and executes <span class='mono'>continue</span>. The event never enters the buffer, no worker sees it, no activity is recorded, no archive record is written, no database row exists. The intake loop continues with the next line."))

E.append(exercise(17, "Trace a stale reading.",
"<p>Zone MIL has already applied a reading with tick 214. A duplicate arrives with tick 214. Describe every consequence.</p>",
"<span class='mono'>BasinZone.apply</span> compares <span class='mono'>reading.tick() &lt;= lastReadingTick</span> and returns <span class='mono'>false</span> without changing any field. The model produces no activity message, so the journal writes nothing for it; the engine's changed test fails, so no archive record and no database row are written. The interface is unchanged. The only trace is that the intake accepted and queued an event that the model declined — which is correct, because the intake's job is to validate the format, not the ordering."))

E.append(exercise(18, "Trace a dispatch that fails its reservation.",
"<p>The operator requests a pump deployment for zone NOR, but all four pumps are already committed. Describe every consequence.</p>",
"<span class='mono'>ResourceAllocator.tryReserve</span> checks every requirement and finds <span class='mono'>PUMP</span> unavailable, so it returns <span class='mono'>false</span> having changed nothing — no resource was partially deducted. <span class='mono'>BasinModel</span> does not create a mission, no snapshot changes, and the interface's resource board is unchanged. The engine reports a failure message, which the listener posts to the event-dispatch thread and the status bar displays. Nothing is written to the log or the database, because nothing happened. This is the all-or-nothing property in action."))

E.append(exercise(19, "Trace a dispatch whose third database write fails.",
"<p>In <span class='mono'>recordDispatch</span>, the mission insert succeeds, the resource rows succeed, and the audit event insert throws <span class='mono'>SQLException</span>. Describe every consequence.</p>",
"The catch block calls <span class='mono'>connection.rollback()</span>, which discards the mission row and the resource-usage rows as well. The exception is then rethrown and caught by the outer catch, which reports it through the status listener. The database therefore contains none of the three writes, so it agrees with the in-memory model, which <i>did</i> record the dispatch. That divergence is a real limitation worth naming honestly: the interface and the log show the dispatch, the database does not, and the status message is what tells the operator. A production system would reconcile on the next start."))

E.append(exercise(20, "Trace a session restore with a truncated file.",
"<p>The file <span class='mono'>last-session.bws</span> is 2,000 bytes but was truncated mid-object. Describe every consequence.</p>",
"The size gate passes, because 2,000 bytes is below the 4 MB bound. The class filter approves the classes it sees. The version check passes, because the header was written first and is intact. <span class='mono'>readObject</span> then throws <span class='mono'>EOFException</span> — a subclass of <span class='mono'>IOException</span> — because the stream ends inside an object. The load fails, the exception propagates to the caller, and the engine reports it. The application starts with a fresh model rather than a corrupt one, which is the correct outcome: a partial session is worse than none."))

E.append(exercise(21, "Trace a history read when the database file is deleted between launches.",
"<p>Describe the sequence from start-up to an empty history table.</p>",
"<span class='mono'>DatabaseManager.isAvailable</span> calls <span class='mono'>openConnection</span>, and because SQLite creates a missing database file on demand, the connection succeeds — so availability is actually true, and the initialiser recreates the four empty tables. <span class='mono'>loadHistory</span> therefore returns an empty list from a real query rather than from the unavailable branch. The table shows no rows and the status reports zero entries. The distinction matters: an empty database and an unavailable database produce the same visible result through different code paths."))

E.append(exercise(22, "Trace a shutdown during a save.",
"<p>The operator clicks Save and immediately closes the window. Describe what survives.</p>",
"Two save operations may be in flight. The explicit save writes to <span class='mono'>name.bws.tmp</span>; the shutdown's automatic save writes to <span class='mono'>last-session.bws</span> through its own temporary file. Both run on <span class='mono'>basin-control</span>, which is single-threaded, so they are serialised rather than concurrent. <span class='mono'>closeEngine</span> stops the feed, closes the pipe, joins intake, drains the archive queue and flushes the journal. If the process is killed before either save completes, the temporary files are incomplete but the previous <span class='mono'>last-session.bws</span> is intact, because the move had not happened. That is the purpose of the atomic replace."))

E.append("""
<h3><span class="n">E.4</span>Architecture interpretation</h3>
""")

E.append(exercise(23, "Why is the archive written on a separate thread from the journal?",
"The journal is a character stream that the engine appends to directly, and it flushes on a policy. The archive is a byte stream with a header that must be written exactly once and typed records that must not interleave. Writing both on the worker thread would make every event wait for two disk operations. Putting the archive behind a single-threaded executor means the worker's cost is a queue insertion, while the header-once and no-interleaving guarantees are still upheld because there is only one archive writer."))

E.append(exercise(24, "Why does the engine publish snapshots rather than letting the interface read the model?",
"Because the model is mutated by three worker threads while the event-dispatch thread renders. Letting the interface read live objects would require the model's monitor to be held during painting, which would block every worker for the duration of a repaint and could deadlock if a listener ever called back into the model. An immutable snapshot removes the shared state entirely: the interface reads a value that cannot change, so no locking is needed and no torn read is possible."))

E.append(exercise(25, "Why does the database layer have both a service and repositories?",
"The service owns concerns that are not about any one table: the worker thread, the availability flag, the queue, the transaction boundaries and the failure reporting. The repositories own concerns that are about exactly one table: its SQL and its row mapping. Merging them would put transaction logic in every repository and SQL in the service; separating them means a repository can be tested against a plain connection with no threads involved, and the service's policy can change without touching any SQL."))

E.append(exercise(26, "Why is the sensor feed a <span class='mono'>Thread</span> subclass while the intake is a <span class='mono'>Runnable</span>?",
"The feed owns a lifecycle: it is started, it sleeps between intervals, it must be interruptible, and it holds a blocking pipe endpoint that must be closed. Extending <span class='mono'>Thread</span> lets it carry a name, a priority and a state that diagnostics report. The intake is a task — a unit of work — with no lifecycle of its own; the engine creates a plain thread, names it, and hands it the task. This is the standard advice to prefer <span class='mono'>Runnable</span> unless you must own the thread, applied where it genuinely differs."))

E.append(exercise(27, "What would break if the model were not thread-safe?",
"Three workers call <span class='mono'>model.process</span> concurrently, and the event-dispatch thread reads snapshots. Without the monitor on <span class='mono'>process</span> and the immutable snapshot boundary, two workers could apply readings to the same zone simultaneously, producing a lost update — one water level overwriting the other. The resource allocator could also over-allocate, because two dispatches could both pass the check loop before either decremented. Both failures are intermittent and load-dependent, which is exactly why the design avoids them structurally rather than by testing."))

E.append(exercise(28, "Why is the resource allocator's reservation all-or-nothing rather than incremental?",
"Because a mission requires several resources, and a partial reservation is a state the system cannot act on: the mission cannot start without all of them, and the deducted resources cannot be used by anything else. Incremental deduction would require a compensating rollback if a later requirement failed, and that rollback is itself a place where a bug could leave the inventory wrong. Checking everything before changing anything means no intermediate state exists to be cleaned up."))

E.append(exercise(29, "Why does the engine have three response workers but one archive worker and one database worker?",
"Because the three kinds of work have different constraints. Applying an event to the model is CPU-bound and independent per event, so concurrency helps. Appending to the archive must be serialised, because the header is written once and records must not interleave. Database work must be serialised for two reasons: SQLite permits one writer, and a single writer means no transaction can interfere with another, so no isolation policy is needed. The thread counts follow from the constraints, not from a guess about performance."))

E.append(exercise(30, "If you replaced SQLite with PostgreSQL, what would change?",
"Five things, and none of them is in the domain or the interface. The Maven dependency changes from <span class='mono'>org.xerial:sqlite-jdbc</span> to the PostgreSQL driver. The URL changes from <span class='mono'>jdbc:sqlite:path</span> to <span class='mono'>jdbc:postgresql://host:port/database</span> with credentials. The DDL changes, because <span class='mono'>AUTOINCREMENT</span> is SQLite syntax and the corresponding PostgreSQL type is different. Connections would need pooling, because a server round trip is far more expensive than opening a local file. And isolation would become a real concern, because a server database allows concurrent writers — so the single-writer guarantee the current design relies on would need replacing with explicit transaction handling. Everything else — the repositories' SQL shape, the prepared statements, the row mapping, the service, the interface — is unchanged, which is the payoff of programming to the JDBC interfaces."))

E.append("</div>")

# ======================================================================
# G — HIGH-YIELD REVISION, GLOSSARY AND REFERENCE
# ======================================================================
G.append("""
<div class="chapter" id="chgloss">
  <div class="chapter-num">REFERENCE</div>
  <h2 class="chapter-title">High-Yield Revision, Glossary and Reference</h2>
  <p class="chapter-deck">The material to read the night before an examination: essential definitions,
  the classes and signatures worth memorising, the mistakes that cost marks, a glossary, and the source
  coverage matrix.</p>
""")

G.append("""
<h3><span class="n">G.1</span>Twenty-five definitions to know exactly</h3>
""")

G.append(table(
  ["Term", "Definition"],
  [
    ["Stream", "An ordered, one-directional sequence of data with a source or destination, consumed or produced incrementally."],
    ["Byte stream", "A stream carrying 8-bit units with no interpretation applied."],
    ["Character stream", "A stream carrying 16-bit characters converted through a charset."],
    ["Charset", "The reversible mapping between characters and bytes, such as UTF-8."],
    ["Filter stream", "A stream that wraps another stream and adds one capability."],
    ["Buffering", "An intermediate array that turns many small operations into few large ones."],
    ["Serialization", "Converting an object graph into a byte sequence including class descriptors."],
    ["Deserialization", "Reconstructing an object graph from such a byte sequence, without invoking constructors."],
    ["<span class='mono'>transient</span>", "A modifier excluding a field from serialization."],
    ["<span class='mono'>serialVersionUID</span>", "The explicit version identity of a serializable class."],
    ["Pipe", "A matched writer/reader pair with a bounded buffer, used between two threads."],
    ["Back-pressure", "A bounded channel making a fast producer wait rather than buffer without limit."],
    ["Monitor", "The lock associated with an object, entered by <span class='mono'>synchronized</span>."],
    ["Condition wait", "A <span class='mono'>wait()</span> inside a loop that re-tests a predicate while holding a monitor."],
    ["Producer–consumer", "A pattern in which one thread produces items into a shared channel and another consumes them."],
    ["Database table", "A named collection of rows sharing the same columns and types."],
    ["Primary key", "The column or columns uniquely identifying each row."],
    ["Index", "An auxiliary structure that speeds up lookups on particular columns."],
    ["JDBC", "The standard Java API for relational database access, comprising interfaces plus a driver mechanism."],
    ["JDBC driver", "The vendor-supplied implementation that translates JDBC calls into a database's protocol."],
    ["PreparedStatement", "A pre-parsed SQL statement with numbered placeholders filled by typed setters."],
    ["ResultSet", "A cursor over the rows a query returned, positioned before the first row initially."],
    ["Transaction", "A group of database operations that all take effect or none do."],
    ["ACID", "Atomicity, consistency, isolation and durability — the four transaction guarantees."],
    ["Event-dispatch thread", "The single thread on which Swing performs event handling and painting."],
  ],
  caption="<b>Table G.1</b> — The definitions worth being able to state word for word.", cls="big"))

G.append("""
<h3><span class="n">G.2</span>Classes and method signatures worth memorising</h3>
""")

G.append(table(
  ["Class", "Key methods", "Notes"],
  [
    ["<span class='mono'>InputStream</span>", "<span class='mono'>read()</span>, <span class='mono'>read(byte[])</span>, <span class='mono'>close()</span>", "<span class='mono'>read()</span> returns <span class='mono'>int</span>; -1 means end"],
    ["<span class='mono'>OutputStream</span>", "<span class='mono'>write(int)</span>, <span class='mono'>write(byte[])</span>, <span class='mono'>flush()</span>, <span class='mono'>close()</span>", "Abstract"],
    ["<span class='mono'>Reader</span>", "<span class='mono'>read()</span>, <span class='mono'>read(char[])</span>, <span class='mono'>close()</span>", "No <span class='mono'>readLine()</span> here"],
    ["<span class='mono'>Writer</span>", "<span class='mono'>write(int)</span>, <span class='mono'>write(String)</span>, <span class='mono'>flush()</span>, <span class='mono'>close()</span>", "Abstract"],
    ["<span class='mono'>BufferedReader</span>", "<span class='mono'>readLine()</span>", "Returns <span class='mono'>null</span> at end"],
    ["<span class='mono'>BufferedWriter</span>", "<span class='mono'>newLine()</span>", "Platform line separator"],
    ["<span class='mono'>DataOutputStream</span>", "<span class='mono'>writeInt</span> (4), <span class='mono'>writeLong</span> (8), <span class='mono'>writeDouble</span> (8), <span class='mono'>writeUTF</span> (2+n)", "Big-endian; the order <i>is</i> the schema"],
    ["<span class='mono'>ObjectOutputStream</span>", "<span class='mono'>writeObject(Object)</span>", "Requires <span class='mono'>Serializable</span>"],
    ["<span class='mono'>ObjectInputStream</span>", "<span class='mono'>readObject()</span>, <span class='mono'>setObjectInputFilter(...)</span>", "Constructors are not called"],
    ["<span class='mono'>Files</span>", "<span class='mono'>newBufferedReader</span>, <span class='mono'>newBufferedWriter</span>, <span class='mono'>newInputStream</span>, <span class='mono'>newOutputStream</span>, <span class='mono'>size</span>, <span class='mono'>move</span>, <span class='mono'>createDirectories</span>", "Prefer these to the classic classes"],
    ["<span class='mono'>DriverManager</span>", "<span class='mono'>getConnection(String url)</span>", "Selects a registered driver"],
    ["<span class='mono'>Connection</span>", "<span class='mono'>prepareStatement</span>, <span class='mono'>createStatement</span>, <span class='mono'>setAutoCommit</span>, <span class='mono'>commit</span>, <span class='mono'>rollback</span>, <span class='mono'>close</span>", "A transaction belongs to a connection"],
    ["<span class='mono'>PreparedStatement</span>", "<span class='mono'>setInt</span>, <span class='mono'>setLong</span>, <span class='mono'>setDouble</span>, <span class='mono'>setString</span>, <span class='mono'>executeQuery</span>, <span class='mono'>executeUpdate</span>", "Placeholders are 1-based"],
    ["<span class='mono'>ResultSet</span>", "<span class='mono'>next()</span>, <span class='mono'>getString</span>, <span class='mono'>getInt</span>, <span class='mono'>getDouble</span>, <span class='mono'>close</span>", "Cursor starts before the first row"],
    ["<span class='mono'>SwingUtilities</span>", "<span class='mono'>invokeLater(Runnable)</span>", "The only safe way to touch Swing from another thread"],
    ["<span class='mono'>CompletableFuture</span>", "<span class='mono'>supplyAsync</span>, <span class='mono'>whenComplete</span>, <span class='mono'>completedFuture</span>", "The callback runs on the completing thread"],
  ],
  caption="<b>Table G.2</b> — The API surface most likely to be asked about.", cls="big"))

G.append("""
<h3><span class="n">G.3</span>Ten mistakes that cost marks</h3>
<ol>
<li><b>Concatenating values into SQL.</b> Use <span class="mono">PreparedStatement</span> with placeholders. Always.</li>
<li><b>Assuming deserialization validates.</b> It bypasses constructors, so the rules you wrote in them do not run. Validate the restored state explicitly.</li>
<li><b>Forgetting the append flag.</b> Opening a file for output truncates it. A journal that should grow will silently restart.</li>
<li><b>Omitting the charset.</b> The platform default differs between machines, so a file written on one may be unreadable on another.</li>
<li><b>Mixing up the end-of-stream signals.</b> <span class="mono">read()</span> returns -1; <span class="mono">readLine()</span> returns <span class="mono">null</span>.</li>
<li><b>Using <span class="mono">wait()</span> in an <span class="mono">if</span>.</b> It must be a loop, because a woken thread is not guaranteed its condition holds.</li>
<li><b>Confusing <span class="mono">wait()</span> with <span class="mono">sleep()</span>.</b> <span class="mono">wait()</span> releases the monitor; <span class="mono">sleep()</span> does not.</li>
<li><b>Returning a <span class="mono">ResultSet</span> from a method that closes its connection.</b> Map rows into your own objects before leaving the block.</li>
<li><b>Touching Swing from a background thread.</b> Wrap the whole component-accessing body in <span class="mono">invokeLater</span>.</li>
<li><b>Spreading several statements across different connections and calling it a transaction.</b> A transaction belongs to one connection.</li>
</ol>
""")

G.append("""
<h3><span class="n">G.4</span>Glossary</h3>
""")

G.append(table(
  ["Term", "Meaning"],
  [
    ["ACID", "Atomicity, consistency, isolation, durability — the four transaction guarantees."],
    ["Aggregate root", "The single object that owns a group of related state and enforces its invariants; here, <span class='mono'>BasinModel</span>."],
    ["Annotation", "Metadata attached to a declaration; its retention policy determines whether it survives to runtime."],
    ["Append mode", "Opening an output stream so new writes follow existing content."],
    ["Atomic move", "Replacing a file in a single step, so no partial state is ever observable."],
    ["Audit trail", "An ordered record of what happened, for later inspection."],
    ["Autocommit", "The JDBC default in which each statement is its own transaction."],
    ["Back-pressure", "A bounded channel making a fast producer wait rather than buffer without limit."],
    ["Bean (JavaBean)", "A POJO following the conventions a framework needs: no-argument constructor, private fields, public accessors."],
    ["Bounded buffer", "A queue with a maximum size that makes producers wait when full."],
    ["Build lifecycle", "Maven's ordered sequence of phases, where a later phase runs every earlier one."],
    ["Byte stream", "A stream of 8-bit units with no interpretation applied."],
    ["Callback", "A function supplied to be invoked later, typically on another thread."],
    ["Charset", "The reversible mapping between characters and bytes."],
    ["Commit", "Making a transaction's changes permanent and visible."],
    ["Condition wait", "A <span class='mono'>wait()</span> inside a loop that re-tests a predicate while holding a monitor."],
    ["Constructor injection", "Supplying an object's dependencies as constructor arguments."],
    ["Coordinate (Maven)", "The groupId, artifactId and version triple identifying a library."],
    ["DataAccessException", "Spring's unchecked exception hierarchy for data access failures."],
    ["DataSource", "An abstraction representing a source of database connections."],
    ["DDL", "Data definition language: statements such as <span class='mono'>CREATE TABLE</span>."],
    ["Decorator pattern", "Adding behaviour by wrapping an object in another of the same interface."],
    ["Deserialization", "Reconstructing an object graph from bytes, without invoking constructors."],
    ["Durability", "The property that a committed change survives a failure."],
    ["EDT (event-dispatch thread)", "The single thread on which Swing handles events and paints."],
    ["Encapsulation", "Keeping state private so behaviour is the only route in."],
    ["Enum", "A type whose values come from a fixed, closed set; may carry data."],
    ["Fan-out", "One decision causing several independent downstream operations."],
    ["Filter stream", "A stream that wraps another stream and adds one capability."],
    ["Fire-and-forget", "A call that queues work and returns immediately, reporting failure out of band."],
    ["Flush", "Forcing buffered data out to the destination without closing."],
    ["Idempotent", "Safe to perform more than once with the same result."],
    ["Index (database)", "An auxiliary structure speeding up lookups on particular columns."],
    ["Inversion of control", "A component declaring interest and being called, rather than polling."],
    ["Isolation", "The property that concurrent transactions do not see each other's partial work."],
    ["JDBC", "The standard Java API for relational database access."],
    ["JdbcTemplate", "A Spring class that executes SQL and manages JDBC resources, leaving SQL and row mapping to the caller."],
    ["Layout manager", "The object deciding where a container's children are placed."],
    ["Magic number", "A constant at the start of a file identifying its format."],
    ["Metadata (file)", "Information about a file — name, size, modification time — as opposed to its contents."],
    ["Monitor", "The lock associated with an object, entered by <span class='mono'>synchronized</span>."],
    ["Namespace (XML)", "A URI-qualified vocabulary that prevents name collisions in a document."],
    ["<span class='mono'>ObjectInputFilter</span>", "A hook approving or rejecting each class a deserialization stream tries to construct."],
    ["Pattern matching", "Testing and binding an object's type in one expression."],
    ["Pipe", "A matched writer/reader pair with a bounded buffer, used between two threads."],
    ["Placeholder", "The <span class='mono'>?</span> in a prepared statement, replaced by a bound value."],
    ["POJO", "A Plain Old Java Object: any ordinary class with no framework convention."],
    ["Primary key", "The column or columns uniquely identifying each row."],
    ["Producer–consumer", "A pattern in which one thread produces into a shared channel and another consumes."],
    ["Record", "A class declaring immutable data, with a compiler-generated constructor and accessors."],
    ["Reflection", "Inspecting and using classes and members at runtime."],
    ["Repository", "A class owning the SQL for one table and mapping rows to and from domain objects."],
    ["ResultSet cursor", "The position marker over a query's rows, starting before the first."],
    ["Rollback", "Discarding a transaction's changes as though they never happened."],
    ["RowMapper", "A callback converting one result-set row into an object."],
    ["Serialization", "Converting an object graph into bytes including class descriptors."],
    ["<span class='mono'>serialVersionUID</span>", "The explicit version identity of a serializable class."],
    ["Service provider file", "<span class='mono'>META-INF/services/java.sql.Driver</span>, which lets a driver register itself automatically."],
    ["Snapshot (immutable)", "A value object copied out of the model so another thread can read it safely."],
    ["SQL injection", "An attack in which user input becomes part of a statement's structure."],
    ["SQLState", "The standard five-character error code carried by a <span class='mono'>SQLException</span>."],
    ["Stale guard", "A check that rejects input older than the state already applied."],
    ["Stream", "An ordered, one-directional sequence of data, consumed incrementally."],
    ["Thin driver", "A pure-Java type 4 JDBC driver needing no native code."],
    ["Thread confinement", "The rule that an object may only be accessed from one thread."],
    ["Transaction", "A group of database operations that all take effect or none do."],
    ["Transient", "A modifier excluding a field from serialization."],
    ["try-with-resources", "A statement that closes every declared resource automatically, in reverse order."],
    ["Uber jar", "A jar containing a project's classes plus all its dependencies' classes."],
    ["Well-formed (XML)", "Following XML's syntax rules, as distinct from conforming to a schema."],
    ["XSD", "XML Schema Definition, a schema language written in XML itself."],
  ],
  caption="<b>Table G.3</b> — Glossary.", cls="big"))

G.append("""
<h3><span class="n">G.5</span>Key workflows on one page</h3>
""")

G.append(code('''READ A TEXT FILE
  Path -> Files.newBufferedReader(path, UTF_8) -> loop on readLine() != null -> close (try-with-resources)

WRITE A TEXT FILE
  Path -> createDirectories(parent) -> Files.newBufferedWriter(path, UTF_8[, CREATE, APPEND])
       -> write -> flush -> close

READ TYPED RECORDS
  Files.newInputStream -> BufferedInputStream -> DataInputStream
  -> readLong, readUTF, readDouble, ... until EOFException

WRITE TYPED RECORDS
  Files.newOutputStream -> BufferedOutputStream -> DataOutputStream
  -> writeLong, writeUTF, writeDouble, ... -> flush -> close

SERIALIZE AN OBJECT GRAPH
  ObjectOutputStream( BufferedOutputStream( Files.newOutputStream(temp) )
  -> writeInt(version) -> writeObject(snapshot) -> flush -> close -> atomic move into place

DESERIALIZE SAFELY
  check size -> ObjectInputStream -> setObjectInputFilter -> readInt(version)
  -> readObject -> cast -> validate

PIPE BETWEEN THREADS
  PipedWriter w = new PipedWriter();  PipedReader r = new PipedReader(w, 8192);
  feed thread writes + flush; intake thread reads readLine() until null; writer.close() ends the loop

BOUNDED QUEUE
  producer: synchronized put -> while (full && !closed) wait(); add; notifyAll();
  consumer: synchronized take -> while (empty && !closed) wait(); remove; notifyAll();

SHUTDOWN ORDER
  stop producer -> close writer -> join consumer -> close queue -> drain archive -> flush journal -> save

JDBC QUERY
  DriverManager.getConnection(url) -> prepareStatement(sql) -> setX(1..n)
  -> executeQuery() -> while (rows.next()) map row -> close rows, statement, connection

JDBC UPDATE
  ... -> executeUpdate() -> inspect the returned row count -> close

JDBC TRANSACTION
  setAutoCommit(false) -> statement 1 -> statement 2 -> commit()
  catch: rollback()   finally: setAutoCommit(true)

SWING OFF-THREAD UPDATE
  worker thread -> SwingUtilities.invokeLater(() -> { update components; repaint(); })

SWING TABLE UPDATE
  model.setEntries(List.copyOf(rows)) -> fireTableDataChanged()''', "the twelve workflows in the book, as checklists", lang="none"))

G.append("""
<h3><span class="n">G.6</span>Source coverage matrix</h3>
<p>Every topic area from the source lecture material, mapped to where it is taught and whether it is
verified against the project's code.</p>
""")

G.append(table(
  ["Source topic", "Book chapter", "Project evidence", "Status"],
  [
    ["Java I/O package overview", "4", "Every stream in the <span class='mono'>io</span> package", "Verified"],
    ["InputStream / OutputStream", "4", "Basis of <span class='mono'>SensorArchive</span>", "Verified"],
    ["FileInputStream / FileOutputStream", "5", "Contrasted with <span class='mono'>Files.newXxx</span>", "Verified (modern form used)"],
    ["Reader / Writer", "4", "<span class='mono'>OperationalJournal</span>, <span class='mono'>ReportWriter</span>", "Verified"],
    ["FileReader / FileWriter", "5", "Contrasted with the modern API", "Verified (modern form used)"],
    ["Buffered streams", "6", "Every file stream is buffered", "Verified"],
    ["DataInputStream / DataOutputStream", "6", "<span class='mono'>SensorArchive</span>", "Verified"],
    ["ByteArrayInputStream / ByteArrayOutputStream", "7", "Illustrative example", "Taught; not used"],
    ["PipedInputStream / PipedOutputStream", "7", "Character variants used instead", "Related"],
    ["PipedReader / PipedWriter", "7", "<span class='mono'>SensorFeed</span> to <span class='mono'>SensorIntake</span>", "Verified"],
    ["File handling and metadata", "5, 9", "<span class='mono'>AppPaths</span>, <span class='mono'>SaveCatalog</span>", "Verified"],
    ["Exceptions and resource management", "4, 5", "try-with-resources, suppressed exceptions", "Verified"],
    ["Object serialization", "8", "<span class='mono'>SnapshotStore</span>", "Verified"],
    ["Threading and the producer–consumer model", "3, 7", "Feed, intake, buffer, workers", "Verified"],
    ["JDBC fundamentals", "10, 11", "<span class='mono'>DatabaseManager</span>", "Verified"],
    ["JDBC architecture and drivers", "11", "SQLite type 4 driver", "Verified"],
    ["Connection", "12", "<span class='mono'>DatabaseManager.openConnection</span>", "Verified"],
    ["Statement", "12", "Schema DDL in <span class='mono'>DatabaseInitializer</span>", "Verified"],
    ["PreparedStatement", "12", "Every repository method", "Verified"],
    ["CallableStatement", "12", "No stored procedures exist", "Taught; not used"],
    ["ResultSet and CRUD", "12", "All four repositories", "Verified"],
    ["SQL parameters", "12", "Nine-placeholder insert", "Verified"],
    ["Transactions", "13", "<span class='mono'>recordDispatch</span>", "Verified"],
    ["SQLException and cleanup", "12, 14", "<span class='mono'>enqueue</span> catches and reports", "Verified"],
    ["Spring JdbcTemplate", "19", "Not used", "Taught as alternative"],
    ["DriverManagerDataSource", "19", "Not used; <span class='mono'>DriverManager</span> used directly", "Taught as alternative"],
    ["Maven and pom.xml", "17", "<span class='mono'>pom.xml</span> with one dependency", "Verified"],
    ["Dependency management", "17", "sqlite-jdbc version property", "Verified"],
    ["XML and namespaces", "18", "<span class='mono'>pom.xml</span> header only", "Verified (build file only)"],
    ["XML Schema", "18", "Not used", "Taught; not used"],
    ["Annotations", "18", "<span class='mono'>@Override</span>, <span class='mono'>@FunctionalInterface</span>, <span class='mono'>@SuppressWarnings</span>", "Verified"],
    ["POJO versus JavaBean", "2, 18", "Records and DTOs; no beans", "Verified"],
    ["Swing components and layouts", "15", "<span class='mono'>MainFrame</span>, <span class='mono'>BasinMapPanel</span>", "Verified"],
    ["Event handling", "15", "Action listeners throughout", "Verified"],
    ["The login application", "15", "Walked through as lecture material", "Lecture-note style"],
    ["Swing and JDBC together", "16", "<span class='mono'>DatabaseHistoryPanel</span>", "Verified"],
  ],
  caption="<b>Table G.4</b> — Source coverage matrix.", cls="big"))

G.append("""
<h3><span class="n">G.7</span>The final visual summary</h3>
<p>One diagram to hold in mind: the whole system, the concepts that make each part work, and the two
boundaries where the technologies meet.</p>
""")

G.append(figure("d29_revision_map", "29", "The complete Java system, revisited",
"The architecture from Diagram 1 with the syllabus concepts annotated onto each layer, plus the two interaction boundaries and the build that puts the driver on the classpath.",
"portrait"))

G.append("""
<div class="summary"><span class="tag">THE LAST WORD</span>
<ul>
<li><b>Architecture first.</b> Name the layers, the threads and the two boundaries before any API.</li>
<li><b>Three properties describe every stream.</b> Direction, unit, and source or destination.</li>
<li><b>Four defences protect deserialization.</b> Size, filter, version, validation.</li>
<li><b>One rule governs Swing.</b> Only the event-dispatch thread touches components.</li>
<li><b>One connection owns a transaction.</b> Everything inside it must share that connection.</li>
<li><b>Two persistence mechanisms, two questions.</b> A file records; a database answers.</li>
<li><b>Explain connections, not definitions.</b> That is what this book has been for.</li>
</ul></div>
</div>
""")

HTML = "".join(R + V + E + G)
