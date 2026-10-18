"""PART I — Understanding the System.  Chapters 1-3."""
from . import *

PART = """
<div class="part-page">
  <div class="pnum">PART I</div>
  <h1>Understanding the System</h1>
  <div class="prule"></div>
  <div class="pintro">Before studying a single API, you need to see the machine as a whole.
  This part introduces BasinWatch, the verified architecture of its runtime, the object
  concepts that hold it together, and the six different ways its components talk to one
  another. Everything later in the book hangs on this frame.</div>
  <div class="chapters">
    <div><span>1</span>The Complete Java System: From Data Input to a Working Application</div>
    <div><span>2</span>Java Application Structure and Core Object Concepts</div>
    <div><span>3</span>How Java Components Communicate</div>
  </div>
</div>
"""

CH1 = (chapter(1, "The Complete Java System: From Data Input to a Working Application",
"One application, many technologies. This chapter builds the mental model that every later chapter refers back to.") + """

<h3><span class="n">1.1</span>The question this book answers</h3>
<p>Here is the question. It is short, and it is the reason this book exists rather than a
stack of separate revision sheets:</p>

<div class="defbox"><span class="tag">THE CENTRAL QUESTION</span>
<p><i>How do separate Java technologies work together to turn incoming data into a usable
application, store information persistently, and display useful results to a user?</i></p></div>

<p>A student who has just finished a semester of Java can usually answer each part of that
question alone. Streams read and write data. JDBC talks to databases. Swing draws windows.
Maven builds projects. Each answer is correct and each is nearly useless on its own,
because in a real program these things are not separate. A button press causes a query; a
query returns rows that become objects; those objects are rendered; the same data is also
written to a log file; a thread produced the data in the first place. The technologies are a
system.</p>

<p>So this chapter does not explain any API in depth. It does something more important: it
shows you the system, names every component in it, and explains why each technology is
present. By the end you should be able to sketch the whole application from memory. Every
later chapter fills in one box of that sketch.</p>

""" + core("""<p>The organising idea of this book is <b>one connected Java application</b>.
Every technology you will study is introduced twice: first on its own terms, then in the
place where the application actually needs it. If you ever lose the thread, come back to
Diagram 1 and find your current topic in it.</p>""") + """

<h3><span class="n">1.2</span>What BasinWatch is trying to accomplish</h3>

<p>BasinWatch is an offline floodplain operations console. A basin is a river catchment
area; when rain falls and water levels rise, some districts flood before others, and a
control room has to decide where to send limited equipment. BasinWatch simulates that
situation on a desktop so a student or planner can practise the decisions without any real
risk.</p>

<p>The operator's job, in the project's own words, is to watch a schematic basin map as rain
and water levels change, review severity-ranked zone alerts, dispatch pumps, levee crews and
evacuation teams to concurrent missions, see what resources remain available, then save the
session, close the application, and restore the model and active operations later.</p>

<div class="grid2">
<div>
<h4 class="plain">What enters the system</h4>
<ul class="tight">
<li>Simulated station observations: rainfall in millimetres and observed water rise in
centimetres, for six named zones.</li>
<li>Simulation pulses marking the passage of a time interval.</li>
<li>Operator commands: start, pause, step, inject a storm cell, dispatch, save, restore,
export a report.</li>
<li>Selection events: which zone the operator is inspecting.</li>
</ul>
</div>
<div>
<h4 class="plain">What leaves the system</h4>
<ul class="tight">
<li>A live map of six zones coloured by risk level.</li>
<li>A ranked activity timeline and a list of active field operations.</li>
<li>A resource board showing available and committed units.</li>
<li>Persistent artefacts: an operational log, a typed binary archive, session saves and
readable reports.</li>
<li>Optional queryable history in a local SQLite database.</li>
</ul>
</div>
</div>

<p>Six zones are monitored. Each has a position on a two-by-three schematic grid, an initial
water level in metres, and a number of exposed residents. Risk is derived from the water
level by fixed thresholds: below 1.7 m is NORMAL, 1.7 m and above is WATCH, 2.6 m and above
is WARNING, and 3.6 m and above is CRITICAL.</p>

""" + practice("""<p>Those thresholds are real code, not invented for the book. They appear in
<span class="mono">BasinZone.assessRisk(double)</span>:</p>
<pre class="long"><span class="kw">static</span> <span class="ty">RiskLevel</span> assessRisk(<span class="kw">double</span> waterLevelMeters) {
    <span class="kw">if</span> (waterLevelMeters &gt;= 3.6) <span class="kw">return</span> <span class="ty">RiskLevel</span>.CRITICAL;
    <span class="kw">if</span> (waterLevelMeters &gt;= 2.6) <span class="kw">return</span> <span class="ty">RiskLevel</span>.WARNING;
    <span class="kw">if</span> (waterLevelMeters &gt;= 1.7) <span class="kw">return</span> <span class="ty">RiskLevel</span>.WATCH;
    <span class="kw">return</span> <span class="ty">RiskLevel</span>.NORMAL;
}</pre>
<div class="codecap"><b>Listing 1.1</b> — from BasinWatch, <span class="mono">domain/BasinZone.java</span></div>""") + """

<h3><span class="n">1.3</span>The verified runtime architecture</h3>

<p>The single most useful thing you can learn about a program is which component owns which
responsibility and which thread runs which code. BasinWatch's architecture is documented in
its own <span class="mono">ARCHITECTURE.md</span>, and — importantly — the documentation
matches the code. Here is the verified picture.</p>

""" + visual("""<p>Read Diagram 1 from top to bottom. Follow the arrow from the operator
into the Swing interface, down through the application commands into the engine, then along
the green sensor path from left to right, and finally down into the two persistence columns.
Every box is a real class; every arrow is a real call, stream write or thread hand-off.</p>""") +

figure("d01_architecture_overview", "1", "The complete BasinWatch system",
"Six layers: the operator, the Swing interface on the event-dispatch thread, the engine's command API, the domain and engine layer, the sensor input path with its piped streams, and the two independent persistence columns for files and JDBC.",
"portrait") + """

<h4 class="plain">What that architecture actually looks like on screen</h4>

<p>Every diagram in this book describes code that runs. Before going any further, look at
what the operator actually sees. The window below is the real BasinWatch application,
launched from the shaded JAR built by Maven, with a simulation in progress: observations
streaming, zones escalating to <span class="mono">CRITICAL</span>, and a field response
dispatched against Marsh End.</p>

""" + screenshot("shot_response_tab", "S1", "The running BasinWatch application, Response tab",
"Captured from the real application (<span class='mono'>java -jar target/basinwatch-1.0.0.jar</span>). "
"The header carries the brand, the title bar of controls (<i>Pause observations</i>, "
"<i>Advance one interval</i>, <i>Inject storm cell</i>, <i>Save session</i>, <i>Restore session</i>, "
"<i>Export situation report</i>) and the risk summary reading "
"<span class='mono'>6 ZONES · 5 CRITICAL · 1 WARNING · 0 WATCH</span>. The basin map below shows "
"one card per zone with its live water level, rainfall and exposed population. The five tabs along "
"the top of the panel — Response, Operations, Insights, Learn and Database history — are the "
"subjects of Chapters 15 to 16, and each one is a real <span class='mono'>JPanel</span> added to a "
"<span class='mono'>JTabbedPane</span>.") + """

<p>Two details in that screenshot are worth noticing now, because the whole book returns to
them. First, the risk summary is not painted by the engine: the engine publishes an immutable
<span class="mono">BasinSnapshot</span>, and a Swing listener copies numbers out of it. Second,
the button labelled <i>Pause observations</i> means the feed is currently running — the label
is derived from the engine's state, so the interface and the model cannot disagree.</p>
""" + visual("""<p>Read Diagram 1 from top to bottom. Follow the arrow from the operator
into the Swing interface, down through the application commands into the engine, then along
the green sensor path from left to right, and finally down into the two persistence columns.
Every box is a real class; every arrow is a real call, stream write or thread hand-off.</p>""") + """

<h4 class="plain">The six layers, in the order data meets them</h4>
<ol>
<li><b>The operator and the interface.</b> <span class="mono">BasinWatchApp.main</span> sets
the system look and feel and then hands control to the event-dispatch thread with
<span class="mono">SwingUtilities.invokeLater</span>. From that moment the
<span class="mono">MainFrame</span> owns the window, and only the event-dispatch thread may
touch Swing components.</li>
<li><b>Application commands.</b> The interface never manipulates the model directly. It
calls a narrow set of methods on <span class="mono">BasinEngine</span>:
<span class="mono">start()</span>, <span class="mono">pause()</span>,
<span class="mono">step()</span>, <span class="mono">dispatch(...)</span>,
<span class="mono">injectStorm(...)</span>, <span class="mono">save(...)</span>,
<span class="mono">load(...)</span>, <span class="mono">exportReport()</span>. Most return a
<span class="mono">CompletableFuture</span>, so the interface can ask for work and keep
painting.</li>
<li><b>The domain and engine layer.</b> <span class="mono">BasinModel</span> is the aggregate
root: it owns the six zones, the mission registry, the recent-activity ring buffer and the
resource allocator. It enforces invariants and produces immutable snapshots. Three
<span class="mono">ResponseWorker</span> tasks consume events and apply them.</li>
<li><b>The sensor input path.</b> A dedicated <span class="mono">SensorFeed</span> thread
encodes observations as text lines and writes them into a
<span class="mono">PipedWriter</span>. A separate <span class="mono">SensorIntake</span> task
reads them through a <span class="mono">BufferedReader</span> over a
<span class="mono">PipedReader</span>, validates each record, and places accepted events into
a bounded <span class="mono">EventBuffer</span>.</li>
<li><b>File persistence.</b> Four independent file responsibilities: a UTF-8 append-only
operational log, a typed binary sensor archive, versioned session snapshots written through
an atomic replace, and human-readable reports.</li>
<li><b>The JDBC layer.</b> An optional, single-threaded
<span class="mono">DatabaseService</span> that writes accepted readings, mission lifecycles,
resource allocations and operational events into a local SQLite file through parameterized
SQL, and reads recent history back for the interface.</li>
</ol>

""" + connect("""<p>Notice that the file column and the database column both hang off the
<i>same</i> point — accepted events — but they are not alternatives. Chapter 9 shows what
each file is for; Chapter 14 shows what the database adds; Chapter 10 explains why an
application would deliberately choose to have both.</p>""") + """

<h3><span class="n">1.4</span>The seven questions the architecture must answer</h3>

<p>An architecture is only useful if it answers concrete questions. These are the seven that
matter for this application, with the verified answers.</p>

<h4 class="plain">Which component processes incoming data?</h4>
<p>Observations arrive as text lines from the pipe. <span class="mono">SensorIntake</span>
parses each line with <span class="mono">SensorReading.parse</span>, which validates the
field count, the record type marker and every numeric range. A malformed record is reported
and discarded — it does not stop the intake loop. Accepted events go into the bounded
<span class="mono">EventBuffer</span>, and one of the three response workers takes them from
there.</p>

<h4 class="plain">Where is Java I/O needed, and why?</h4>
<p>In four genuinely different places, for four genuinely different reasons. The pipe
carries observations between threads. The journal and reports give humans a readable audit
trail. The archive keeps typed numeric measurements for later diagnosis. The snapshot store
captures the whole session so it can be restored. Chapter 9 treats this as a design question
rather than a list.</p>

<h4 class="plain">Why does JDBC exist in this application?</h4>
<p>Because a file answers a different question than a database. A log file is a sequence of
lines; asking "show me the 200 most recent readings for zone MIL, newest first" means reading
and filtering the whole file. A database answers that with an index and a
<span class="mono">LIMIT</span>. BasinWatch therefore keeps both, and the database is
optional precisely because it is an addition rather than a requirement.</p>

<h4 class="plain">What does the Swing interface do?</h4>
<p>Three things: it renders immutable snapshots, it collects operator intent, and it reports
outcomes. It does no domain logic and no persistence. That separation is what makes the rest
of the application testable without a window.</p>

<h4 class="plain">Which work happens on background threads?</h4>
<p>Observation production (<span class="mono">SensorFeed</span>), intake
(<span class="mono">basin-sensor-intake</span>), response processing (three
<span class="mono">basin-response-N</span> threads), archiving
(<span class="mono">basin-sensor-archive</span>), control commands
(<span class="mono">basin-control</span>) and database writes
(<span class="mono">basin-database</span>). Only rendering and event handling happen on the
event-dispatch thread.</p>

<h4 class="plain">How does data survive the application closing?</h4>
<p>Five ways, listed in Table 1.1. On a clean shutdown the engine also writes an automatic
<span class="mono">last-session.bws</span> snapshot, so the next launch can restore the
basin.</p>

""" + table(
  ["Artefact", "Written by", "Contains", "Restored on next launch?"],
  [
    ["<span class='mono'>data/logs/operations.log</span>", "OperationalJournal",
     "Timestamped operational events as UTF-8 text", "No — it is an audit trail"],
    ["<span class='mono'>data/archive/sensors.bin</span>", "SensorArchive (via ArchiveWorker)",
     "Typed tick, station, zone, rainfall, rise", "No — it is a measurement record"],
    ["<span class='mono'>data/saves/*.bws</span>", "SnapshotStore",
     "Versioned session snapshot: tick, zones, stock, missions, activity",
     "<b>Yes</b> — on request, or automatically for <span class='mono'>last-session.bws</span>"],
    ["<span class='mono'>data/reports/*.txt</span>", "ReportWriter",
     "A human-readable situation report", "No — it is a document"],
    ["<span class='mono'>data/basinwatch.db</span>", "DatabaseService + repositories",
     "Sensor readings, missions, resource usage, events in four tables",
     "Read back as history, not as live state"],
  ],
  caption="<b>Table 1.1</b> — The five persistence artefacts and what each one is for.") + """

<h4 class="plain">Where do the technologies interact, and where do they stay separate?</h4>
<p>They interact at exactly two boundaries. The first is the <i>accepted event</i>: after the
model has processed an event, the engine writes to the log, submits to the archive worker,
and enqueues a database operation. The second is the <i>published snapshot</i>: the engine
hands an immutable value to the interface, the only channel by which background work becomes
visible. Everywhere else the layers are deliberately ignorant of one another: the model does
not know about files, the repositories do not know about Swing, and the interface does not
know about SQL.</p>

""" + distinct("""<p>The engine publishes <b>immutable snapshots</b>, not live objects. A
<span class="mono">BasinSnapshot</span> is a record whose constructor copies every list and
map with <span class="mono">List.copyOf</span> and <span class="mono">Map.copyOf</span>. That
single decision is why the interface can render data on the event-dispatch thread while
workers continue to mutate the model — the snapshot cannot change underneath it.</p>""") + """

<h3><span class="n">1.5</span>The Java Concepts Connection Map</h3>

<p>Every syllabus topic in this book has a home. Diagram 2 places them all at once, grouped
into four columns. Use it as a map rather than a summary: when a later chapter introduces a
concept, you should be able to point at the column it belongs to.</p>

""" + figure("d02_concept_map", "2", "The Java Concepts Connection Map",
"Language foundations, Java I/O, concurrency, and the combined data/UI/build column. Each entry names a real class or file in the project.",
"portrait") + """

<p>Read the map in four movements:</p>
<ul>
<li><b>Language foundations</b> (Chapter 2) explain the object concepts that make the rest
possible: classes and objects, interfaces as contracts, polymorphism, justified inheritance,
enums for bounded vocabularies, records for immutable values, encapsulation, and the
POJO-versus-JavaBean distinction.</li>
<li><b>Java I/O</b> (Chapters 4 to 9) covers byte and character streams, buffering, data
streams, byte-array streams, piped streams, serialization and file metadata.</li>
<li><b>Concurrency</b> (Chapters 3 and 7, then used everywhere) covers threads, runnables,
monitors, condition waiting, the producer–consumer pattern, interruption and joining, and
deadlock avoidance.</li>
<li><b>Data, UI and build</b> (Chapters 10 to 19) covers JDBC from driver to transaction,
Swing from frame to repaint, and the configuration and packaging that make the application
run at all.</li>
</ul>

<h3><span class="n">1.6</span>What is genuinely difficult here</h3>

<p>It is worth being honest about which parts of this application are hard, because those are
the parts worth understanding deeply rather than memorising.</p>

<p><b>Concurrency is hard because correctness is invisible.</b> If two dispatches both read
the same resource count as available, the bug appears only under load and only sometimes.
BasinWatch's answer is a single short synchronized reservation that checks every required
resource before decrementing any of them — an all-or-nothing operation. There is no way to
observe the intermediate state, because there is no intermediate state.</p>

<p><b>Shutdown is hard because it is where resources leak.</b> Stopping a feed thread,
closing a pipe, waking waiting consumers, draining an archive queue, flushing a journal and
writing a final snapshot must happen in the right order. The engine's
<span class="mono">closeEngine()</span> does exactly this, and reports a timeout rather than
pretending success.</p>

<p><b>Persistence is hard because the easy version is unsafe.</b> Writing a file with
<span class="mono">ObjectOutputStream</span> is two lines; making it safe means bounding the
input size, filtering the classes that may be constructed, checking a format version, and
validating the restored domain state. Chapter 8 walks through all four.</p>

""" + mistake("""<p>The most common architectural mistake in student projects is letting the
interface do the work. A button handler that opens a database connection, queries, and updates
a label feels natural because it is one function in one file. It also freezes the window for
the duration of the query, makes the logic untestable without a screen, and spreads SQL across
the codebase. BasinWatch's rule — the interface asks, the engine decides, a worker executes, a
snapshot reports — is the fix.</p>""") + """

<h3><span class="n">1.7</span>How the rest of the book is organised</h3>

""" + table(
  ["Part", "Chapters", "What you will be able to do afterwards"],
  [
    ["<b>I — Understanding the System</b>", "1–3",
     "Sketch the architecture, explain the object concepts, and distinguish six forms of component communication."],
    ["<b>II — Java I/O and Persistent Files</b>", "4–9",
     "Choose and layer the right stream for a task, manage resources safely, and explain four different persistence mechanisms."],
    ["<b>III — Databases and JDBC</b>", "10–14",
     "Open a connection, execute parameterized SQL, map result sets, use transactions, and explain why a database is optional here."],
    ["<b>IV — Swing and the User Interface</b>", "15–16",
     "Build a component tree, handle events, keep the event-dispatch thread free, and show database results safely."],
    ["<b>V — Configuration and Related Techniques</b>", "17–19",
     "Explain how dependencies reach the classpath, what XML and annotations are for, and how JdbcTemplate abstracts raw JDBC."],
    ["<b>VI — Putting Everything Together</b>", "20–21",
     "Trace four real scenarios end to end and answer the eight integration questions."],
    ["<b>Revision</b>", "R, V, E, G",
     "Revise with comparison tables, answer viva questions, and work through tracing exercises."],
  ],
  caption="<b>Table 1.2</b> — The book's structure and what each part delivers.") +

exam("""<p>If you are asked "describe your project architecture" in a viva, do not start with
the code. Start with the data. Say what enters the system, which component validates it, where
it is processed, what is persisted, and how the result reaches the screen. Then name the
classes. Examiners reward the flow; the class names follow naturally.</p>""") +

summary([
  "BasinWatch is an offline floodplain operations console: a single-process Swing desktop application with no server, no network and no external service.",
  "Six layers: operator and interface, application commands, domain and engine, sensor input path, file persistence, and the optional JDBC layer.",
  "The event-dispatch thread owns all Swing components; five other threads do background work and publish immutable snapshots back to it.",
  "Java I/O appears in four distinct roles: a pipe between threads, a readable log, a typed binary archive, and a session snapshot.",
  "JDBC exists because selective queries over indexed rows are a different job from reading a text file; the database is an addition, not a replacement.",
  "Data survives shutdown in five artefacts, of which only the session snapshot restores live state.",
  "Technologies meet at exactly two boundaries: the accepted event and the published snapshot.",
]) + keyterms([
  "<b>Aggregate root</b> — the single object that owns a group of related state and enforces its invariants. Here, <span class='mono'>BasinModel</span>.",
  "<b>Immutable snapshot</b> — a value object copied out of the model so another thread can read it safely.",
  "<b>Event-dispatch thread (EDT)</b> — the single Swing thread that runs event handling and painting.",
  "<b>Bounded buffer</b> — a queue with a maximum size that makes producers wait when it is full.",
  "<b>Optional subsystem</b> — a component whose failure does not stop the application. Here, the SQLite history.",
]) + "</div>")


CH2 = (chapter(2, "Java Application Structure and Core Object Concepts",
"Objects, interfaces, inheritance, enums, records and validation — the vocabulary the rest of the book assumes.") + """

<h3><span class="n">2.1</span>Why start with objects?</h3>
<p>Every later chapter is about a mechanism — a stream, a query, a listener. Each mechanism
operates on objects, and each is designed around an object concept. If a method takes an
interface, the interface's design determines what the method can do. If a class is a record,
it cannot be mutated. So the object model has to come first.</p>

<p>This chapter is not an introduction to writing classes. It is a tour of the specific
object decisions BasinWatch makes, with the reason for each, plus the POJO-versus-JavaBean
distinction that appears in the syllabus and matters the moment you meet a framework.</p>

<h3><span class="n">2.2</span>Classes, objects, state and behaviour</h3>
<p>A class is a template; an object is an instance of it. An object has state (its fields)
and behaviour (its methods), and good design keeps state private so behaviour is the only
route in.</p>

""" + defbox("Encapsulation",
"keeping fields private and exposing only the operations that make sense, so an object can never be placed in an invalid state from outside.") + """

<p>BasinWatch applies this at several levels. <span class="mono">BasinZone</span> is
package-private: only classes in <span class="mono">com.basinwatch.domain</span> may even
refer to it. Its fields are private, and it exposes a small set of package-private methods —
<span class="mono">apply</span>, <span class="mono">pump</span>,
<span class="mono">reinforceLevee</span>, <span class="mono">evacuate</span> — plus
<span class="mono">snapshot()</span>, which returns an immutable copy.</p>

""" + code('''final class BasinZone {
    private final String id;
    private final String name;
    private double waterLevelMeters;
    private double lastRainMillimeters;
    private int exposedResidents;
    private boolean leveeReinforced;
    private long lastReadingTick = -1;
    private RiskLevel risk;

    boolean apply(SensorReading reading) {
        if (reading.tick() <= lastReadingTick) {
            return false;                     // a stale reading is rejected, not applied
        }
        lastReadingTick = reading.tick();
        lastRainMillimeters = reading.rainfallMillimeters();
        double runoffFactor = leveeReinforced ? 0.58 : 1.0;
        double rainfallContribution = reading.rainfallMillimeters() * 0.0014;
        double observedRise = reading.observedRiseCentimeters() / 100.0;
        waterLevelMeters = Math.min(8.0,
                Math.max(0.0, waterLevelMeters + (rainfallContribution + observedRise) * runoffFactor));
        risk = assessRisk(waterLevelMeters);
        return true;
    }
    // pump, reinforceLevee, evacuate, snapshot, restore, assessRisk ...
}''',
"from BasinWatch, domain/BasinZone.java — state is private; behaviour is the only route in.") + """

<p>Three things in that listing deserve attention. First, the stale-reading guard: if the
incoming tick is not newer than the last one applied, the reading is ignored and the method
returns <span class="mono">false</span>. That is an invariant, not a nicety — without it, an
out-of-order observation could reduce a water level. Second, the reinforced levee multiplies
runoff by 0.58, which is a real domain consequence of an earlier operator decision. Third,
the water level is clamped to the range 0 to 8 metres on every update, so the field can never
hold a physically impossible value.</p>

""" + connect("""<p>That guard is why Chapter 20's trace can say "the observation was
accepted" and mean something specific. A reading is accepted only if it is newer than the
last one for that zone <i>and</i> the model changed as a result. The engine uses exactly that
test when deciding whether to write the reading to the database.</p>""") + """

<h3><span class="n">2.3</span>Interfaces as contracts</h3>
<p>An interface declares what a type can do without saying how. In BasinWatch, the whole
event system is built on one interface with four methods.</p>

""" + code('''public interface BasinEvent {
    long tick();
    String zoneId();
    String category();
    String describe();
}''', "from BasinWatch, domain/BasinEvent.java") + """

<p>Three records implement it: <span class="mono">SensorReading</span>,
<span class="mono">SimulationPulse</span> and <span class="mono">DispatchRequest</span>. They
are radically different in content — a measurement, a time marker, an operator command — yet
they all satisfy the same contract, so a single queue and a single
<span class="mono">process</span> method can handle all of them.</p>

<h3><span class="n">2.4</span>Polymorphism: one call, several behaviours</h3>
<p>Polymorphism means the same call site behaves according to the actual type of the object.
<span class="mono">BasinModel.process</span> is the clearest example in the project.</p>

""" + code('''public synchronized List<String> process(BasinEvent event) {
    if (event == null) {
        throw new IllegalArgumentException("Event is required.");
    }
    ArrayList<String> messages = new ArrayList<>();
    if (event instanceof SensorReading reading) {
        applyReading(reading, messages);
    } else if (event instanceof SimulationPulse pulse) {
        applyPulse(pulse, messages);
    } else if (event instanceof DispatchRequest request) {
        applyDispatch(request, messages);
    } else {
        throw new IllegalArgumentException("Unsupported basin event: " + event.getClass().getName());
    }
    return List.copyOf(messages);
}''', "from BasinWatch, domain/BasinModel.java — pattern matching on the event type.") + """

<p>This is polymorphism expressed with pattern matching rather than with a method override.
Both are valid; the choice here is deliberate. The model wants <i>one</i> place where the
complete set of event types is visible, so that adding a fourth event type produces a
compile-time-visible gap rather than a silently ignored class. The
<span class="mono">else</span> branch throws, so an unknown event type is a loud failure
rather than a silent no-op.</p>

""" + distinct("""<p><b>Interface polymorphism</b> (what the queue relies on) and
<b>dispatch polymorphism</b> (what the model performs) are different things. The interface
lets the buffer store any event without knowing its type. The
<span class="mono">instanceof</span> chain is how the model decides which behaviour to run.
You need both: the first for type safety, the second for behaviour selection.</p>""") + """

<h3><span class="n">2.5</span>Inheritance: used narrowly and for a reason</h3>
<p>Inheritance is the most over-used feature in student Java. BasinWatch uses it exactly
twice, and both times because the superclass is a real framework contract rather than a
convenience.</p>

<ul>
<li><span class="mono">SensorFeed extends Thread</span>. A feed has a genuine lifecycle to
own: it must be started, it has a long-running loop, it holds a blocking pipe endpoint, and
it must be interruptible and joinable. Extending <span class="mono">Thread</span> lets it
carry a name (<span class="mono">"basin-sensor-feed"</span>), a priority, and a state that
diagnostics can report.</li>
<li><span class="mono">MainFrame extends JFrame</span>, <span class="mono">BasinMapPanel
extends JPanel</span>, <span class="mono">DatabaseHistoryPanel extends JPanel</span>. Swing
is an inheritance-based framework: to be a component you must be a component. Overriding
<span class="mono">paintComponent</span> is how custom drawing is done.</li>
</ul>

<p>Everywhere else, composition is preferred. <span class="mono">BasinEngine</span> does not
extend anything; it <i>has</i> an <span class="mono">EventBuffer</span>, a
<span class="mono">DatabaseService</span>, a list of listener lists and an
<span class="mono">ExecutorService</span>.</p>

""" + code('''public final class SensorFeed extends Thread {
    public SensorFeed(Writer destination, List<String> zoneIds, SimulationSettings settings,
                      AtomicLong tickSequence, Consumer<String> failureReporter) {
        super("basin-sensor-feed");           // a named thread is a diagnosable thread
        this.destination = destination;
        this.zoneIds = List.copyOf(zoneIds);
        this.settings = settings;
        this.tickSequence = tickSequence;
        this.failureReporter = failureReporter;
        setPriority(Thread.NORM_PRIORITY);
    }
    @Override
    public void run() { /* the timed emission loop */ }
    public void requestStop() throws IOException { /* cooperative shutdown */ }
}''', "from BasinWatch, engine/SensorFeed.java — the one justified Thread subclass.") +

distinct("""<p>Compare with <span class="mono">SensorIntake</span>, which
<span class="mono">implements Runnable</span> instead. Why the difference? Because intake is
a <i>task</i> — a unit of work — not a lifecycle owner. The engine creates a plain
<span class="mono">Thread</span>, names it <span class="mono">"basin-sensor-intake"</span>,
and hands it the task. This is the "prefer <span class="mono">Runnable</span> unless you must
own the thread" rule, applied literally.</p>""") + """

<h3><span class="n">2.6</span>Enums: a fixed vocabulary, typed</h3>
<p>When a value comes from a small closed set, an enum beats a
<span class="mono">String</span> or an <span class="mono">int</span>, because the compiler
then knows every legal value. BasinWatch has four domain enums, and each carries data with
it.</p>

""" + code('''public enum RiskLevel {
    NORMAL("Routine", 0), WATCH("Watch", 1), WARNING("Warning", 2), CRITICAL("Critical", 3);

    private final String label;
    private final int rank;
    RiskLevel(String label, int rank) { this.label = label; this.rank = rank; }
    public String label() { return label; }
    public int rank() { return rank; }
}''', "from BasinWatch, domain/RiskLevel.java — each constant carries a label and a rank.") + """

<p>The <span class="mono">rank()</span> method is what makes risk escalation detectable:
<span class="mono">applyReading</span> compares
<span class="mono">currentRisk.rank() &gt; previousRisk.rank()</span> and prefixes the
activity message with "Risk increased:" when it is true. That comparison is a domain rule
expressed as ordinary code, and it is why the database can be told
<span class="mono">riskEscalated</span> as a boolean rather than being asked to work it
out.</p>

<p><span class="mono">MissionType</span> goes further and carries the whole definition of a
mission:</p>

""" + code('''public enum MissionType {
    PUMP_DEPLOYMENT("Deploy portable pump", 8, 0.62,
            Map.of(ResourceType.PUMP, 1, ResourceType.FIELD_CREW, 1)),
    LEVEE_REINFORCEMENT("Reinforce levee", 10, 0.0,
            Map.of(ResourceType.LEVEE_CREW, 1, ResourceType.SUPPLY_TRUCK, 1)),
    EVACUATION("Evacuate exposed residents", 6, 0.0,
            Map.of(ResourceType.EVAC_VEHICLE, 1, ResourceType.FIELD_CREW, 1));

    private final String label;
    private final int durationTicks;
    private final double waterEffectMeters;
    private final Map<ResourceType, Integer> requirements;
    // constructor, accessors, toString ...
}''', "from BasinWatch, domain/MissionType.java — duration, effect and resource cost live with the type.") +

core("""<p>Putting a mission's duration, its effect on water level, and the resources it
requires inside the enum constant means there is exactly one place to look when a mission type
changes. The allocator, the scheduler and the database all read the same definition. This is
the single most useful habit in the whole chapter: <b>make the data live where the knowledge
lives</b>.</p>""") + """

<h3><span class="n">2.7</span>Records: immutable values with no boilerplate</h3>
<p>A record declares immutable data in one line. The compiler generates a canonical
constructor, accessors named after the components, and correct <span class="mono">equals</span>,
<span class="mono">hashCode</span> and <span class="mono">toString</span>.</p>

""" + code('''public record SensorReading(
        long tick, String stationId, String zoneId,
        double rainfallMillimeters, double observedRiseCentimeters) implements BasinEvent {

    public SensorReading {                       // compact constructor: validation
        if (tick < 0 || !validIdentifier(stationId) || !validIdentifier(zoneId)
                || !Double.isFinite(rainfallMillimeters) || rainfallMillimeters < 0
                || rainfallMillimeters > 500
                || !Double.isFinite(observedRiseCentimeters) || observedRiseCentimeters < 0
                || observedRiseCentimeters > 200) {
            throw new IllegalArgumentException("Invalid sensor reading.");
        }
    }

    @Override public String category() { return "OBSERVATION"; }

    public String encode() {
        return String.format(Locale.ROOT, "READ|%d|%s|%s|%.3f|%.3f",
                tick, stationId, zoneId, rainfallMillimeters, observedRiseCentimeters);
    }

    public static SensorReading parse(String line) {
        String[] fields = line.split("\\\\|", -1);
        if (fields.length != 6 || !"READ".equals(fields[0])) {
            throw new IllegalArgumentException("Malformed sensor observation.");
        }
        try {
            return new SensorReading(Long.parseLong(fields[1]), fields[2], fields[3],
                    Double.parseDouble(fields[4]), Double.parseDouble(fields[5]));
        } catch (NumberFormatException ex) {
            throw new IllegalArgumentException("Sensor reading contains an invalid number.", ex);
        }
    }
}''', "from BasinWatch, domain/SensorReading.java — a record that validates on construction.") + """

<p>Three patterns in that listing are worth naming, because they recur throughout the book.</p>

<p><b>The compact constructor validates.</b> A record's canonical constructor can be written
without repeating the parameter list, and any exception thrown there prevents the object from
existing. This is why <span class="mono">parse</span> can be trusted: if it returns a
<span class="mono">SensorReading</span>, the ranges are already correct. Validation happens at
the boundary, once, instead of being re-checked by every consumer.</p>

<p><b>encode and parse are a matched pair.</b> <span class="mono">encode()</span> produces a
pipe-delimited line; <span class="mono">parse()</span> is its inverse and rejects anything
that is not exactly six fields beginning with <span class="mono">READ</span>. Keeping them
next to each other in the same class is what makes the wire format maintainable. Chapter 7
follows that format through the pipe.</p>

<p><b>Immutability makes the object safe to share.</b> A
<span class="mono">SensorReading</span> can be handed from the feed thread to the intake
thread to a worker thread with no synchronization at all, because no thread can change it.</p>

""" + connect("""<p>Records and serialization meet in Chapter 8. A record is an excellent
in-memory value, but records are serializable only if every component type is serializable and
the record has no non-serializable superclass. BasinWatch's snapshot DTOs are therefore plain
final classes with a no-argument constructor rather than records — a deliberate choice
explained in that chapter.</p>""") + """

<h3><span class="n">2.8</span>POJO versus JavaBean</h3>

""" + defbox("POJO",
"a Plain Old Java Object — any ordinary class with fields and methods, subject to no framework convention at all.") +

defbox("JavaBean",
"a POJO that follows a convention: a public no-argument constructor, private fields, and public getX/setX accessors, usually implementing Serializable, so that a framework can create and populate it by reflection.") +

figure("d24_pojo_vs_bean", "3", "POJO versus JavaBean, side by side",
"Left: BasinWatch's SensorReading record — a POJO with no convention. Right: the same data as a JavaBean with a no-argument constructor and accessors.",
"landscape") + """

<p>The distinction matters practically. A record cannot be a JavaBean: it has no no-argument
constructor and no <span class="mono">setX</span> methods, so a framework that expects to
instantiate a bean and then call setters cannot use it. Conversely, nothing requires a
JavaBean to be mutable in practice — it only has to <i>look</i> that way to the framework.</p>

<p>BasinWatch contains three shapes, and each is deliberate:</p>

""" + table(
  ["Shape", "Example", "Why that shape"],
  [
    ["Record (immutable POJO)",
     "<span class='mono'>SensorReading</span>, <span class='mono'>ZoneSnapshot</span>, <span class='mono'>DatabaseHistoryEntry</span>",
     "Values that cross a boundary must not change while in flight; the compiler generates accessors and equality."],
    ["Plain final class with mutable fields",
     "<span class='mono'>SavedZone</span>, <span class='mono'>SavedMission</span>, <span class='mono'>SessionSnapshot</span>",
     "Serialization restores fields directly, so accessors are unnecessary. A no-argument constructor is required by the serialization mechanism."],
    ["Framework-style JavaBean", "None in BasinWatch",
     "No framework in this project needs to instantiate objects by name. Chapter 19 shows where a JavaBean would be required."],
  ],
  caption="<b>Table 2.1</b> — The three object shapes and why BasinWatch uses each.") +

related("""<p>If BasinWatch used Spring's component scanning, its services would become
JavaBeans or annotated components: a no-argument constructor plus
<span class='mono'>@Autowired</span> setters, or a constructor annotated for injection. It does
not. Instead, wiring is explicit and visible: <span class='mono'>BasinEngine</span> constructs
the <span class='mono'>DatabaseService</span>, which constructs the
<span class='mono'>DatabaseManager</span> and passes it to each repository constructor. That is
constructor injection performed by hand. Diagram 27 contrasts the two.</p>""") + """

<h3><span class="n">2.9</span>Access modifiers as a design tool</h3>
<p>Modifiers are not decoration; they are how a design is enforced. BasinWatch's choices are
systematic.</p>

""" + table(
  ["Modifier", "Where it is used", "What it prevents"],
  [
    ["<span class='mono'>public</span>",
     "Engine commands, domain value types, repository methods called from the service",
     "Nothing — but the set is deliberately small and stable."],
    ["<span class='mono'>package-private</span>",
     "<span class='mono'>BasinZone</span>, <span class='mono'>ResponseMission</span>, <span class='mono'>SavedZone</span>, the connection-taking overloads in repositories",
     "Any code outside the package reaching into the aggregate's internals. Only <span class='mono'>BasinModel</span> can mutate a zone."],
    ["<span class='mono'>private</span>", "Fields, helper methods, the schema array, the filter function",
     "Everything except the class's own methods."],
    ["<span class='mono'>final</span> (class)",
     "<span class='mono'>BasinModel</span>, <span class='mono'>BasinEngine</span>, <span class='mono'>SnapshotStore</span>, <span class='mono'>OperationalJournal</span>",
     "Subclassing a class that was not designed for it."],
    ["<span class='mono'>static final</span> (constants)",
     "<span class='mono'>MAGIC</span>, <span class='mono'>FORMAT_VERSION</span>, <span class='mono'>MAX_SAVE_BYTES</span>, <span class='mono'>WORKER_COUNT</span>",
     "Magic numbers scattered through the code, and accidental modification."],
  ],
  caption="<b>Table 2.2</b> — Access modifiers, their use in the project, and what they enforce.") +

practice("""<p>The connection-taking overloads are a particularly neat example. Each
repository has a public method that opens its own connection and a package-private method that
accepts an existing one:</p>
<pre class="long"><span class="kw">public</span> <span class="kw">void</span> insert(<span class="ty">SensorReading</span> reading, <span class="ty">ZoneSnapshot</span> zone, <span class="ty">Instant</span> timestamp)
        <span class="kw">throws</span> <span class="ty">SQLException</span> {
    <span class="kw">try</span> (<span class="ty">Connection</span> connection = database.openConnection()) {
        insert(connection, reading, zone, timestamp);      <span class="cm">// the package-private overload</span>
    }
}

<span class="kw">void</span> insert(<span class="ty">Connection</span> connection, <span class="ty">SensorReading</span> reading, <span class="ty">ZoneSnapshot</span> zone,
            <span class="ty">Instant</span> timestamp) <span class="kw">throws</span> <span class="ty">SQLException</span> { /* binds and executes */ }</pre>
<div class="codecap"><b>Listing 2.2</b> — from BasinWatch, <span class="mono">db/SensorReadingRepository.java</span></div>
<p>The public overload is for ordinary use. The package-private overload exists so that
<span class="mono">MissionRepository</span> can enlist several writes in <i>one</i> transaction
on <i>one</i> connection — the subject of Chapter 13. Visibility encodes the rule: only a
class in the same package may participate in someone else's transaction.</p>""") + """

<h3><span class="n">2.10</span>How BasinWatch divides responsibility</h3>
<p>Six packages, six responsibilities. This division is the reason later chapters can be
organised by technology without becoming a pile of unrelated facts.</p>

""" + table(
  ["Package", "Responsibility", "Knows about", "Must not know about"],
  [
    ["<span class='mono'>app</span>", "The Swing window, panels, listeners and entry point",
     "engine commands, snapshots", "SQL, streams, files"],
    ["<span class='mono'>domain</span>", "Zones, events, missions, resources, invariants",
     "nothing outside itself", "files, SQL, Swing, threads"],
    ["<span class='mono'>engine</span>", "Lifecycle, threading, queues, coordination",
     "domain, io, db", "Swing components"],
    ["<span class='mono'>io</span>", "File paths, streams, snapshots, reports",
     "domain values", "SQL, Swing"],
    ["<span class='mono'>db</span>", "Connections, schema, repositories, transactions",
     "domain values", "Swing, files"],
    ["<span class='mono'>learning</span>", "Optional in-application architecture cards",
     "nothing", "everything else"],
  ],
  caption="<b>Table 2.3</b> — Package responsibilities and the boundaries between them.") +

exam("""<p>A reliable viva answer to "how is your project structured?" is: <i>"by
responsibility, and dependencies point one way — the interface depends on the engine, the
engine depends on the domain, file and database layers, and none of those depend back on the
interface."</i> Then give one concrete example: the model has no import of
<span class='mono'>javax.swing</span>, which is why it can be tested without a window.</p>""") +

summary([
  "Encapsulation is enforced by modifiers: <span class='mono'>BasinZone</span> is package-private and its fields are private, so only the aggregate can change zone state.",
  "One interface, <span class='mono'>BasinEvent</span>, unifies three unrelated event records so a single queue and a single process method can handle them.",
  "Polymorphism appears as pattern matching in <span class='mono'>BasinModel.process</span>, with an explicit failure branch for unknown types.",
  "Inheritance is used twice and only where a framework contract requires it: <span class='mono'>Thread</span> for the feed, Swing components for the UI.",
  "Enums carry their own data — labels, ranks, durations, water effects and resource requirements.",
  "Records provide validated immutable values; the compact constructor is the validation point.",
  "A POJO has no convention; a JavaBean adds a no-argument constructor, accessors and often Serializable. Every bean is a POJO, not vice versa.",
]) + keyterms([
  "<b>Aggregate</b> — a cluster of objects treated as one unit for change; <span class='mono'>BasinModel</span> with its zones and missions.",
  "<b>Compact constructor</b> — a record constructor written without the parameter list, used here purely for validation.",
  "<b>Pattern matching</b> — testing and binding an object's type in one expression, as in <span class='mono'>event instanceof SensorReading reading</span>.",
  "<b>Stale guard</b> — a check that rejects input older than the state already applied.",
  "<b>Constructor injection</b> — supplying an object's dependencies as constructor arguments, here done by hand rather than by a framework.",
]) + "</div>")

CH3 = (chapter(3, "How Java Components Communicate",
"Method calls, shared objects, streams, events, queues and database operations are six different mechanisms. This chapter separates them.") + """

<h3><span class="n">3.1</span>The problem with saying "they communicate"</h3>
<p>When you describe an application it is tempting to say that components "talk to each other"
and leave it there. That sentence hides six distinct mechanisms with completely different
properties. A method call is synchronous and immediate. A stream carries bytes or characters
in one direction and can block. A queue decouples two threads in time. An event listener
inverts control. A database operation crosses an execution boundary. An interrupt is a
cooperative request, not a command.</p>

<p>Choosing the wrong one produces the classic failures: a frozen interface, a race condition,
a lost update, a deadlock, a silent data loss. So this chapter names each mechanism, states its
properties, and shows where BasinWatch uses it — and, just as importantly, where it does not.</p>

""" + figure("d28_dependency_graph", "4", "Component dependency graph",
"Who creates whom, and the one-way direction of dependencies: app depends on engine, engine depends on domain, io and db, and nothing depends back on app.",
"landscape") + """

<h3><span class="n">3.2</span>Mechanism one: the method call</h3>
<p>The ordinary method call is synchronous, in-process, typed and immediate. The caller waits,
the callee runs on the caller's thread, and arguments and return values are checked by the
compiler.</p>

<p>BasinWatch uses method calls for everything that is fast and deterministic.
<span class="mono">BasinModel.process(event)</span> is a method call.
<span class="mono">BasinZone.assessRisk(waterLevel)</span> is a method call.
<span class="mono">SessionSnapshot.from(snapshot)</span> is a method call. None of them touches
a disk, a network or a thread.</p>

""" + core("""<p>The design rule the project follows is: <b>a method call may not block on
external work.</b> Anything that reads a disk, waits for another thread, or talks to a database
is moved behind a different mechanism — a future, a queue, or a background thread. That is why
the model's methods are short and why the engine's file and database work is submitted rather
than performed inline.</p>""") + """

<h3><span class="n">3.3</span>Mechanism two: shared objects under a monitor</h3>
<p>Two threads can communicate simply by reading and writing the same object. The cost is that
every such access needs protection, and the protection is what creates the bugs.</p>

<p><span class="mono">ResourceAllocator</span> is the canonical example: a shared, finite
inventory read and written by several response workers.</p>

""" + code('''public synchronized boolean tryReserve(Map<ResourceType, Integer> request) {
    validateRequest(request);
    for (Map.Entry<ResourceType, Integer> entry : request.entrySet()) {
        if (available.get(entry.getKey()) < entry.getValue()) {
            return false;                       // nothing has been changed yet
        }
    }
    request.forEach((type, amount) -> available.put(type, available.get(type) - amount));
    return true;
}''', "from BasinWatch, domain/ResourceAllocator.java — check every requirement, then decrement.") + """

<p>Read that method twice. The first loop only <i>checks</i>. If any single requirement cannot
be met, the method returns <span class="mono">false</span> having changed nothing at all. Only
after every requirement has been confirmed does the second loop decrement. That is what makes
the reservation all-or-nothing: there is no moment at which a caller could observe a partially
reserved state, because the entire method holds the object's monitor from start to finish.</p>

""" + connect("""<p>This is also the project's deadlock-avoidance strategy, which its own
architecture notes describe directly: one short inventory monitor, no I/O inside it, no nested
acquisition of another lock, and a stable policy. A lock-ordering cycle requires two locks
acquired in opposite orders by two threads; with one lock, that cycle cannot form.</p>""") + """

<h3><span class="n">3.4</span>Mechanism three: streams</h3>
<p>A stream is a one-directional channel that carries a sequence of bytes or characters, with
its own buffering and blocking behaviour. It is the subject of all of Part II, so here we only
need its role in the architecture: it is how the feed thread hands data to the intake thread
without either one knowing the other's class.</p>

""" + code('''// BasinEngine.startFeed() — creating the connected pair
PipedWriter writer = new PipedWriter();
PipedReader reader = new PipedReader(writer, 8_192);
feedWriter = writer;
intakeThread = new Thread(new SensorIntake(
        new BufferedReader(reader), eventBuffer, this::reportFailure,
        ignored -> publishDiagnosticsStatus()), "basin-sensor-intake");
sensorFeed = new SensorFeed(writer, List.of("UPR", "MIL", "NOR", "OLD", "MAR", "SOU"),
        settings, tickSequence, this::reportFailure);
intakeThread.start();
sensorFeed.start();''', "from BasinWatch, engine/BasinEngine.java — the writer is handed to the feed, the reader to intake.") + """

<p>Note what is <i>not</i> shared: the feed never sees the
<span class="mono">EventBuffer</span>, and intake never sees the
<span class="mono">SensorFeed</span>. The only object they have in common is the pipe. This is
a much narrower contract than a shared list, and it is why the two threads can be reasoned
about separately.</p>

<h3><span class="n">3.5</span>Mechanism four: the queue with condition waiting</h3>
<p>A queue decouples producer and consumer in time. The producer does not wait for the consumer
to be ready; the consumer does not poll. The mechanism that makes this work is
<span class="mono">wait()</span> and <span class="mono">notifyAll()</span> under a monitor, and
it must be written carefully.</p>

""" + code('''public synchronized boolean put(BasinEvent event) throws InterruptedException {
    if (event == null) {
        throw new IllegalArgumentException("Event is required.");
    }
    while (!closed && events.size() == capacity) {     // condition re-checked in a loop
        waitingProducers++;
        try {
            wait();                                    // releases the monitor while waiting
        } finally {
            waitingProducers--;
        }
    }
    if (closed) {
        return false;
    }
    events.addLast(event);
    notifyAll();                                       // wake every waiter to re-check
    return true;
}''', "from BasinWatch, engine/EventBuffer.java — a correct condition-wait loop.") + """

<p>Four properties of that code are the whole lesson, and they appear in every correct
condition-wait implementation:</p>

<ol>
<li><b>Wait inside a loop, never inside an <span class="mono">if</span>.</b> A thread that
wakes up is not guaranteed that its condition is now true — another consumer may have taken the
item first. So the test is repeated.</li>
<li><b>Hold the monitor.</b> <span class="mono">wait()</span> may only be called by a thread
that owns the object's monitor. The <span class="mono">synchronized</span> keyword on the
method provides it.</li>
<li><b>Signal with <span class="mono">notifyAll()</span>, not
<span class="mono">notify()</span>.</b> Producers and consumers wait on the same monitor, so
waking one arbitrary thread might wake a producer when only consumers can progress.
<span class="mono">notifyAll()</span> lets every waiter re-check, and the ones that cannot
proceed go back to waiting.</li>
<li><b>Count the waiters.</b> <span class="mono">waitingProducers</span> and
<span class="mono">waitingConsumers</span> are incremented and decremented around the wait in a
<span class="mono">finally</span> block, so the diagnostic view stays accurate even if the
thread is interrupted. These counters are diagnostics, not synchronisation — an important
distinction this chapter returns to.</li>
</ol>

""" + distinct("""<p><span class="mono">wait()</span> releases the monitor;
<span class="mono">sleep()</span> does not. This single sentence explains most of the confusion
around Java threading. A waiting thread lets another thread enter the synchronized region; a
sleeping thread keeps the lock and blocks everyone else. BasinWatch uses
<span class="mono">wait()</span> for coordination and <span class="mono">Thread.sleep(...)</span>
only for cadence — the feed's interval and the shutdown quiescence check — never as a
signalling device.</p>""") +

mistake("""<p>Using <span class='mono'>Thread.sleep()</span> to wait for another thread's work,
and using a flag variable polled in a loop, are the two most common substitutes for condition
waiting. Both are wrong for the same reason: they guess at timing instead of reacting to state.
A sleeping consumer may sleep too long (wasted latency) or too little (busy spinning), and a
polled flag cannot wake anybody at the moment the state changes.</p>""") + """

<h3><span class="n">3.6</span>Mechanism five: events and listeners</h3>
<p>An event listener inverts control: instead of a component asking for data, the component
declares interest and is called when something happens. In BasinWatch the interface registers
listeners on the engine.</p>

""" + code('''engine.addSnapshotListener(snapshot ->
        SwingUtilities.invokeLater(() -> updateSnapshot(snapshot)));
engine.addStatusListener(message ->
        SwingUtilities.invokeLater(() -> statusLabel.setText(message)));
engine.addDatabaseStatusListener(message ->
        SwingUtilities.invokeLater(() -> databaseStatus.setText(message)));''',
"from BasinWatch, app/MainFrame.java and app/DatabaseHistoryPanel.java — three listener registrations.") + """

<p>The engine holds these in <span class="mono">CopyOnWriteArrayList</span> instances, which is
the right collection when reads vastly outnumber writes and iteration happens concurrently:
publication iterates a stable snapshot of the list while a registration safely creates a new
array.</p>

<p>The important part of this mechanism is the wrapper. The listener is invoked on a worker
thread, and the very first thing it does is post the update to the event-dispatch thread. The
listener contract is therefore: <i>I may be called from any thread; I will not touch Swing
directly.</i> Chapter 16 examines that hand-off in detail.</p>

<h3><span class="n">3.7</span>Mechanism six: database operations</h3>
<p>A database operation is the only mechanism in this list that leaves the Java execution
model. Even with an embedded SQLite file, the operation involves a different execution path:
SQL is parsed and planned, rows are read through a cursor, and failures arrive as
<span class="mono">SQLException</span> rather than as ordinary Java exceptions.</p>

<p>BasinWatch wraps this in two different shapes depending on direction:</p>

<ul>
<li><b>Writes are fire-and-forget.</b> <span class="mono">recordSensor</span>,
<span class="mono">recordDispatch</span> and <span class="mono">recordCompletion</span> return
<span class="mono">void</span>. They enqueue a lambda and return immediately. The caller learns
about failure through the status listener, not through a return value.</li>
<li><b>Reads return a future.</b> <span class="mono">loadHistory</span> returns a
<span class="mono">CompletableFuture&lt;List&lt;DatabaseHistoryEntry&gt;&gt;</span>, so the
interface can attach a callback without blocking.</li>
</ul>

""" + code('''public void recordSensor(SensorReading reading, ZoneSnapshot zone, Instant timestamp,
                           boolean riskEscalated) {
    enqueue(() -> {
        sensors.insert(reading, zone, timestamp);
        if (riskEscalated) {
            operationalEvents.insert(timestamp, "RISK ESCALATION", zone.id(),
                    "Risk increased to " + zone.risk().name() + " at " + zone.name());
        }
    });
}''', "from BasinWatch, db/DatabaseService.java — a write is a queued lambda, not a blocking call.") +

distinct("""<p>A <span class='mono'>CompletableFuture</span> is not a thread. It is a handle to
a result that may not exist yet. <span class='mono'>whenComplete</span> registers work to run
when the result arrives, and that work runs on whichever thread completed the future — which is
why every UI callback in this project immediately calls
<span class='mono'>SwingUtilities.invokeLater</span>.</p>""") + """

<h3><span class="n">3.8</span>Choosing between the six</h3>
<p>Table 3.1 is the decision table this chapter has been building towards. It is worth
memorising, because examiners like asking "which mechanism would you use here?"</p>

""" + table(
  ["Mechanism", "Direction", "Blocking?", "Thread boundary?", "Used in BasinWatch for"],
  [
    ["Method call", "two-way", "yes, briefly", "no — same thread",
     "All domain logic; every fast, deterministic operation"],
    ["Shared object under a monitor", "two-way", "may block on the lock", "yes",
     "The finite resource inventory"],
    ["Stream", "one-way", "yes when full or empty", "usually yes",
     "Observation text from feed to intake; all file access"],
    ["Queue with wait/notifyAll", "one-way", "yes when full or empty", "yes",
     "The bounded event buffer between intake and workers"],
    ["Listener / event", "one-way, inverted", "no", "callback may arrive on any thread",
     "Snapshot, status and database-status publication to the UI"],
    ["Database operation", "request and response", "yes unless offloaded", "yes — moved to its own thread",
     "Optional SQLite history: writes queued, reads via futures"],
  ],
  caption="<b>Table 3.1</b> — The six communication mechanisms and where each belongs.") +

exam("""<p>If you are asked why a pipe is used when a shared list would work, the answer is
about contract width. A shared list gives both threads access to every element and to the
list's own methods, so any bug in either thread can corrupt it. A pipe gives them one narrow
operation each: write a character sequence, read a character sequence. Narrower contracts are
easier to reason about, and the pipe also provides back-pressure for free — the writer blocks
when the buffer is full.</p>""") + """

<h3><span class="n">3.9</span>The two boundaries, restated</h3>
<p>Chapter 1 claimed that the technologies meet at exactly two boundaries. With the six
mechanisms named, that claim can be made precise.</p>

<div class="grid2">
<div>
<h4 class="plain">Boundary one — the accepted event</h4>
<p>A worker has just applied an event to the model. At this single point the engine fans out: it
appends to the journal, submits to the archive worker, and enqueues a database operation.
Everything downstream of that fan-out is persistence, and none of it can change the model.</p>
</div>
<div>
<h4 class="plain">Boundary two — the published snapshot</h4>
<p>The engine calls every registered snapshot listener with an immutable value. That call
crosses from background threads to the event-dispatch thread and is the only channel by which
background work becomes visible to a human.</p>
</div>
</div>

""" + connect("""<p>Chapter 20 traces four complete scenarios across these boundaries: an
observation, a dispatch with its transaction, a save-and-restore cycle, and a history read.
Each scenario exercises a different subset of the six mechanisms, which is exactly why tracing
them is a better revision exercise than reciting the table.</p>""") +

summary([
  "Six distinct communication mechanisms: method call, shared object under a monitor, stream, queue with condition waiting, listener event, and database operation.",
  "A method call may not block on external work; anything slow moves behind a queue, a future or a background thread.",
  "Shared state requires a monitor, and the reservation is all-or-nothing: check everything, then change everything.",
  "A stream is a narrow one-directional contract with built-in back-pressure — that is why a pipe beats a shared list.",
  "A condition wait must be a loop, must hold the monitor, must use notifyAll, and must re-check its condition.",
  "wait() releases the monitor; sleep() does not. sleep() is for cadence, never for coordination.",
  "Writes to the database are queued and non-blocking; reads return CompletableFutures whose callbacks hop back to the EDT.",
]) + keyterms([
  "<b>Monitor</b> — the lock associated with an object; entered by <span class='mono'>synchronized</span>.",
  "<b>Condition wait</b> — <span class='mono'>wait()</span> inside a loop that re-tests a predicate while holding a monitor.",
  "<b>Back-pressure</b> — a bounded channel making a fast producer slow down instead of consuming unbounded memory.",
  "<b>Inversion of control</b> — a component declaring interest and being called, rather than polling for change.",
  "<b>Fire-and-forget</b> — a call that queues work and returns immediately, reporting failure out of band.",
]) + "</div>")

HTML = PART + CH1 + CH2 + CH3
