"""PART III — Databases and JDBC.  Chapters 10-14."""
from . import *

P = []
B10, B11, B12, B13, B14 = [], [], [], [], []

P.append("""
<div class="part-page">
  <div class="pnum">PART III</div>
  <h1>Databases and JDBC</h1>
  <div class="prule"></div>
  <div class="pintro">A file records what happened; a database answers questions about it. This part
  explains why an application keeps both, how JDBC carries SQL from Java to a database and rows back,
  what a transaction guarantees, and how BasinWatch's optional SQLite history is actually built.</div>
  <div class="chapters">
    <div><span>10</span>Why Databases and JDBC Exist</div>
    <div><span>11</span>JDBC Architecture and Drivers</div>
    <div><span>12</span>SQL Execution Through JDBC</div>
    <div><span>13</span>Database Transactions and Reliable Persistence</div>
    <div><span>14</span>How BasinWatch Uses JDBC and SQLite</div>
  </div>
</div>
""")

# ======================================================================
# CHAPTER 10
# ======================================================================
B10.append(chapter(10, "Why Databases and JDBC Exist",
"Memory, files and structured storage. Why an application chooses more than one persistence mechanism, and where JDBC fits between Java code and a database."))

B10.append("""
<h3><span class="n">10.1</span>Three places data can live</h3>
<p>Data in a running Java program lives in three quite different places, and each has a different
lifetime and a different set of capabilities.</p>
""")

B10.append(table(
  ["", "In-memory state", "Persistent files", "A relational database"],
  [
    ["Lifetime", "Until the process ends or the object is discarded", "Until the file is deleted", "Until the rows are deleted"],
    ["Access speed", "Nanoseconds — a field read", "Microseconds to milliseconds", "Microseconds to milliseconds, plus query planning"],
    ["Can be searched selectively?", "Only by writing code to iterate", "Only by reading and filtering yourself", "<b>Yes</b> — indexes and <span class='mono'>WHERE</span> clauses"],
    ["Concurrent access", "Requires explicit synchronisation", "Effectively one writer", "Built-in locking and isolation"],
    ["Partial update", "A field assignment", "Rewrite the region or the file", "An <span class='mono'>UPDATE</span> touching one row"],
    ["Guarantees", "None beyond the language", "None beyond what you write", "Atomicity, consistency, isolation, durability"],
    ["Structure", "Objects and references", "Whatever format you invent", "Tables, columns, types, constraints"],
  ],
  caption="<b>Table 10.1</b> — Three homes for data, compared."))

B10.append(core("""<p>The decisive difference is not speed. It is <b>selective access</b>. Reading one
record out of ten million is trivial in a database and expensive in a file, because a database
maintains an index and a file does not. Everything else — transactions, constraints, concurrency —
follows from that.</p>"""))

B10.append("""
<h3><span class="n">10.2</span>Why BasinWatch uses more than one mechanism</h3>
<p>BasinWatch keeps in-memory state, four kinds of file, and an optional SQLite database. That is not
indecision; it is five different questions being asked of the same data.</p>
""")

B10.append(table(
  ["The question being asked", "Best mechanism", "Why not the others"],
  [
    ["What is the water level in MIL right now?",
     "In-memory model", "A file read or a query would be slower and would need synchronising."],
    ["What has the application been doing today?",
     "Operational log file", "A database would work, but a text file is readable without any tooling."],
    ["What exactly did station MIL-ST-2 report at 09:15?",
     "Sensor archive", "The log does not carry every field; a snapshot keeps only the present."],
    ["Restore the situation from yesterday's save.",
     "Session snapshot", "Replaying a log is fragile; a snapshot restores state directly."],
    ["Show me the 200 most recent readings for MIL, newest first.",
     "<b>Database</b>", "A log requires reading and filtering everything; an index and a <span class='mono'>LIMIT</span> answer it directly."],
    ["How many missions completed in the last hour?",
     "<b>Database</b>", "Aggregation is one SQL expression over indexed rows; over a text file it is a full scan in application code."],
  ],
  caption="<b>Table 10.2</b> — Six questions, and the mechanism that answers each best."))

B10.append(distinct("""<p><b>A database is not simply "a better file".</b> For a single-user desktop
application, adding a database adds a dependency, a driver, a schema, a migration concern and a
failure mode. BasinWatch treats its database as <i>optional</i> precisely because the file layer
already satisfies the essential requirements. The database earns its place by enabling queries, not by
being more modern.</p>"""))

B10.append("""
<h3><span class="n">10.3</span>Relational structure in one page</h3>
<p>A relational database stores data in <b>tables</b>. A table has named <b>columns</b> with declared
<b>types</b> and zero or more <b>rows</b>. A <b>primary key</b> uniquely identifies a row; a
<b>foreign key</b> references a row in another table, which is how relationships are expressed.</p>
""")

B10.append(code('''CREATE TABLE sensor_readings (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    reading_tick      INTEGER NOT NULL,
    station_id        TEXT    NOT NULL,
    zone_id           TEXT    NOT NULL,
    rainfall_mm       REAL    NOT NULL,
    rise_cm           REAL    NOT NULL,
    water_level_m     REAL    NOT NULL,
    risk_level        TEXT    NOT NULL,
    risk_escalated    INTEGER NOT NULL,
    recorded_at       TEXT    NOT NULL
);

CREATE INDEX idx_sensor_readings_zone_time
    ON sensor_readings (zone_id, recorded_at DESC);''',
"from BasinWatch, db/DatabaseInitializer.java — one table and the index that makes the history query fast.", lang="sql"))

B10.append("""
<p>Read that definition as a set of promises the database will enforce for you.</p>

<p><span class="mono">PRIMARY KEY AUTOINCREMENT</span> gives every row a unique identity without the
application inventing one. <span class="mono">NOT NULL</span> on every column means a missing value is
rejected rather than silently stored as null. The types are declared, so
<span class="mono">rainfall_mm</span> cannot hold the text "twelve".</p>

<p>The index is the important line. Without it, a query for one zone's recent readings must examine
every row. With it, the database walks the index directly to the matching rows in the right order —
which is exactly the query the interface makes.</p>
""")

B10.append("""
<h3><span class="n">10.4</span>SQL in four verbs</h3>
<p>Almost everything an application does with a database is one of four operations, and the acronym
CRUD names them.</p>
""")

B10.append(table(
  ["Operation", "SQL", "Returns", "BasinWatch example"],
  [
    ["Create", "<span class='mono'>INSERT INTO table (columns) VALUES (?, ?)</span>", "an update count",
     "Store one accepted sensor reading"],
    ["Read", "<span class='mono'>SELECT columns FROM table WHERE condition</span>", "a result set",
     "The 200 most recent history entries"],
    ["Update", "<span class='mono'>UPDATE table SET column = ? WHERE condition</span>", "an update count",
     "Mark a mission as completed"],
    ["Delete", "<span class='mono'>DELETE FROM table WHERE condition</span>", "an update count",
     "Not used — history is retained by design"],
  ],
  caption="<b>Table 10.3</b> — CRUD mapped to SQL, with the project's use of each."))

B10.append(related("""<p>BasinWatch never deletes from its history tables. For an audit log that is
the right choice — you want to be able to explain what happened last month. Real systems handle
retention with a time-based purge, an archival export, or partitioning. If you are asked in a viva
"what about the database growing forever?", that is the honest answer: the current design trades disk
space for a complete record, and a production system would add a retention policy.</p>"""))

B10.append("""
<h3><span class="n">10.5</span>Where JDBC fits</h3>
<p>Java cannot speak SQL to a database directly. There is no shared memory, no common protocol, and
each database vendor has its own wire format. JDBC is the layer that bridges the gap.</p>
""")

B10.append(defbox("JDBC",
"the Java Database Connectivity API: a standard set of interfaces in <span class='mono'>java.sql</span> that let Java code open a connection, send SQL, and read results without depending on a particular database product."))

B10.append(figure("d11_jdbc_architecture", "13", "The JDBC architecture",
"Java application code calls only the java.sql interfaces. DriverManager selects a registered driver, the driver converts the calls into the database's own protocol, and the database executes the SQL. Results travel back through the same layers.",
"landscape"))

B10.append("""
<p>The key idea is that the application depends on <i>interfaces</i>, not on the database. Change from
SQLite to PostgreSQL and the application code does not change — only the driver on the classpath and
the connection URL do.</p>
""")

B10.append(connect("""<p>Chapter 17 shows how that driver actually arrives on the classpath: as a Maven
dependency. And Chapter 19 shows what happens when a framework like Spring wraps these same interfaces
in a higher-level abstraction. JDBC is the foundation both approaches share.</p>"""))

B10.append("""
<h3><span class="n">10.6</span>Why SQLite specifically</h3>
<p>SQLite is a complete relational database implemented as a library, not as a server. The database is
a single file on disk, and the "connection" is a handle to that file. For an offline desktop
application that is an ideal fit.</p>
""")

B10.append(table(
  ["Property", "Server database (PostgreSQL, MySQL)", "SQLite"],
  [
    ["Process", "A separate server process", "Linked into your program as a library"],
    ["Installation", "Install, configure and start the server", "Add one jar to the classpath"],
    ["Connection", "Network connection, host, port, credentials", "A path to a file"],
    ["Concurrent writers", "Many, with row and table locking", "One at a time — the whole file is locked for a write"],
    ["Ideal for", "Multi-user, network, high concurrency", "Embedded, single-user, desktop, testing"],
    ["Used by BasinWatch?", "<b>No</b>", "<b>Yes</b> — the only database the project uses"],
  ],
  caption="<b>Table 10.4</b> — Server databases and SQLite, and why the latter suits a desktop application."))

B10.append(exam("""<p>A common question asks why JDBC is described as a "thin" API. The answer is that
it does very little itself: it defines interfaces and a driver-registration mechanism, and delegates
almost all real work to the driver. That thinness is exactly why it works with any database and why
frameworks can build on it.</p>"""))

B10.append(summary([
  "Data can live in memory, in files, or in a database; the decisive difference is selective access via indexes.",
  "BasinWatch keeps all three because different questions need different mechanisms, not because one is superior.",
  "A relational table declares columns, types and constraints, and a primary key gives every row an identity.",
  "An index is what makes a query fast; without one, the database examines every row.",
  "CRUD maps to INSERT, SELECT, UPDATE and DELETE, and the project deliberately never deletes.",
  "JDBC is a set of interfaces plus a driver mechanism; the application depends on the interfaces, so the database can be swapped.",
  "SQLite is a library, not a server, which is why it suits an offline desktop application.",
]))

B10.append(keyterms([
  "<b>Table</b> — a named collection of rows sharing the same columns.",
  "<b>Primary key</b> — the column or columns uniquely identifying each row.",
  "<b>Index</b> — an auxiliary structure that speeds up lookups on particular columns.",
  "<b>Constraint</b> — a rule the database enforces, such as <span class='mono'>NOT NULL</span>.",
  "<b>JDBC</b> — the standard Java API for relational database access.",
]))

B10.append("</div>")

# ======================================================================
# CHAPTER 11
# ======================================================================
B11.append(chapter(11, "JDBC Architecture and Drivers",
"The interfaces, the driver's job, the four driver types, and how a connection is actually established."))

B11.append("""
<h3><span class="n">11.1</span>The two halves of JDBC</h3>
<p>JDBC is deliberately split in two. One half is fixed and shipped with Java: the interfaces in
<span class="mono">java.sql</span>. The other half is supplied by whoever makes the database: the
driver, which implements those interfaces for one specific product.</p>
""")

B11.append(table(
  ["Interface", "Defined in", "Implemented by", "The application uses it to"],
  [
    ["<span class='mono'>Driver</span>", "<span class='mono'>java.sql</span>", "The database vendor", "Accept a URL and decide whether it can handle it"],
    ["<span class='mono'>Connection</span>", "<span class='mono'>java.sql</span>", "The vendor's driver", "Hold a session with the database"],
    ["<span class='mono'>Statement</span>", "<span class='mono'>java.sql</span>", "The vendor's driver", "Send fixed SQL"],
    ["<span class='mono'>PreparedStatement</span>", "<span class='mono'>java.sql</span>", "The vendor's driver", "Send parameterized SQL, safely"],
    ["<span class='mono'>CallableStatement</span>", "<span class='mono'>java.sql</span>", "The vendor's driver", "Invoke a stored procedure"],
    ["<span class='mono'>ResultSet</span>", "<span class='mono'>java.sql</span>", "The vendor's driver", "Iterate over the rows a query returned"],
    ["<span class='mono'>SQLException</span>", "<span class='mono'>java.sql</span>", "The vendor's driver", "Report a database error"],
    ["<span class='mono'>DriverManager</span>", "<span class='mono'>java.sql</span>", "The JDK", "Choose a driver for a URL and hand back a connection"],
  ],
  caption="<b>Table 11.1</b> — The JDBC interfaces and who implements them."))

B11.append(core("""<p>This is the single most important structural fact about JDBC, and it is worth
stating plainly: <b>every method you call on a <span class='mono'>Connection</span> is code you have
never read</b>. The interface is in the JDK; the implementation is in the driver jar. That is why
changing the driver can change behaviour, and why exact exception messages differ between
databases.</p>"""))

B11.append("""
<h3><span class="n">11.2</span>What the driver actually does</h3>
<p>A driver has four responsibilities.</p>

<ol>
<li><b>Recognise its own URLs.</b> Given <span class="mono">jdbc:sqlite:data/basinwatch.db</span>, the
SQLite driver accepts it and other drivers decline.</li>
<li><b>Open a connection.</b> For SQLite that means opening the file; for PostgreSQL it means a TCP
connection, a handshake and authentication.</li>
<li><b>Translate calls into the database's protocol.</b> A
<span class="mono">PreparedStatement.setDouble(3, 12.4)</span> becomes whatever bytes that database
expects.</li>
<li><b>Translate results back.</b> A result row becomes a <span class="mono">ResultSet</span>
positioned on that row, with typed getters.</li>
</ol>
""")

B11.append(visual("""<p>Follow Diagram 13 with those four responsibilities in mind. The application
touches only the top band. <span class='mono'>DriverManager</span> is the switchboard. The driver is
the translator. Everything below it belongs to the database.</p>"""))

B11.append("""
<h3><span class="n">11.3</span>The four driver types</h3>
<p>JDBC drivers are classified into four types by their architecture. The classification is a standard
examination topic, and it is also genuinely useful for understanding why modern drivers are the way
they are.</p>
""")

B11.append(table(
  ["Type", "Name", "How it works", "Pros", "Cons"],
  [
    ["1", "JDBC–ODBC bridge", "Java calls an ODBC driver through native code",
     "Could reach any database with an ODBC driver",
     "Deprecated and removed; required native code and a platform ODBC stack"],
    ["2", "Native-API driver", "Java calls the vendor's native client library",
     "Slightly faster than type 1",
     "Requires the vendor's client library installed on every machine"],
    ["3", "Network-protocol driver", "Java talks to a middleware server that talks to the database",
     "One driver for many databases; useful behind a firewall",
     "An extra server to install, configure and maintain"],
    ["4", "Thin driver", "Pure Java, speaks the database's own protocol directly",
     "<b>No native code, no middleware, one jar, portable</b>",
     "One driver per database product"],
  ],
  caption="<b>Table 11.2</b> — The four JDBC driver types."))

B11.append(clarify("""<p><b>Type 1 is no longer available.</b> The
<span class='mono'>jdbc-odbc</span> bridge was deprecated and then removed from the JDK; it does not
exist on a modern Java runtime. If a lecture note presents it as a current option, the correct modern
position is: it was type 1, it is historical, and types 3 and 4 are what remain in practice. Types 3
and 4 have largely converged, because modern databases provide efficient binary wire protocols that a
thin driver can speak directly.</p>"""))

B11.append("""
<h3><span class="n">11.4</span>How a connection is established</h3>
<p>Three things are needed: a URL, the driver on the classpath, and a call to
<span class="mono">DriverManager</span>.</p>
""")

B11.append(code('''// the URL names the driver family, then whatever that driver needs
jdbc:sqlite:data/basinwatch.db
jdbc:postgresql://localhost:5432/basinwatch
jdbc:mysql://localhost:3306/basinwatch?useSSL=false

// opening a connection
String url = "jdbc:sqlite:data/basinwatch.db";
try (Connection connection = DriverManager.getConnection(url)) {
    // ... use the connection
}   // the connection is closed here''', "illustrative — the JDBC URL shape and the connection call"))

B11.append("""
<p>The URL is the only piece of configuration that names the database product, which is why changing
databases is usually a change to one string and one dependency.</p>
""")

B11.append("""
<h3><span class="n">11.5</span>Driver registration</h3>
<p>For <span class="mono">DriverManager</span> to find a driver, the driver class must be registered.
There are three ways this can happen.</p>
""")

B11.append(table(
  ["Mechanism", "How it works", "When to use it"],
  [
    ["Service provider file",
     "The driver jar contains <span class='mono'>META-INF/services/java.sql.Driver</span> naming the class. The JDK loads it automatically.",
     "<b>The normal case.</b> Modern drivers do this, so no code is needed."],
    ["<span class='mono'>Class.forName(...)</span>",
     "Explicitly loads the driver class, which registers itself in a static initialiser.",
     "Legacy code, or a driver with no service file. Still seen in older textbooks."],
    ["<span class='mono'>DriverManager.registerDriver(...)</span>",
     "Registers a driver instance directly.",
     "Unusual; used when constructing a driver manually."],
  ],
  caption="<b>Table 11.3</b> — Three ways a driver becomes available to <span class='mono'>DriverManager</span>."))

B11.append(mistake("""<p>Writing <span class='mono'>Class.forName("org.sqlite.JDBC")</span> in modern
code. It is harmless but unnecessary: the SQLite driver ships a service file, so the JDK discovers it
automatically. More importantly, the habit hides a real question — <i>is the driver actually on the
classpath?</i> If it is not, <span class='mono'>DriverManager</span> throws
<span class='mono'>SQLException: No suitable driver found for jdbc:sqlite:...</span>, and no amount of
<span class='mono'>forName</span> will help. The fix is a Maven dependency, not a line of code.
Chapter 17 covers exactly that.</p>"""))

B11.append("""
<h3><span class="n">11.6</span>How BasinWatch manages connections</h3>
<p>The project wraps connection handling in one small class, so no repository has to know the URL.</p>
""")

B11.append(code('''public final class DatabaseManager {
    private static final String DRIVER_CLASS = "org.sqlite.JDBC";
    private final String url;

    public DatabaseManager(Path databaseFile) {
        this.url = "jdbc:sqlite:" + databaseFile.toAbsolutePath();
    }

    public Connection openConnection() throws SQLException {
        Connection connection = DriverManager.getConnection(url);
        connection.setAutoCommit(true);            // each statement commits on its own
        return connection;
    }

    public boolean isAvailable() {
        try (Connection connection = openConnection()) {
            return connection.isValid(2);          // two-second validity check
        } catch (SQLException ex) {
            return false;                          // absence is reported, not thrown
        }
    }

    public String url() {
        return url;
    }
}''', "from BasinWatch, db/DatabaseManager.java — one place that knows the URL."))

B11.append("""
<p>Three decisions in that class shape everything downstream.</p>

<p><b>The URL is built once, in the constructor.</b> No other class contains the string
<span class="mono">"jdbc:sqlite:"</span>.</p>

<p><b><span class="mono">isAvailable</span> returns a boolean rather than throwing.</b> This is what
makes the database optional. The application asks "is history available?" and handles both answers,
instead of being forced to handle an exception merely to find out.</p>

<p><b>Autocommit is set explicitly.</b> It is the default, but stating it documents the decision — and
Chapter 13 shows the one place where it is deliberately turned off.</p>
""")

B11.append(connect("""<p>Notice that <span class='mono'>isAvailable</span> catches
<span class='mono'>SQLException</span> and converts it into <span class='mono'>false</span>. That is an
exception-translation decision, and Chapter 14 explains why the rest of the application depends on it:
an unavailable database must not prevent the application from running.</p>"""))

B11.append(exam("""<p>Two questions recur. "What does the driver do?" — answer with the four
responsibilities: recognise the URL, open the connection, translate calls to the protocol, translate
results back. "Which driver type does your project use?" — type 4, a pure-Java thin driver, which is
why it needs only a jar on the classpath and no native library.</p>"""))

B11.append(summary([
  "JDBC is split between fixed interfaces in <span class='mono'>java.sql</span> and a vendor-supplied driver that implements them.",
  "A driver recognises its own URLs, opens connections, translates calls to the database protocol, and translates results back.",
  "The four driver types are the ODBC bridge (removed), native-API, network-protocol middleware, and the pure-Java thin driver.",
  "A connection needs a URL of the form <span class='mono'>jdbc:product:details</span> and a driver on the classpath.",
  "Modern drivers register themselves through a service file, so <span class='mono'>Class.forName</span> is no longer required.",
  "\u201cNo suitable driver found\u201d means the driver jar is missing, not that registration code is missing.",
  "BasinWatch builds the URL in one place and reports database availability as a boolean rather than an exception.",
]))

B11.append(keyterms([
  "<b>JDBC URL</b> — a string of the form <span class='mono'>jdbc:product:details</span> identifying a database to connect to.",
  "<b>Thin driver</b> — a pure-Java type 4 driver that needs no native code.",
  "<b>DriverManager</b> — the JDK class that selects a registered driver for a URL and returns a connection.",
  "<b>Service provider file</b> — <span class='mono'>META-INF/services/java.sql.Driver</span>, which lets a driver register itself automatically.",
  "<b>Autocommit</b> — the mode in which each statement is its own transaction.",
]))

B11.append("</div>")

# ======================================================================
# CHAPTER 12
# ======================================================================
B12.append(chapter(12, "SQL Execution Through JDBC",
"Connection, Statement, PreparedStatement, CallableStatement, ResultSet, CRUD operations, and the complete execution lifecycle."))

B12.append("""
<h3><span class="n">12.1</span>The objects in one query</h3>
<p>Executing a query involves a small cast of objects, each with one job. It is worth meeting them
before looking at any code.</p>
""")

B12.append(table(
  ["Object", "Job", "Created by", "Closed by"],
  [
    ["<span class='mono'>Connection</span>", "A session with the database", "<span class='mono'>DriverManager.getConnection(url)</span>", "try-with-resources"],
    ["<span class='mono'>Statement</span>", "A container for fixed SQL", "<span class='mono'>connection.createStatement()</span>", "try-with-resources"],
    ["<span class='mono'>PreparedStatement</span>", "A pre-compiled statement with placeholders", "<span class='mono'>connection.prepareStatement(sql)</span>", "try-with-resources"],
    ["<span class='mono'>CallableStatement</span>", "A stored-procedure invocation", "<span class='mono'>connection.prepareCall(sql)</span>", "try-with-resources"],
    ["<span class='mono'>ResultSet</span>", "A cursor over the rows a query returned", "Returned by <span class='mono'>executeQuery()</span>", "try-with-resources"],
    ["<span class='mono'>SQLException</span>", "A database failure", "Thrown by any of the above", "Caught by the caller"],
  ],
  caption="<b>Table 12.1</b> — The objects involved in executing SQL."))

B12.append(figure("d12_sql_execution_lifecycle", "14", "The SQL execution lifecycle",
"From obtaining a connection through preparing a statement, binding parameters, executing, iterating the result set, and closing every resource in reverse order. The two execution paths — query and update — diverge after execution and converge again at cleanup.",
"portrait"))

B12.append("""
<h3><span class="n">12.2</span>Three kinds of statement</h3>
<p>All three statement types implement the same interface, but they exist for different reasons and
one of them is the right default.</p>
""")

B12.append(table(
  ["", "Statement", "PreparedStatement", "CallableStatement"],
  [
    ["SQL", "Fixed, assembled in Java", "Fixed template with <span class='mono'>?</span> placeholders", "A stored procedure call"],
    ["Parameters", "None — values are concatenated into the string", "Bound with typed setters", "Bound as input, and registered as output"],
    ["Pre-compiled by the database?", "No — parsed on every execution", "<b>Yes</b> — parsed once, executed many times", "Yes"],
    ["Safe against SQL injection?", "<b>No</b>", "<b>Yes</b>", "<b>Yes</b>"],
    ["Efficient in a loop?", "No — reparsed each time", "<b>Yes</b>", "Yes"],
    ["Typical use", "A one-off DDL statement such as <span class='mono'>CREATE TABLE</span>", "Everything the application does repeatedly", "Calling a procedure that returns values"],
  ],
  caption="<b>Table 12.2</b> — The three statement types and when each is appropriate."))

B12.append(figure("d14_statement_types", "15", "Statement, PreparedStatement and CallableStatement",
"One interface family, three levels of capability. Statement sends fixed SQL with no parameters; PreparedStatement adds numbered placeholders and pre-parsing; CallableStatement adds stored-procedure invocation with registered output parameters.",
"landscape"))

B12.append(core("""<p><b>Use <span class='mono'>PreparedStatement</span> by default.</b> It is safer,
it is faster when reused, and it makes the SQL readable by separating the statement from the values.
<span class='mono'>Statement</span> is for statements that genuinely have no parameters — schema
creation, for example — and <span class='mono'>CallableStatement</span> is for stored procedures.</p>"""))

B12.append("""
<h3><span class="n">12.3</span>Why PreparedStatement matters: SQL injection</h3>
<p>This is the most important practical lesson in the chapter, and the demonstration is short.</p>
""")

B12.append(code('''// ---- DANGEROUS: values concatenated into the SQL text ----
String zone = userInput;                                  // e.g.  MIL' OR '1'='1
String sql = "SELECT * FROM sensor_readings WHERE zone_id = '" + zone + "'";
Statement statement = connection.createStatement();
ResultSet rs = statement.executeQuery(sql);

// the database actually receives:
//   SELECT * FROM sensor_readings WHERE zone_id = 'MIL' OR '1'='1'
// the OR clause is now part of the statement, so EVERY row matches.

// ---- SAFE: the value is bound, never parsed as SQL ----
String safeSql = "SELECT * FROM sensor_readings WHERE zone_id = ?";
try (PreparedStatement ps = connection.prepareStatement(safeSql)) {
    ps.setString(1, userInput);                           // bound as a VALUE
    try (ResultSet rs2 = ps.executeQuery()) {
        // the database receives a plan for the fixed text,
        // plus one parameter whose value is MIL' OR '1'='1 -- a literal string
    }
}''', "illustrative — the injection vulnerability and its fix", lang="sql"))

B12.append("""
<p>The difference is not about escaping characters. With a
<span class="mono">PreparedStatement</span>, the SQL text is sent to the database and <i>parsed</i>
before the parameter values are supplied. The parser has already decided what is a statement and what
is a value, so no value can become part of the statement's structure. Quoting and escaping become
irrelevant because the value never enters the parser's input.</p>
""")

B12.append(distinct("""<p><b>Concatenating values into SQL is unsafe even when you escape them
yourself.</b> Manual escaping has to handle quote characters, backslashes, multi-byte encodings and
database-specific syntax, and getting it subtly wrong is easy. Binding parameters removes the problem
entirely rather than mitigating it. BasinWatch uses
<span class='mono'>PreparedStatement</span> at every site, including the statements with no
parameters.</p>"""))

B12.append("""
<h3><span class="n">12.4</span>Binding parameters</h3>
<p>Placeholders are numbered from one, and each needs a typed setter matching the column's type.</p>
""")

B12.append(figure("d13_prepared_statement_binding", "16", "PreparedStatement parameter binding",
"An SQL template with numbered placeholders, the typed setter call for each, and the value the database receives. The order of the placeholders is what the index refers to — not the order of the setter calls.",
"landscape"))

B12.append(code('''String sql = """
        INSERT INTO sensor_readings (reading_tick, station_id, zone_id, rainfall_mm,
                                     rise_cm, water_level_m, risk_level,
                                     risk_escalated, recorded_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """;

try (PreparedStatement statement = connection.prepareStatement(sql)) {
    statement.setLong(1, reading.tick());                       // 1 -> reading_tick
    statement.setString(2, reading.stationId());                // 2 -> station_id
    statement.setString(3, reading.zoneId());                   // 3 -> zone_id
    statement.setDouble(4, reading.rainfallMillimeters());      // 4 -> rainfall_mm
    statement.setDouble(5, reading.observedRiseCentimeters());  // 5 -> rise_cm
    statement.setDouble(6, zone.waterLevelMeters());            // 6 -> water_level_m
    statement.setString(7, zone.risk().name());                 // 7 -> risk_level
    statement.setInt(8, riskEscalated ? 1 : 0);                 // 8 -> risk_escalated
    statement.setString(9, timestamp.toString());               // 9 -> recorded_at
    statement.executeUpdate();
}''', "from BasinWatch, db/SensorReadingRepository.java — nine placeholders, nine typed setters.", lang="sql"))

B12.append(visual("""<p>Count the placeholders in that statement, then count the setter calls. There are
nine of each, and the indices run 1 to 9 with no gaps. That is the check to perform whenever you read
JDBC code: a missing setter, or an index that skips a number, means a parameter silently retains
whatever value it had.</p>"""))

B12.append(table(
  ["SQL type", "Setter", "Java type"],
  [
    ["<span class='mono'>INTEGER</span>", "<span class='mono'>setInt</span> / <span class='mono'>setLong</span>", "<span class='mono'>int</span> / <span class='mono'>long</span>"],
    ["<span class='mono'>REAL</span>", "<span class='mono'>setDouble</span> / <span class='mono'>setFloat</span>", "<span class='mono'>double</span> / <span class='mono'>float</span>"],
    ["<span class='mono'>TEXT</span>", "<span class='mono'>setString</span>", "<span class='mono'>String</span>"],
    ["<span class='mono'>BOOLEAN</span>", "<span class='mono'>setBoolean</span>", "<span class='mono'>boolean</span>"],
    ["<span class='mono'>NULL</span>", "<span class='mono'>setNull(index, java.sql.Types.X)</span>", "any reference type"],
    ["A date or timestamp", "<span class='mono'>setTimestamp</span> / <span class='mono'>setDate</span>", "<span class='mono'>java.sql.Timestamp</span> / <span class='mono'>java.sql.Date</span>"],
  ],
  caption="<b>Table 12.3</b> — The common setters and the SQL types they correspond to."))

B12.append(mistake("""<p>Two binding mistakes appear constantly. First, off-by-one indices:
placeholders are <b>1-based</b>, so the first setter is <span class='mono'>setX(1, ...)</span>, not
zero. Second, treating a boolean as a boolean in SQLite: the column here is declared
<span class='mono'>INTEGER</span>, so the code converts with
<span class='mono'>riskEscalated ? 1 : 0</span> rather than assuming a native boolean type
exists.</p>"""))

B12.append("""
<h3><span class="n">12.5</span>Executing: query versus update</h3>
<p>After binding, the two execution paths diverge and the choice is determined by whether the
statement returns rows.</p>
""")

B12.append(table(
  ["Method", "Use for", "Returns", "Typical statement"],
  [
    ["<span class='mono'>executeQuery()</span>", "Statements that produce rows", "A <span class='mono'>ResultSet</span>",
     "<span class='mono'>SELECT</span>"],
    ["<span class='mono'>executeUpdate()</span>", "Statements that change rows", "An <span class='mono'>int</span>: rows affected",
     "<span class='mono'>INSERT</span>, <span class='mono'>UPDATE</span>, <span class='mono'>DELETE</span>"],
    ["<span class='mono'>execute()</span>", "When you do not know which will happen", "A <span class='mono'>boolean</span>: true if a result set is available",
     "Dynamic or DDL statements"],
    ["<span class='mono'>executeBatch()</span>", "Several statements at once", "An <span class='mono'>int[]</span> of counts",
     "Bulk inserts"],
  ],
  caption="<b>Table 12.4</b> — Execution methods and what each returns."))

B12.append(core("""<p>The return value of <span class='mono'>executeUpdate()</span> is worth using
rather than discarding. It is the number of rows the statement actually affected, which tells you
whether your <span class='mono'>WHERE</span> clause matched anything. An
<span class='mono'>UPDATE</span> returning zero almost always means the condition was wrong, and that
is worth knowing.</p>"""))

B12.append("""
<h3><span class="n">12.6</span>Reading a ResultSet</h3>
<p>A result set is a cursor. It starts <i>before</i> the first row, so the loop must advance before
reading.</p>
""")

B12.append(code('''public List<DatabaseHistoryEntry> loadHistory(Connection connection, int limit)
        throws SQLException {
    String sql = """
            SELECT occurred_at, event_type, zone_id, detail
              FROM operational_events
             ORDER BY occurred_at DESC
             LIMIT ?
            """;
    ArrayList<DatabaseHistoryEntry> entries = new ArrayList<>();
    try (PreparedStatement statement = connection.prepareStatement(sql)) {
        statement.setInt(1, limit);
        try (ResultSet rows = statement.executeQuery()) {
            while (rows.next()) {                          // advance, then read
                entries.add(new DatabaseHistoryEntry(
                        DatabaseHistoryType.valueOf(rows.getString("event_type")),
                        rows.getString("zone_id"),
                        rows.getString("detail"),
                        Instant.parse(rows.getString("occurred_at"))));
            }
        }
    }
    return List.copyOf(entries);
}''', "from BasinWatch, db/OperationalEventRepository.java — the canonical read loop.", lang="sql"))

B12.append("""
<p>Four habits in that method are the whole of result-set handling.</p>

<p><b>The loop is <span class="mono">while (rows.next())</span>.</b>
<span class="mono">next()</span> moves the cursor and returns false when there are no more rows. A
<span class="mono">do-while</span> would be wrong, because the cursor starts before the first row.</p>

<p><b>Columns are read by name.</b> <span class="mono">rows.getString("event_type")</span> is clearer
than <span class="mono">rows.getString(2)</span> and survives a change to the select list. The
trade-off is a small lookup cost, which is irrelevant here.</p>

<p><b>Each row is converted into a domain object inside the loop.</b> The method returns
<span class="mono">List&lt;DatabaseHistoryEntry&gt;</span>, not a
<span class="mono">ResultSet</span>. That is essential: a result set is tied to its statement and its
connection, and once they close it is unusable. Converting immediately means the caller receives
ordinary values.</p>

<p><b><span class="mono">List.copyOf</span> makes the result immutable.</b> The same discipline as
every other boundary in the project.</p>
""")

B12.append(mistake("""<p>Returning a <span class='mono'>ResultSet</span> from a method that also
closes the connection. The caller receives an object that looks usable and fails with
<span class='mono'>SQLException: ResultSet closed</span> on the first
<span class='mono'>next()</span>. The rule is that a result set never outlives the block that created
it — map rows into your own objects before leaving.</p>"""))

B12.append("""
<h3><span class="n">12.7</span>SQLException and what it tells you</h3>
<p>Every JDBC method that touches the database can throw
<span class="mono">SQLException</span>. It is checked, and it carries more information than a plain
message.</p>
""")

B12.append(table(
  ["Method", "Meaning"],
  [
    ["<span class='mono'>getMessage()</span>", "The driver's description, often including the database's own error text"],
    ["<span class='mono'>getSQLState()</span>", "A five-character standard code, such as <span class='mono'>23505</span> for a unique-constraint violation"],
    ["<span class='mono'>getErrorCode()</span>", "A vendor-specific numeric code"],
    ["<span class='mono'>getNextException()</span>", "A chained second failure, when one statement produces several errors"],
    ["<span class='mono'>getCause()</span>", "The underlying exception, such as an <span class='mono'>IOException</span> from the database file"],
  ],
  caption="<b>Table 12.5</b> — What an <span class='mono'>SQLException</span> carries."))

B12.append("""
<h3><span class="n">12.8</span>The complete lifecycle, in order</h3>
<p>Everything in this chapter reduces to one sequence. Learn it as a sequence, because examiners and
reviewers both ask for it.</p>
""")

B12.append(trace("The eight steps of a parameterized query", [
  "<b>Obtain a connection.</b> <span class='mono'>DriverManager.getConnection(url)</span>, inside try-with-resources.",
  "<b>Prepare the statement.</b> <span class='mono'>connection.prepareStatement(sql)</span> sends the SQL text to the database, which parses and plans it once.",
  "<b>Bind every parameter.</b> One typed setter per placeholder, indices 1 to n, no gaps.",
  "<b>Execute.</b> <span class='mono'>executeQuery()</span> for a read, <span class='mono'>executeUpdate()</span> for a write.",
  "<b>Consume the result.</b> For a query, loop with <span class='mono'>while (rows.next())</span> and map each row into a domain object. For an update, check the returned row count.",
  "<b>Close the result set.</b> Handled by its own try-with-resources block.",
  "<b>Close the statement.</b> Handled by the statement's try-with-resources block.",
  "<b>Close the connection.</b> Handled by the outermost try-with-resources block — and this is where a transaction would be committed or rolled back.",
]))

B12.append(connect("""<p>Step eight is where Chapter 13 begins. Everything above happens inside a
transaction, whether you think about it or not: in autocommit mode each statement is its own
transaction, and turning autocommit off lets several statements share one.</p>"""))

B12.append(exam("""<p>If asked to "write the code to insert a row safely", the marks are distributed
roughly as follows: using <span class='mono'>PreparedStatement</span> rather than concatenation;
binding every parameter with the correct type and 1-based index; using
<span class='mono'>executeUpdate</span>; and closing all three resources. Mentioning
<span class='mono'>try-with-resources</span> explicitly is usually worth a mark on its own.</p>"""))

B12.append(summary([
  "A query involves a Connection, a Statement of some kind, and possibly a ResultSet, all of which must be closed.",
  "PreparedStatement is the default choice: safer, pre-parsed, and reusable.",
  "Concatenating values into SQL permits injection; binding parameters makes the value unable to become part of the statement.",
  "Placeholders are numbered from one and each needs a typed setter whose Java type matches the SQL type.",
  "executeQuery returns a ResultSet; executeUpdate returns a row count; execute returns a boolean.",
  "A ResultSet cursor starts before the first row, so the loop must call next() before reading.",
  "Map each row into your own object inside the loop; never return a ResultSet from a method that closes its connection.",
  "SQLException carries a message, an SQLState, a vendor error code, and possibly chained exceptions.",
]))

B12.append(keyterms([
  "<b>Placeholder</b> — the <span class='mono'>?</span> character in a prepared statement, replaced by a bound value.",
  "<b>SQL injection</b> — an attack in which user input becomes part of a statement's structure.",
  "<b>ResultSet cursor</b> — the position marker that starts before the first row.",
  "<b>Row count</b> — the number of rows an update affected, returned by <span class='mono'>executeUpdate</span>.",
  "<b>SQLState</b> — the standard five-character error code carried by a <span class='mono'>SQLException</span>.",
]))

B12.append("</div>")

# ======================================================================
# CHAPTER 13
# ======================================================================
B13.append(chapter(13, "Database Transactions and Reliable Persistence",
"Transaction boundaries, commit and rollback, and why several related changes must succeed or fail together."))

B13.append("""
<h3><span class="n">13.1</span>The problem: a half-finished operation</h3>
<p>Consider what a dispatch actually involves. A mission row must be created. Several resource
counts must be decremented. An event must be recorded for the audit trail. These are three separate
statements against three separate tables.</p>

<p>If the first succeeds and the second fails, the database now claims a mission is running with
resources that were never deducted. That is not a small inconsistency: the resource board will be
wrong for the rest of the session, and the history will not explain why.</p>
""")

B13.append(defbox("Transaction",
"a group of database operations treated as a single unit: either every operation in the group takes effect, or none of them does."))

B13.append(figure("d15_transaction", "17", "Transaction commit and rollback",
"Three statements inside one transaction. On success the connection commits and all three changes become visible together. On failure the connection rolls back and the database returns to its state before the transaction began — including the statements that had already succeeded.",
"landscape"))

B13.append("""
<h3><span class="n">13.2</span>The four guarantees</h3>
<p>Transactions are described by four properties, known by the acronym ACID. Each is worth
understanding in concrete terms rather than as a slogan.</p>
""")

B13.append(table(
  ["Property", "Means", "In this project"],
  [
    ["<b>Atomicity</b>", "All operations take effect, or none do", "A dispatch writes a mission, deducts resources and logs an event — or writes nothing"],
    ["<b>Consistency</b>", "The database moves from one valid state to another", "<span class='mono'>NOT NULL</span> and type constraints hold at commit time"],
    ["<b>Isolation</b>", "Concurrent transactions do not see each other's partial work", "The database work runs on a single thread, so there is one writer"],
    ["<b>Durability</b>", "Once committed, the change survives a crash", "SQLite flushes the committed transaction to the database file"],
  ],
  caption="<b>Table 13.1</b> — The ACID properties and what each means here."))

B13.append("""
<h3><span class="n">13.3</span>Controlling a transaction in JDBC</h3>
<p>By default a connection is in <b>autocommit</b> mode: each statement is committed immediately as
its own transaction. Turning autocommit off gives you control.</p>
""")

B13.append(code('''connection.setAutoCommit(false);        // begin: nothing commits until you say so
try {
    // ... statement 1
    // ... statement 2
    // ... statement 3
    connection.commit();                // all three become visible together
} catch (SQLException ex) {
    connection.rollback();              // undo everything since setAutoCommit(false)
    throw ex;
} finally {
    connection.setAutoCommit(true);     // restore the default for the next caller
}''', "illustrative — the standard transaction skeleton"))

B13.append(core("""<p>Notice the shape: turn autocommit off, do the work in a
<span class='mono'>try</span>, commit at the end of the try, roll back in the
<span class='mono'>catch</span>, and restore autocommit in a
<span class='mono'>finally</span>. The <span class='mono'>finally</span> matters when the connection
comes from a pool and will be reused by someone who does not expect an open transaction.</p>"""))

B13.append(mistake("""<p>Forgetting to roll back, or forgetting to restore autocommit. Both leave the
connection in an unexpected state. A missing rollback means a later commit could persist work that
was supposed to be discarded; a missing restore means the next user of a pooled connection
accidentally joins your transaction. BasinWatch avoids the first problem by rolling back in the catch
block and the second by closing the connection afterwards rather than pooling it.</p>"""))

B13.append("""
<h3><span class="n">13.4</span>How BasinWatch records a dispatch</h3>
<p>The dispatch path is the project's one genuine multi-statement operation, and it is where the
transaction is used.</p>
""")

B13.append(code('''public void recordDispatch(ResponseMission mission, ZoneSnapshot zone,
                         Map<ResourceType, Integer> allocation, Instant timestamp) {
    enqueue(() -> {
        try (Connection connection = database.openConnection()) {
            connection.setAutoCommit(false);               // begin the transaction
            try {
                missions.insert(connection, mission, timestamp);        // 1. the mission row
                for (Map.Entry<ResourceType, Integer> entry : allocation.entrySet()) {
                    resourceUsage.insert(connection, mission.id(), entry.getKey(),
                            entry.getValue(), timestamp);               // 2. one row per resource
                }
                operationalEvents.insert(connection, timestamp, "DISPATCH", zone.id(),
                        mission.type().label() + " allocated to " + zone.name());  // 3. the audit event
                connection.commit();                       // all three take effect together
            } catch (SQLException ex) {
                connection.rollback();                     // none of them take effect
                throw ex;
            }
        } catch (SQLException ex) {
            statusReporter.accept("Could not record dispatch: " + ex.getMessage());
        }
    });
}''', "from BasinWatch, db/DatabaseService.java — one transaction, three kinds of write."))

B13.append(visual("""<p>Follow the three numbered writes in that method. If the third throws, the
rollback undoes the first two — so the database never contains a mission with no audit event, or
resource deductions with no mission. That is what atomicity buys, and it is why the transaction
boundary is drawn around all three rather than around each one.</p>"""))

B13.append("""
<h3><span class="n">13.5</span>Why the writes share one connection</h3>
<p>This is the detail that most often goes wrong in student implementations, and it explains the
package-private overloads from Chapter 2.</p>
""")

B13.append(code('''// Each repository can open its own connection — fine for a single write
public void insert(ResponseMission mission, Instant timestamp) throws SQLException {
    try (Connection connection = database.openConnection()) {
        insert(connection, mission, timestamp);
    }
}

// ...but a transaction must span ONE connection, so a shared overload is needed
void insert(Connection connection, ResponseMission mission, Instant timestamp)
        throws SQLException {
    try (PreparedStatement statement = connection.prepareStatement(INSERT_SQL)) {
        statement.setString(1, mission.id());
        // ... bind the rest, then executeUpdate()
    }
}''', "from BasinWatch, db/MissionRepository.java — the two overloads and why both exist."))

B13.append(distinct("""<p><b>A transaction belongs to a connection, not to a statement.</b> Calling
<span class='mono'>commit()</span> on one connection has no effect on work done on another. So if
three repositories each opened their own connection, three separate transactions would exist and
atomicity would be lost entirely — the code would look correct and silently not be. Passing one
connection through every write is the mechanism that makes the transaction real.</p>"""))

B13.append("""
<h3><span class="n">13.6</span>Isolation, and why it is simple here</h3>
<p>Isolation is the property that governs what one transaction can see of another's uncommitted work.
Real systems offer several isolation levels, trading consistency against concurrency, and reasoning
about them is one of the harder parts of database engineering.</p>

<p>BasinWatch sidesteps the whole problem in one design decision: all database work runs on a single
dedicated thread. There is exactly one writer, so there is never a second transaction to interfere.</p>
""")

B13.append(code('''private void enqueue(DatabaseOperation operation) {
    if (!available) {
        return;                                  // database disabled: silently do nothing
    }
    try {
        executor.submit(() -> {
            try {
                operation.run();
            } catch (SQLException ex) {
                statusReporter.accept("Database operation failed: " + ex.getMessage());
            } catch (RuntimeException ex) {
                statusReporter.accept("Unexpected database error: " + ex);
            }
        });
    } catch (RejectedExecutionException ex) {
        statusReporter.accept("Database queue is full; operation dropped.");
    }
}''', "from BasinWatch, db/DatabaseService.java — one single-threaded executor is the whole concurrency policy."))

B13.append("""
<p>That method is worth reading closely, because it is where several chapters meet.</p>

<p><b>The executor is single-threaded.</b> Every database operation runs one after another on
<span class="mono">"basin-database"</span>. No two transactions are ever concurrent, so no isolation
anomaly is possible and no locking policy is needed.</p>

<p><b>An unavailable database is a no-op, not an error.</b> The early return means every call site
can invoke <span class="mono">recordSensor</span> or <span class="mono">recordDispatch</span> without
checking availability first. The optional subsystem is optional at the call site too.</p>

<p><b>Failures are reported, not thrown.</b> A database failure cannot propagate into the event
processing path, because the work happens on a different thread. It is reported through the status
listener and the application continues.</p>

<p><b>A full queue drops the operation rather than blocking.</b>
<span class="mono">RejectedExecutionException</span> is caught and reported. For an optional history
feature, dropping a record is better than stalling the sensor pipeline.</p>
""")

B13.append(connect("""<p>Compare this with the resource allocator in Chapter 3. That used a
synchronized block to make an in-memory reservation atomic. Here the database provides atomicity
through a transaction. Two different mechanisms, one shared goal: never let a partially complete
change be observable.</p>"""))

B13.append(exam("""<p>A likely question is "give an example from your project where a transaction is
needed, and explain what would go wrong without it." The dispatch path is the ideal answer: without a
transaction, a failure after the mission insert would leave a running mission with resources that
were never deducted, so the resource board would be permanently wrong and the audit trail would not
explain it. Naming the three writes and the failure point is what makes the answer convincing.</p>"""))

B13.append(summary([
  "A transaction groups several operations so that all of them take effect or none do.",
  "The ACID properties are atomicity, consistency, isolation and durability.",
  "JDBC connections are in autocommit mode by default; <span class='mono'>setAutoCommit(false)</span> begins a transaction you control.",
  "The standard skeleton is: disable autocommit, work in a try, commit, roll back in the catch, restore autocommit in a finally.",
  "A transaction belongs to a connection, so every statement in it must use that same connection.",
  "BasinWatch's dispatch records a mission, its resource usage and an audit event in one transaction.",
  "All database work runs on one single-threaded executor, so isolation anomalies cannot arise and no locking policy is needed.",
  "A database failure is reported to the status listener rather than propagated into event processing.",
]))

B13.append(keyterms([
  "<b>ACID</b> — atomicity, consistency, isolation, durability.",
  "<b>Commit</b> — making a transaction's changes permanent and visible.",
  "<b>Rollback</b> — discarding a transaction's changes as though they never happened.",
  "<b>Autocommit</b> — the default mode in which each statement is its own transaction.",
  "<b>Isolation level</b> — the degree to which concurrent transactions are prevented from seeing each other's partial work.",
]))

B13.append("</div>")

# ======================================================================
# CHAPTER 14
# ======================================================================
B14.append(chapter(14, "How BasinWatch Uses JDBC and SQLite",
"The database architecture, the schema, the repositories, and a complete trace of a history record from an accepted observation to a table cell."))

B14.append("""
<h3><span class="n">14.1</span>The four classes that make up the database layer</h3>
<p>The whole database subsystem is four kinds of class, each with one responsibility.</p>
""")

B14.append(table(
  ["Class", "Responsibility", "Knows about", "Does not know about"],
  [
    ["<span class='mono'>DatabaseManager</span>", "Hold the URL and hand out connections",
     "The driver, the URL", "Tables, SQL, the domain"],
    ["<span class='mono'>DatabaseInitializer</span>", "Create the tables and indexes if absent",
     "The schema", "Anything else"],
    ["<span class='mono'>DatabaseService</span>", "Own the worker thread, wrap operations in transactions, report failures",
     "Repositories, the status listener", "Swing, files, SQL text"],
    ["<span class='mono'>*Repository</span> (four)", "Turn domain values into SQL and rows back into domain values",
     "Its own table and its SQL", "Threads, transactions, other repositories"],
  ],
  caption="<b>Table 14.1</b> — The four responsibilities of the database layer."))

B14.append(figure("d17_db_dataflow", "18", "Database data flow",
"An accepted observation travels from the engine, through the database service's queue, onto the worker thread, into the repository, through a prepared statement into SQLite. A history read travels the reverse path as a future whose callback returns to the event-dispatch thread.",
"portrait"))

B14.append("""
<h3><span class="n">14.2</span>The schema</h3>
<p>Four tables hold the history. Each corresponds to one kind of thing the application does.</p>
""")

B14.append(code('''CREATE TABLE IF NOT EXISTS sensor_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reading_tick INTEGER NOT NULL,
    station_id TEXT NOT NULL,
    zone_id TEXT NOT NULL,
    rainfall_mm REAL NOT NULL,
    rise_cm REAL NOT NULL,
    water_level_m REAL NOT NULL,
    risk_level TEXT NOT NULL,
    risk_escalated INTEGER NOT NULL,
    recorded_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS missions (
    id TEXT PRIMARY KEY,
    mission_type TEXT NOT NULL,
    zone_id TEXT NOT NULL,
    started_tick INTEGER NOT NULL,
    completes_at_tick INTEGER NOT NULL,
    status TEXT NOT NULL,
    recorded_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS resource_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mission_id TEXT NOT NULL,
    resource_type TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    recorded_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS operational_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    occurred_at TEXT NOT NULL,
    event_type TEXT NOT NULL,
    zone_id TEXT,
    detail TEXT NOT NULL
);''', "from BasinWatch, db/DatabaseInitializer.java — the four tables.", lang="sql"))

B14.append(figure("d16_schema", "19", "The database schema",
"Four tables and the relationships between them. Missions and resource usage are linked by mission id; sensor readings and operational events carry a zone id that names a zone in the model. Every table carries a timestamp so history can be ordered.",
"landscape"))

B14.append("""
<p>Three design decisions are visible in the schema.</p>

<p><b>Every table has a timestamp.</b> History is only useful if it can be ordered and filtered by
time, and <span class="mono">recorded_at</span> is stored as ISO-8601 text so that string ordering
matches chronological ordering — the same choice the log file makes.</p>

<p><b><span class='mono'>missions.id</span> is the primary key and is text.</b> The application already
generates identifiers such as <span class="mono">BW-0001</span> — <span class="mono">"BW-"</span>
followed by a four-digit zero-padded sequence — so the database uses them rather than
inventing a second identity. This is what lets <span class="mono">resource_usage.mission_id</span>
refer to a mission.</p>

<p><b><span class='mono'>operational_events.zone_id</span> is the one nullable column.</b> Not every
event belongs to a zone — a global warning does not — and <span class="mono">NOT NULL</span> would
force a meaningless value.</p>
""")

B14.append(related("""<p>The schema declares the mission relationship with a plain column rather
than a <span class='mono'>FOREIGN KEY ... REFERENCES</span> constraint. That is a deliberate
simplification: SQLite enforces foreign keys only when
<span class='mono'>PRAGMA foreign_keys = ON</span> is set for the connection, so a constraint written
in the schema could be silently ignored. A production schema would enable the pragma and declare the
constraint, so that deleting a mission could not orphan its resource rows. BasinWatch's single-writer
design means the application itself maintains the relationship.</p>"""))

B14.append("""
<h3><span class="n">14.3</span>Initialisation, and why it is idempotent</h3>
<p>The initialiser runs at start-up and must be safe to run every time.</p>
""")

B14.append(code('''public void initialise() throws SQLException {
    try (Connection connection = database.openConnection();
         Statement statement = connection.createStatement()) {
        for (String ddl : SCHEMA) {
            statement.execute(ddl);            // every statement uses IF NOT EXISTS
        }
    }
}''', "from BasinWatch, db/DatabaseInitializer.java — creating the schema is idempotent."))

B14.append("""
<p>The <span class="mono">IF NOT EXISTS</span> clause in every
<span class="mono">CREATE</span> is what makes this safe. Without it, the second launch of the
application would fail with "table already exists". With it, the first launch creates the tables and
every later launch does nothing. This is the simplest possible migration strategy, and it is
appropriate for a project with one schema version.</p>
""")

B14.append(distinct("""<p><b><span class='mono'>Statement</span> is used here, not
<span class='mono'>PreparedStatement</span>.</b> That is correct and deliberate: these are fixed DDL
statements with no parameters, so there is nothing to bind and nothing to inject. It is a useful
example of the one case where <span class='mono'>Statement</span> is the right choice — and it shows
that "always use PreparedStatement" is really "always use it when there are values".</p>"""))

B14.append("""
<h3><span class="n">14.4</span>Tracing a reading from the sensor to the table</h3>
<p>This is the central trace of the chapter. Follow one observation all the way to a stored row.</p>
""")

B14.append(trace("One accepted observation, from pipe to table", [
  "<b>The feed encodes it.</b> <span class='mono'>SensorFeed</span> builds a <span class='mono'>SensorReading</span> and writes <span class='mono'>reading.encode()</span> plus a line separator into the <span class='mono'>PipedWriter</span>.",
  "<b>The intake parses it.</b> <span class='mono'>SensorIntake</span> reads the line and calls <span class='mono'>SensorReading.parse(line)</span>, which validates the field count and ranges.",
  "<b>The intake queues it.</b> <span class='mono'>eventBuffer.put(event)</span> hands it to the workers; the call blocks if the buffer is full.",
  "<b>A worker processes it.</b> One of the three <span class='mono'>ResponseWorker</span> threads takes the event and calls <span class='mono'>model.process(event)</span>, which applies the reading to the zone and returns activity messages.",
  "<b>The worker fans out.</b> The engine appends to the journal, submits to the archive worker, and — if the reading was accepted and changed the zone — calls <span class='mono'>database.recordSensor(...)</span>.",
  "<b>The service queues it.</b> <span class='mono'>recordSensor</span> calls <span class='mono'>enqueue</span>, which submits a lambda to the single-threaded executor and returns immediately.",
  "<b>The worker thread runs it.</b> The lambda opens a connection, and <span class='mono'>SensorReadingRepository.insert</span> prepares the nine-placeholder statement and binds every value.",
  "<b>SQLite executes it.</b> The driver sends the statement and the bound values; the database inserts the row and commits it, because autocommit is on.",
  "<b>If it was a risk escalation, a second insert follows.</b> An <span class='mono'>operational_events</span> row is written with the type <span class='mono'>RISK ESCALATION</span>.",
  "<b>A failure is reported, not thrown.</b> Any <span class='mono'>SQLException</span> is caught by <span class='mono'>enqueue</span>'s lambda and passed to the status listener, which posts it to the interface.",
]))

B14.append(practice("""<p>Step five is where the acceptance test lives, and it is worth seeing
exactly. The engine writes to the database only when the model actually changed:</p>
<pre class="long"><span class="kw">if</span> (event <span class="kw">instanceof</span> <span class="ty">SensorReading</span> reading) {
    <span class="ty">ZoneSnapshot</span> zone = model.zone(reading.zoneId());
    <span class="kw">boolean</span> riskEscalated = zone.risk().rank() &gt; previousRiskRank;
    database.recordSensor(reading, zone, <span class="ty">Instant</span>.now(), riskEscalated);
}</pre>
<div class="codecap"><b>Listing 14.1</b> — from BasinWatch, <span class="mono">engine/BasinEngine.java</span></div>
<p>This is why Chapter 2's stale-reading guard matters. A reading older than the last one applied is
rejected by <span class="mono">BasinZone.apply</span>, the model does not change, and no row is
written. Without that guard, a duplicate or out-of-order observation would appear in the history as
though it had taken effect.</p>"""))

B14.append("""
<h3><span class="n">14.5</span>Reading history back into the interface</h3>
<p>The read path is the reverse, and it uses a future so the interface never blocks.</p>
""")

B14.append(code('''public CompletableFuture<List<DatabaseHistoryEntry>> loadHistory(int limit) {
    if (!available) {
        return CompletableFuture.completedFuture(List.of());   // optional means empty, not error
    }
    CompletableFuture<List<DatabaseHistoryEntry>> future = new CompletableFuture<>();
    enqueue(() -> future.complete(history.loadRecent(limit)));
    return future;
}''', "from BasinWatch, db/DatabaseService.java — a read returns a future; an unavailable database returns an empty list."))

B14.append("""
<p>Two details are worth naming. When the database is unavailable the future is completed
<i>immediately</i> with an empty list, so the caller's callback runs normally and simply shows no
history. And the actual query runs on the database thread, so the future completes on that thread —
which is why the interface's callback must hop back to the event-dispatch thread.</p>
""")

B14.append(screenshot("shot_database_records", "S2", "The Database history tab reading real rows from SQLite",
"The same query seen from the operator's side. The status line reads "
"<span class='mono'>200 recent record(s) · 0 database write(s) pending</span> and the table below it "
"is populated with genuine rows: <span class='mono'>SENSOR</span> entries with their timestamp, "
"zone code and a rendered detail string such as <span class='mono'>4.38 m water</span>. "
"Each visible cell came out of a <span class='mono'>ResultSet</span> via "
"<span class='mono'>OperationalEventRepository.loadRecent</span> and was copied into a "
"<span class='mono'>HistoryTableModel</span> on the event-dispatch thread. The category selector "
"on the left chooses between sensor readings, response records and missions, which is why "
"<span class='mono'>DatabaseHistoryType</span> exists as an enum."))

B14.append("""
<p>Nothing in that table is hard-coded for the screenshot. The rows were written by the running
simulation, stored in <span class="mono">basinwatch.db</span>, read back through JDBC and mapped into
the table model. If the SQLite file is deleted and the application restarted, the same panel reports
that history is unavailable and shows an empty table — the rest of the console keeps working.</p>
""")

B14.append(code('''public List<DatabaseHistoryEntry> loadRecent(int limit) throws SQLException {
    String sql = """
            SELECT occurred_at AS at, event_type AS type, zone_id AS zone, detail AS detail
              FROM operational_events
             ORDER BY occurred_at DESC
             LIMIT ?
            """;
    // ... prepare, bind limit, iterate the result set, map each row
}''', "from BasinWatch, db/OperationalEventRepository.java — the query behind the history table.", lang="sql"))

B14.append("""
<h3><span class="n">14.6</span>Why the database is optional</h3>
<p>The final question about this layer is the most important one: why does the application work
without it?</p>
""")

B14.append(figure("d18_db_failure_isolation", "20", "Database failure isolation",
"How a database failure is contained. The exception is caught on the database worker thread, converted into a status message, and posted to the interface. The sensor pipeline, the model, the files and the interface all continue unaffected.",
"landscape"))

B14.append("""
<p>Four mechanisms together produce that isolation, and each was a decision.</p>

<p><b>Availability is a boolean, checked once.</b> <span class="mono">DatabaseManager.isAvailable</span>
catches the exception and returns false, so the rest of the code tests a value rather than handling a
failure.</p>

<p><b>Every write is a queued lambda.</b> Because the work happens on another thread, an exception
there cannot propagate into the caller's stack.</p>

<p><b>The queue wrapper catches everything.</b> <span class="mono">enqueue</span> catches both
<span class="mono">SQLException</span> and <span class="mono">RuntimeException</span> and routes them
to the status listener.</p>

<p><b>A read on an unavailable database returns an empty list.</b> The interface's code path is
identical in both cases, so no branch is needed at the call site.</p>
""")

B14.append(core("""<p>This is the design pattern worth taking away from Part III, and it generalises
well beyond databases: <b>an optional subsystem should be detectable, isolated, and
silent-on-absence.</b> Detectable through a boolean or a capability query. Isolated by running on its
own thread so failures cannot propagate. Silent-on-absence by returning a sensible empty result
rather than raising an error the caller must anticipate.</p>"""))

B14.append(exam("""<p>If asked "what happens if the database is unavailable?", the complete answer has
four parts: the application still starts, because availability is checked rather than assumed; the
history panel shows an empty list and a status message; all writes become no-ops; and the file layer
is entirely unaffected, so the log, archive, snapshot and reports are still produced. Answering with
only the first part is the usual mistake.</p>"""))

B14.append(summary([
  "The database layer has four responsibilities: connection management, schema creation, service coordination, and per-table SQL.",
  "Four tables hold readings, missions, resource usage and operational events; every one carries a timestamp.",
  "Schema creation is idempotent through <span class='mono'>CREATE TABLE IF NOT EXISTS</span>, so it is safe on every launch.",
  "Fixed DDL statements use <span class='mono'>Statement</span>; everything with values uses <span class='mono'>PreparedStatement</span>.",
  "A reading reaches the database only when the model actually changed, which is why the stale-reading guard matters.",
  "Reads return <span class='mono'>CompletableFuture</span>s so the interface never blocks on a query.",
  "The database is optional because availability is a boolean, writes are queued and isolated on their own thread, and reads on an unavailable database return an empty list.",
  "An optional subsystem should be detectable, isolated and silent on absence.",
]))

B14.append(keyterms([
  "<b>Repository</b> — a class that owns the SQL for one table and maps rows to and from domain objects.",
  "<b>Idempotent</b> — safe to perform more than once with the same result.",
  "<b>DDL</b> — data definition language: statements such as <span class='mono'>CREATE TABLE</span>.",
  "<b>Single-threaded executor</b> — an executor with one worker, serialising all submitted tasks.",
  "<b>Capability query</b> — asking whether an optional subsystem is available rather than assuming it is.",
]))

B14.append("</div>")

HTML = "".join(P + B10 + B11 + B12 + B13 + B14)
