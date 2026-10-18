"""PART VI — Putting Everything Together.  Chapters 20-21."""
from . import *

P = []
B20, B21 = [], []

P.append("""
<div class="part-page">
  <div class="pnum">PART VI</div>
  <h1>Putting Everything Together</h1>
  <div class="prule"></div>
  <div class="pintro">This part returns to the whole system. Four real scenarios are traced from their
  origin to their visible result, crossing every thread and every layer the book has described. Then
  the final exercise gives you the eight questions that turn knowing the parts into explaining the
  whole.</div>
  <div class="chapters">
    <div><span>20</span>End-to-End BasinWatch Architecture Walkthrough</div>
    <div><span>21</span>Final Integration Exercise</div>
  </div>
</div>
""")

# ======================================================================
# CHAPTER 20
# ======================================================================
B20.append(chapter(20, "End-to-End BasinWatch Architecture Walkthrough",
"Four scenarios traced through every layer, each following a genuinely different route. This is the integrative centerpiece of the book."))

B20.append("""
<h3><span class="n">20.1</span>Why four scenarios and not one</h3>
<p>It is tempting to trace a single "typical" request through the system and declare the architecture
explained. That would be misleading, because BasinWatch has four genuinely different data paths and
forcing them into one diagram would misrepresent at least three of them.</p>
""")

B20.append(table(
  ["Scenario", "Origin", "Threads crossed", "Persists to", "Visible result"],
  [
    ["<b>A</b> — an observation", "Sensor feed thread", "Feed, intake, worker, database", "Log, archive, database", "Map colour and activity timeline"],
    ["<b>B</b> — a dispatch", "Operator click", "EDT, worker, control, database", "Log, database (transaction)", "Resource board and mission list"],
    ["<b>C</b> — save and restore", "Operator click, then next launch", "EDT, control", "Session snapshot file", "The whole restored model"],
    ["<b>D</b> — a history read", "Operator click", "EDT, database, EDT", "Nothing — it is a read", "A populated history table"],
  ],
  caption="<b>Table 20.1</b> — The four scenarios and how each differs."))

B20.append(core("""<p>Read the table's second and third columns together. Scenario A is the only one
that starts without a user. Scenario D is the only one that writes nothing. Scenario B is the only one
that needs a transaction. Scenario C is the only one whose result is visible on a <i>later</i> run. Those
differences are why one trace would not be enough.</p>"""))

B20.append(figure("d27_end_to_end_sequence", "24", "The full sequence diagram, with all four scenarios",
"Repeated from Diagram 24 in Chapter 16 so the trace can be read beside the scenarios. The complete sequence across the operator, the event-dispatch thread, the engine, the sensor path, the workers, the file layer, the database thread and the SQLite file. Scenarios A, B, C and D are marked so you can follow each separately.",
"portrait"))

B20.append("""
<h3><span class=\"n\">20.2</span>Scenario A: an observation, fully traced</h3>
<p>This is the system's heartbeat. Nothing is clicked; the application produces its own data.</p>
""")

B20.append(trace("Scenario A — from the feed loop to a coloured zone on the map", [
  "<b>1. The feed loop wakes.</b> <span class='mono'>SensorFeed.run</span> is in its timed loop on <span class='mono'>basin-sensor-feed</span>. It increments the shared tick counter and begins a new interval.",
  "<b>2. Six readings are generated.</b> For each of the six zones, a <span class='mono'>SensorReading</span> is constructed with randomised rainfall and rise values within the configured bounds. The compact constructor validates the ranges as it is built.",
  "<b>3. Each reading is encoded and written.</b> <span class='mono'>reading.encode()</span> produces a pipe-delimited line such as <span class='mono'>READ|214|MIL-ST-2|MIL|12.400|3.100</span>, which is written into the <span class='mono'>PipedWriter</span> along with a line separator.",
  "<b>4. The pipe transfers and applies back-pressure.</b> Characters move into the pipe's 8,192-character buffer. If intake has fallen behind and the buffer is full, the feed's write blocks here — the producer waits rather than overrunning memory.",
  "<b>5. Intake reads a line.</b> On <span class='mono'>basin-sensor-intake</span>, <span class='mono'>SensorIntake.run</span> is blocked in <span class='mono'>source.readLine()</span>. It wakes, receives the line, and returns it without the terminator.",
  "<b>6. The record is parsed and validated.</b> <span class='mono'>SensorReading.parse</span> splits on the pipe character and checks that there are exactly six fields beginning with <span class='mono'>READ</span>. A malformed line is reported and skipped; the loop continues.",
  "<b>7. The event is queued.</b> <span class='mono'>eventBuffer.put(event)</span> adds it to the bounded deque. If the buffer is full, this call waits on the monitor; if it is closed, the method returns false and intake stops.",
  "<b>8. A worker takes it.</b> One of the three <span class='mono'>ResponseWorker</span> threads is waiting in <span class='mono'>eventBuffer.take()</span>. It wakes, removes the event, and calls <span class='mono'>model.process(event)</span>.",
  "<b>9. The model applies it.</b> <span class='mono'>applyReading</span> finds the zone, calls <span class='mono'>BasinZone.apply(reading)</span>, and — crucially — receives false if the reading is stale. The risk level is recomputed from the new water level.",
  "<b>10. Escalation is detected.</b> The new risk rank is compared with the previous one. If it increased, the activity message is prefixed with \u201cRisk increased:\u201d and a boolean is prepared for the database.",
  "<b>11. Activity is recorded and the snapshot is published.</b> An <span class='mono'>ActivityEntry</span> is added to the model's ring buffer, and <span class='mono'>model.snapshot()</span> produces a new immutable <span class='mono'>BasinSnapshot</span>.",
  "<b>12. The listener chain fires.</b> <span class='mono'>BasinEngine</span> calls every snapshot listener on the worker thread. Each listener's first action is <span class='mono'>SwingUtilities.invokeLater</span>.",
  "<b>13. The EDT updates the interface.</b> The map panel's snapshot field is replaced and <span class='mono'>repaint()</span> is requested; the activity list and labels are updated. The zone's circle changes colour.",
  "<b>14. Persistence runs in parallel.</b> The engine appends each activity message to the journal, submits the reading to the archive worker, and — only if the model changed — calls <span class='mono'>database.recordSensor(...)</span>.",
  "<b>15. The database thread writes.</b> On <span class='mono'>basin-database</span>, the repository prepares the nine-placeholder insert, binds every value, and executes it. If the risk escalated, a second row is written to <span class='mono'>operational_events</span>.",
]))

B20.append(visual("""<p>Follow the thread changes in Scenario A: feed, intake, worker, then EDT <i>and</i>
database in parallel. Steps one to three are the feed thread. Steps five to seven are intake. Steps eight
to twelve are a worker. Steps thirteen and fifteen happen concurrently on two different threads. Only
step thirteen touches Swing.</p>"""))

B20.append(practice("""<p>Step nine is worth pausing on, because it is where the architecture earns its
keep. The model decides whether a reading counts, and everything downstream obeys that decision:</p>
<pre class="long"><span class="cm">// BasinZone.apply returns false for a stale reading</span>
<span class="kw">boolean</span> changed = zone.apply(reading);
<span class="kw">if</span> (!changed) {{
    <span class="cm">// no activity entry, no archive record, no database row</span>
    <span class="kw">return</span>;
}}</pre>
<p>One boolean, decided in the domain, determines whether three separate persistence mechanisms write
anything at all. That is what "the model is the source of truth" means in practice.</p>"""))

B20.append("""
<h3><span class=\"n\">20.3</span>Scenario B: a dispatch, and its transaction</h3>
<p>This scenario starts with a person and ends with a changed resource board. It is also the only
scenario that needs a database transaction.</p>
""")

B20.append(trace("Scenario B — from a dispatch click to a changed resource board", [
  "<b>1. The operator selects a mission type and a zone, then clicks Dispatch.</b> Two combo boxes and a button, all on the EDT.",
  "<b>2. The listener calls the engine.</b> <span class='mono'>engine.dispatch(zoneId, missionType)</span> — one call, returning immediately.",
  "<b>3. The engine submits the work.</b> The request is submitted to <span class='mono'>basin-control</span> and the caller receives a <span class='mono'>CompletableFuture</span>.",
  "<b>4. The control thread reserves resources.</b> <span class='mono'>ResourceAllocator.tryReserve(requirements)</span> runs under the allocator's monitor: it checks every requirement, and only if all are satisfied does it decrement any of them.",
  "<b>5. A failed reservation stops here.</b> If any resource is short, the method returns false, no state changes, and the future completes with a message the interface displays. Nothing is persisted, because nothing happened.",
  "<b>6. A successful reservation creates a mission.</b> <span class='mono'>BasinModel</span> constructs a <span class='mono'>ResponseMission</span> with an identifier, a start tick and a completion tick derived from the mission type's duration.",
  "<b>7. The model publishes a new snapshot.</b> The resource board now shows the deduction and the mission list shows the new operation. The listener chain posts both to the EDT.",
  "<b>8. Persistence begins.</b> The engine appends an ALLOCATED entry to the journal and calls <span class='mono'>database.recordDispatch(...)</span>.",
  "<b>9. The database transaction opens.</b> On <span class='mono'>basin-database</span>, a connection is obtained and <span class='mono'>setAutoCommit(false)</span> is called.",
  "<b>10. Three writes execute on that one connection.</b> The mission row, one resource-usage row per required resource, and an audit event — all through package-private repository overloads that accept the shared connection.",
  "<b>11. The transaction commits.</b> All three rows become visible together, or none of them does.",
  "<b>12. A failure rolls back.</b> If any of the three throws, <span class='mono'>rollback()</span> discards all of them, and the status listener reports the failure to the interface.",
  "<b>13. Completion is scheduled.</b> In the model, the mission's completion tick is in the future. When the tick arrives, a later pulse completes the mission, releases the resources, and records a second transaction.",
]))

B20.append(visual("""<p>Notice step four and step eleven are the same idea implemented twice. Step four
makes an <i>in-memory</i> change atomic using a monitor; step eleven makes a <i>database</i> change atomic
using a transaction. Both exist to prevent a partially completed change from being observable. Chapter 13
makes this comparison explicitly.</p>"""))

B20.append(mistake("""<p>A common wrong design puts the resource reservation <i>after</i> the database
write. Then a failed reservation leaves a mission row claiming resources that were never deducted, and the
history contradicts the live state. The order matters: reserve first, because the in-memory reservation is
the decision, and the database records the decision.</p>"""))

B20.append("""
<h3><span class=\"n\">20.4</span>Scenario C: save, exit, and restore</h3>
<p>This scenario is the only one whose result is visible on a later run, and it is the reason the snapshot
format is versioned and validated.</p>
""")

B20.append(trace("Scenario C — from a save click to a restored basin on the next launch", [
  "<b>1. The operator clicks Save.</b> On the EDT, the listener opens a file chooser and obtains a target path.",
  "<b>2. The listener calls the engine.</b> <span class='mono'>engine.save(target)</span>, returning a future.",
  "<b>3. The control thread takes a snapshot.</b> <span class='mono'>model.snapshot()</span> produces an immutable <span class='mono'>BasinSnapshot</span> while holding the model's monitor, so the copy is consistent.",
  "<b>4. The snapshot is converted to a DTO.</b> <span class='mono'>SessionSnapshot.from(snapshot)</span> copies zones, resources, missions and recent activity into serializable plain classes.",
  "<b>5. A temporary file is written.</b> <span class='mono'>SnapshotStore.save</span> opens <span class='mono'>name.bws.tmp</span>, writes the format version, then serializes the DTO.",
  "<b>6. The temporary file is moved into place.</b> <span class='mono'>Files.move(..., ATOMIC_MOVE)</span> replaces the real file in one step, so an interrupted save cannot corrupt an existing snapshot.",
  "<b>7. The status is reported.</b> The future completes with the path, and the callback posts the message to the EDT.",
  "<b>8. Later, the application exits cleanly.</b> <span class='mono'>closeEngine()</span> stops the feed, closes the pipe, joins intake, drains the archive queue, flushes the journal, and writes <span class='mono'>last-session.bws</span> automatically.",
  "<b>9. On the next launch, the engine checks for a restore point.</b> It looks for <span class='mono'>last-session.bws</span> in the saves directory.",
  "<b>10. Four gates are applied on load.</b> The file size is bounded, an <span class='mono'>ObjectInputFilter</span> approves only <span class='mono'>com.basinwatch</span>, <span class='mono'>java.lang</span>, <span class='mono'>java.util</span> and <span class='mono'>java.time</span> classes, the format version is compared, and the DTO is validated.",
  "<b>11. The model is rebuilt.</b> Zones are restored with their water levels, the resource allocator is refilled, missions are reinstated with their remaining durations, and the activity ring buffer is repopulated.",
  "<b>12. The interface shows the restored state.</b> The map, the resource board, the mission list and the activity timeline all reflect the saved session, and the tick counter resumes.",
]))

B20.append(visual("""<p>Count the differences between the save path and the restore path. Saving is
straightforward: copy, convert, write, move. Restoring is defensive: four gates before a single value is
trusted. That asymmetry is deliberate and it is the single most important thing to understand about
serialization in an application — writing is your own data, reading is unverified input.</p>"""))

B20.append("""
<h3><span class=\"n\">20.5</span>Scenario D: a history read</h3>
<p>This scenario writes nothing. It is the shortest of the four, and it is the one that most directly
connects JDBC to Swing.</p>
""")

B20.append(trace("Scenario D — from a Refresh click to a populated table", [
  "<b>1. The operator clicks Refresh.</b> Delivered to the EDT and dispatched to the button's listener.",
  "<b>2. The listener calls <span class='mono'>historyPanel.reload()</span> and returns.</b> Nothing blocks.",
  "<b>3. The panel asks the engine.</b> <span class='mono'>engine.loadHistory(200)</span> returns a future immediately.",
  "<b>4. Availability is checked.</b> If the database is unavailable, an already-completed future holding an empty list is returned and steps five to eight are skipped.",
  "<b>5. The query is enqueued.</b> A lambda is submitted to <span class='mono'>basin-database</span>.",
  "<b>6. The repository prepares and binds.</b> One placeholder for the limit, bound with <span class='mono'>setInt(1, limit)</span>.",
  "<b>7. SQLite executes and returns rows.</b> The index on <span class='mono'>operational_events</span> serves the descending time order.",
  "<b>8. Rows are mapped and the future completes.</b> Each row becomes a <span class='mono'>DatabaseHistoryEntry</span>; <span class='mono'>future.complete(entries)</span> runs the callback on the database thread.",
  "<b>9. The callback posts to the EDT.</b> <span class='mono'>SwingUtilities.invokeLater</span>.",
  "<b>10. The table model is updated.</b> <span class='mono'>setEntries(entries)</span> copies the list and calls <span class='mono'>fireTableDataChanged()</span>.",
  "<b>11. The table repaints.</b> It asks the model for the row count and redraws the visible rows.",
]))

B20.append("""
<h3><span class=\"n\">20.6</span>Where the four scenarios differ, and why that matters</h3>
<p>Placing the four traces side by side shows the architecture's real shape more clearly than any single
diagram.</p>
""")

B20.append(table(
  ["", "A — observation", "B — dispatch", "C — save/restore", "D — history read"],
  [
    ["Initiated by", "A timer", "A click", "A click, then a later launch", "A click"],
    ["First thread", "Feed", "EDT", "EDT", "EDT"],
    ["Crosses the pipe?", "<b>Yes</b>", "No", "No", "No"],
    ["Needs a transaction?", "No — single-row inserts", "<b>Yes</b> — three related writes", "No", "No — read only"],
    ["Writes files?", "Log and archive", "Log", "<b>Snapshot</b>", "No"],
    ["Writes the database?", "Yes, if the model changed", "Yes, transactionally", "No", "No"],
    ["Result visible immediately?", "Yes, on the map", "Yes, on the resource board", "No — on the next launch", "Yes, in the table"],
    ["Can fail silently?", "Yes — a malformed record is skipped", "No — a failed reservation is reported", "No — a failed save is reported", "Yes — an unavailable database shows empty history"],
  ],
  caption="<b>Table 20.2</b> — The four scenarios compared across the dimensions that matter."))

B20.append("""
<h3><span class=\"n\">20.7</span>The dependency graph</h3>
<p>Finally, the static picture: who depends on whom. Dependencies point one way, and that direction is
what makes the layers testable and replaceable.</p>
""")

B20.append(figure("d28_dependency_graph", "4", "The component dependency graph, revisited",
"Repeated from Diagram 4 in Chapter 3, now read as a design argument. Arrows point from a component to what it depends on. The app package depends on the engine, the engine depends on the domain, io and db packages, and none of those depends back on the app. The domain depends on nothing.",
"landscape"))

B20.append("""
<p>Three properties of that graph are worth naming.</p>

<p><b>The domain is at the bottom and depends on nothing.</b> No file, no database, no Swing. That is why
the model can be tested in a unit test with no setup at all, and why the same model could be driven by a
different interface.</p>

<p><b>There are no cycles.</b> Nothing the engine depends on depends on the engine. A cycle would make the
layers impossible to test in isolation and impossible to replace.</p>

<p><b>The interface is at the top and depends on the engine, not the reverse.</b> The engine has no import
of <span class="mono">javax.swing</span> anywhere, which is what allows the whole application to run
headless in a test.</p>
""")

B20.append(connect("""<p>This chapter has traced four paths through that graph. If you can redraw
Diagram 4 from memory, name the thread for each box, and describe one scenario that crosses it, you can
answer almost any architecture question about this application.</p>"""))

B20.append(exam("""<p>In a viva, the strongest thing you can do is offer to trace a scenario and then
choose the one that best matches the question. If the question is about persistence, trace C. If it is
about transactions, trace B. If it is about threading, trace A. If it is about the interface and the
database together, trace D. Choosing the scenario is itself evidence that you understand the
architecture.</p>"""))

B20.append(summary([
  "Four genuinely different paths exist: an observation, a dispatch, a save-and-restore, and a history read.",
  "Scenario A crosses the pipe and fans out to three persistence mechanisms, but writes to the database only when the model changed.",
  "Scenario B is the only transactional path, and it reserves resources before recording anything.",
  "Scenario C is defensive on the way in and straightforward on the way out, because reading is unverified input.",
  "Scenario D writes nothing and is the clearest example of the JDBC-to-Swing path.",
  "The dependency graph is acyclic, with the domain at the bottom and the interface at the top.",
  "The engine has no dependency on Swing, which is what makes the application testable without a window.",
]))

B20.append(keyterms([
  "<b>Fan-out</b> — one decision causing several independent downstream operations.",
  "<b>Restore point</b> — a saved state the application checks for at start-up.",
  "<b>Acyclic dependency graph</b> — a component graph with no cycles, so each layer can be tested and replaced independently.",
  "<b>Source of truth</b> — the single component whose decision everything else obeys; here, the domain model.",
]))

B20.append("</div>")

# ======================================================================
# CHAPTER 21
# ======================================================================
B21.append(chapter(21, "Final Integration Exercise",
"A guided walkthrough of the real code, the eight questions that turn knowledge of parts into an explanation of the whole, and where every syllabus concept lives."))

B21.append("""
<h3><span class=\"n\">21.1</span>How to use this chapter</h3>
<p>This is not a summary. It is an exercise. Read the guided walkthrough below, then answer the eight
questions from memory, using the code as a reference only to check yourself. If you can answer all eight
about any class in the project, you can explain the application.</p>
""")

B21.append("""
<h3><span class=\"n\">21.2</span>Guided walkthrough: following one class completely</h3>
<p>Take <span class="mono">SensorIntake</span>. It is a small class — a single
<span class="mono">run</span> method — but it sits at the junction of streams, threads, validation and
queueing, so it is the ideal subject for the exercise.</p>
""")

B21.append(code('''public final class SensorIntake implements Runnable {
    private final BufferedReader source;
    private final EventBuffer buffer;
    private final Consumer<String> warningReporter;
    private final Consumer<String> statusReporter;

    public SensorIntake(BufferedReader source, EventBuffer buffer,
                        Consumer<String> warningReporter, Consumer<String> statusReporter) {
        this.source = source;
        this.buffer = buffer;
        this.warningReporter = warningReporter;
        this.statusReporter = statusReporter;
    }

    @Override
    public void run() {
        statusReporter.accept("Sensor intake online");
        try (source) {
            String line;
            while ((line = source.readLine()) != null) {
                BasinEvent event;
                try {
                    if (line.startsWith("PULSE|")) {
                        event = new SimulationPulse(Long.parseLong(line.substring(6)));
                    } else {
                        event = SensorReading.parse(line);
                    }
                } catch (IllegalArgumentException ex) {
                    warningReporter.accept("Discarded malformed sensor record: " + ex.getMessage());
                    continue;
                }
                if (!buffer.put(event)) {
                    warningReporter.accept("Event buffer closed; intake stopping.");
                    break;
                }
            }
        } catch (IOException ex) {
            warningReporter.accept("Sensor intake ended with an I/O error: " + ex.getMessage());
        } catch (InterruptedException ex) {
            Thread.currentThread().interrupt();
        } finally {
            statusReporter.accept("Sensor intake offline");
        }
    }
}''', "from BasinWatch, engine/SensorIntake.java — the complete class, unedited."))

B21.append("""
<p>Now apply the eight questions to it.</p>
""")

B21.append("""
<h4 class="plain">1. Why is this class needed?</h4>
<p>Because reading and validating the observation stream is a distinct job with its own failure modes. It
blocks on input, it must tolerate malformed data without stopping, and it must hand off to a queue that can
be full. Putting that in <span class="mono">SensorFeed</span> would make the producer responsible for the
consumer's timing; putting it in the workers would make every worker re-validate the same stream. As its own
task, it can be reasoned about — and tested — alone.</p>

<h4 class="plain">2. How does it communicate with other classes?</h4>
<p>Through four constructor arguments, each a narrow contract. A
<span class="mono">BufferedReader</span> (a stream), an <span class="mono">EventBuffer</span> (a queue), and
two <span class="mono">Consumer&lt;String&gt;</span> callbacks (events). It has no reference to the feed, the
model, the engine or any interface class. That is why it can be tested by handing it a
<span class="mono">StringReader</span> and a fresh buffer.</p>

<h4 class="plain">3. Which data does it receive?</h4>
<p>Lines of text, one per event. Each line is either a pipe-delimited observation beginning with
<span class="mono">READ|</span>, or a pulse beginning with <span class="mono">PULSE|</span>. It receives
nothing else — no objects, no configuration, no state.</p>

<h4 class="plain">4. Does it use a stream, an event, a method call, or a database query?</h4>
<p>All three of the first, and none of the last. A <b>stream</b> supplies the characters. A <b>method
call</b> performs the parse, which validates. An <b>event</b> — a callback — reports warnings and status,
and the queue hand-off is a fourth mechanism, condition waiting. There is no database interaction at all,
which is correct: persistence is a decision for the engine, made after the model has processed the event.</p>

<h4 class="plain">5. How does its result affect the application?</h4>
<p>Indirectly and only through the queue. For every accepted line it places one event in the buffer; a
worker then takes it. For every rejected line it produces a warning and continues. It never returns a value,
because it is a long-running task rather than a function — its effect is the stream of events it delivers.</p>

<h4 class="plain">6. What survives application shutdown?</h4>
<p>Nothing that this class owns. The buffer's contents are drained and processed before shutdown; the pipe
is closed; the reader is closed by try-with-resources. The durable record is created by the engine — a
journal line, an archive record and possibly a database row — none of which this class touches. That
separation is deliberate.</p>

<h4 class="plain">7. What happens if the relevant operation fails?</h4>
<p>Three distinct outcomes, and the differences are the design.</p>
<ul>
<li><b>A malformed line</b> produces a warning and the loop continues. One bad record cannot stop the
stream.</li>
<li><b>An <span class="mono">IOException</span></b> ends the loop and reports. The channel is broken; there
is nothing left to read.</li>
<li><b>A closed buffer</b> makes <span class="mono">put</span> return false, so intake reports and stops
cleanly rather than waiting forever for a consumer that will never come.</li>
</ul>

<h4 class="plain">8. Which design alternative is taught in the lecture notes?</h4>
<p>Reading from a file with <span class="mono">FileReader</span> and a
<span class="mono">BufferedReader</span> in a <span class="mono">main</span> method. That is the same read
loop with a different source and no threading. The lecture version demonstrates the stream API; this
version demonstrates what changes when the source is another thread and the consumer is concurrent — which
is why the try-with-resources, the two failure categories and the closed-buffer check all matter.</p>
""")

B21.append(core("""<p>Notice what those eight answers produced between them. They covered streams, threads,
queues, callbacks, validation, exception strategy, persistence boundaries and the relationship to the
lecture material — for one small class. That is the exercise's purpose: the same eight questions work on
<span class='mono'>BasinZone</span>, on <span class='mono'>SensorReadingRepository</span>, on
<span class='mono'>SnapshotStore</span> and on <span class='mono'>DatabaseHistoryPanel</span>.</p>"""))

B21.append("""
<h3><span class=\"n\">21.3</span>Where every syllabus concept lives</h3>
<p>This table is the book's index of concepts against their homes in the system. Use it to check coverage
and to find the example for a topic you are revising.</p>
""")

B21.append(table(
  ["Syllabus concept", "Where it is taught", "Where it lives in BasinWatch"],
  [
    ["Classes, objects, encapsulation", "Ch. 2", "<span class='mono'>BasinZone</span> — private state, package-private behaviour"],
    ["Interfaces", "Ch. 2", "<span class='mono'>BasinEvent</span>, implemented by three records"],
    ["Polymorphism", "Ch. 2", "<span class='mono'>BasinModel.process</span> pattern matching"],
    ["Inheritance", "Ch. 2", "<span class='mono'>SensorFeed extends Thread</span>, Swing panels"],
    ["Enums", "Ch. 2", "<span class='mono'>RiskLevel</span>, <span class='mono'>MissionType</span>, <span class='mono'>ResourceType</span>"],
    ["Records", "Ch. 2", "<span class='mono'>SensorReading</span>, <span class='mono'>ZoneSnapshot</span>, <span class='mono'>DatabaseHistoryEntry</span>"],
    ["POJO versus JavaBean", "Ch. 2, 18", "Records and serializable DTOs; no framework beans"],
    ["Threads and Runnable", "Ch. 3, 7", "<span class='mono'>SensorFeed</span>, <span class='mono'>SensorIntake</span>, three workers"],
    ["Synchronization and monitors", "Ch. 3", "<span class='mono'>ResourceAllocator.tryReserve</span>, <span class='mono'>BasinModel.process</span>"],
    ["wait / notifyAll", "Ch. 3, 7", "<span class='mono'>EventBuffer.put</span> and <span class='mono'>take</span>"],
    ["Producer–consumer", "Ch. 3, 7", "Feed produces, intake consumes, workers process"],
    ["Interruption and joining", "Ch. 7", "<span class='mono'>closeEngine</span> shutdown sequence"],
    ["Byte streams", "Ch. 4, 6", "Sensor archive via <span class='mono'>DataOutputStream</span>"],
    ["Character streams", "Ch. 4, 5", "Journal, reports, and the pipe"],
    ["FileInputStream / FileOutputStream", "Ch. 5", "The classic API, contrasted with <span class='mono'>Files.newXxx</span>"],
    ["FileReader / FileWriter", "Ch. 5", "The classic character API, contrasted with <span class='mono'>Files.newBufferedReader</span>"],
    ["ByteArrayInputStream / ByteArrayOutputStream", "Ch. 7", "Demonstrated as the in-memory case"],
    ["Piped streams", "Ch. 7", "<span class='mono'>PipedWriter</span> / <span class='mono'>PipedReader</span> between feed and intake"],
    ["Buffered streams", "Ch. 6", "Every file stream in the project is wrapped"],
    ["DataInputStream / DataOutputStream", "Ch. 6", "<span class='mono'>SensorArchive</span>"],
    ["Serialization", "Ch. 8", "<span class='mono'>SnapshotStore</span> with <span class='mono'>ObjectOutputStream</span>"],
    ["Deserialization safety", "Ch. 8", "Size bound, class filter, version check, validation"],
    ["File metadata and exceptions", "Ch. 5", "<span class='mono'>SaveCatalog.list</span>, <span class='mono'>EOFException</span> handling"],
    ["JDBC architecture", "Ch. 11", "<span class='mono'>DatabaseManager</span> and the driver"],
    ["Driver types", "Ch. 11", "SQLite's pure-Java type 4 driver"],
    ["Connection", "Ch. 12", "<span class='mono'>DatabaseManager.openConnection</span>"],
    ["Statement", "Ch. 12", "<span class='mono'>DatabaseInitializer</span> DDL"],
    ["PreparedStatement", "Ch. 12", "Every repository insert and query"],
    ["CallableStatement", "Ch. 12", "Taught; not used — no stored procedures"],
    ["ResultSet", "Ch. 12", "<span class='mono'>OperationalEventRepository.loadRecent</span>"],
    ["CRUD", "Ch. 12", "Insert, select and update; delete is deliberately absent"],
    ["Transactions", "Ch. 13", "<span class='mono'>DatabaseService.recordDispatch</span>"],
    ["SQLException handling", "Ch. 12, 14", "Caught in <span class='mono'>enqueue</span>, reported to the UI"],
    ["Swing components and layouts", "Ch. 15", "<span class='mono'>MainFrame</span>, <span class='mono'>BasinMapPanel</span>"],
    ["Events and listeners", "Ch. 15", "Action listeners throughout the frame"],
    ["Custom painting", "Ch. 15", "<span class='mono'>BasinMapPanel.paintComponent</span>"],
    ["Event-dispatch thread", "Ch. 15, 16", "Every listener and every <span class='mono'>invokeLater</span> call"],
    ["JDBC to Swing", "Ch. 16", "<span class='mono'>DatabaseHistoryPanel</span> and its table model"],
    ["Maven and pom.xml", "Ch. 17", "<span class='mono'>pom.xml</span> and the shade plugin"],
    ["XML and namespaces", "Ch. 18", "<span class='mono'>pom.xml</span> header; taught, not otherwise used"],
    ["XML Schema", "Ch. 18", "Taught; not used in the project"],
    ["Annotations", "Ch. 18", "<span class='mono'>@Override</span>, <span class='mono'>@FunctionalInterface</span>, <span class='mono'>@SuppressWarnings</span>"],
    ["JavaBeans", "Ch. 18", "Taught; the project wires by hand"],
    ["Spring JdbcTemplate", "Ch. 19", "Taught as an alternative; the project uses raw JDBC"],
    ["DriverManagerDataSource", "Ch. 19", "Taught; the project uses <span class='mono'>DriverManager</span> directly"],
  ],
  caption="<b>Table 21.1</b> — Every syllabus concept, where it is taught, and where it lives in the project."))

B21.append("""
<h3><span class=\"n\">21.4</span>The eight questions</h4>
<p>Work through these for a class of your choosing. If you can answer all eight without looking, you
understand that class and its place in the system.</p>
""")

B21.append(exercise(1, "Why is this class needed?",
"<p>State the responsibility in one sentence, then say what would go wrong if the class did not exist. The second part is the one that shows understanding: \u201cthe model would have to validate input\u201d or \u201cthe interface would have to know SQL\u201d is a real answer; \u201cit is a class that does X\u201d is not.</p>"))

B21.append(exercise(2, "How does it communicate with other classes?",
"<p>List the constructor arguments and the methods it calls on them. Name the mechanism for each — method call, stream, callback, queue, query. Note the classes it does <i>not</i> reference, because those absences are also design decisions.</p>"))

B21.append(exercise(3, "Which data does it receive?",
"<p>Give the types and the shape. \u201cA line of pipe-delimited text with six fields\u201d is a better answer than \u201ca string\u201d, because it explains why the parse validates what it validates.</p>"))

B21.append(exercise(4, "Does it use a stream, an event, a method call, or a database query?",
"<p>Answer with all that apply, and say why each is the right mechanism. If the answer is \u201cnone of them\u201d, explain what mechanism it does use instead — an in-memory collection, a monitor, a future.</p>"))

B21.append(exercise(5, "How does its result affect the application?",
"<p>Trace forward to the visible effect. A method that returns a boolean may ultimately change a colour on a map, and being able to say so is the difference between knowing a class and knowing a system.</p>"))

B21.append(exercise(6, "What survives application shutdown?",
"<p>Answer for each artefact: nothing, an audit record, a typed measurement, or a restorable snapshot. Then say which component is responsible for writing it — it will rarely be the class you started with.</p>"))

B21.append(exercise(7, "What happens if the relevant operation fails?",
"<p>Distinguish recoverable from unrecoverable, and reported from propagated. A class that skips a bad record and one that aborts the loop are making different assumptions about what failure means.</p>"))

B21.append(exercise(8, "Which design alternative is taught in the lecture notes?",
"<p>Name the textbook version and say precisely what differs. \u201cThe lecture version reads a file in main; this version reads a pipe on a background thread\u201d is the shape of a good answer, because it explains why the extra machinery exists.</p>"))

B21.append("""
<h3><span class=\"n\">21.5</span>Three design alternatives worth being able to argue</h3>
<p>An examiner who wants to know whether you understand a design will ask what you would do differently.
These are the three most likely, with both sides of the argument.</p>
""")

B21.append(table(
  ["Choice in BasinWatch", "The alternative", "Argument for the alternative", "Argument for what the project does"],
  [
    ["Raw JDBC with hand-written repositories",
     "Spring JdbcTemplate with a DataSource",
     "Less boilerplate per query; declarative transactions; pooling available",
     "One dependency instead of four; the JDBC mechanics remain visible; appropriate for a dozen queries"],
    ["One file per artefact, no database by default",
     "Store everything in the database",
     "One mechanism, one query language, consistent access",
     "The application works with no database at all; the log is readable without tooling; the snapshot restores state that a row store would need replay for"],
    ["Hand-written constructor wiring",
     "A dependency-injection framework",
     "Wiring is declarative; large graphs become manageable; lifecycles are managed",
     "Wiring is visible in the source; a missing dependency is a compile error rather than a runtime one; no scanning, no reflection, no framework start-up"],
  ],
  caption="<b>Table 21.2</b> — Three design choices, and the case for each side."))

B21.append(core("""<p>The point of that table is not that one column is right. It is that a design
choice can be defended with reasons. In a viva, saying \u201cI used raw JDBC because the project has one
database and a dozen queries, and adding Spring would add four dependencies to save perhaps forty
lines\u201d is a far stronger answer than \u201cthe lecture notes used JDBC\u201d.</p>"""))

B21.append("""
<h3><span class=\"n\">21.6</span>What you should now be able to do</h3>
<ul>
<li><b>Draw the architecture from memory</b>, with the layers, the threads and the two persistence
columns.</li>
<li><b>Name the mechanism</b> for any interaction in the system: method call, monitor, stream, queue,
callback or query.</li>
<li><b>Trace four scenarios</b> end to end, saying which thread runs each step.</li>
<li><b>Choose a stream</b> for a task and justify the layers, including the charset and the buffering.</li>
<li><b>Explain why serialization needs four defences</b>, and name them.</li>
<li><b>Write a parameterized query</b> with correct 1-based binding and complete resource handling, and say
why binding beats concatenation.</li>
<li><b>Say what a transaction guarantees</b> and identify the one place the project needs one.</li>
<li><b>Keep the event-dispatch thread free</b>, and explain what happens when you do not.</li>
<li><b>Explain how the JDBC driver reaches the classpath</b>, and why the shade transformer matters.</li>
<li><b>Distinguish raw JDBC from JdbcTemplate</b> without claiming the project uses both.</li>
<li><b>Answer the eight questions</b> about any class in the project.</li>
</ul>
""")

B21.append(connect("""<p>The revision section that follows turns each of those capabilities into
comparison tables, viva questions and tracing exercises. Work through Chapter 21 first; then use the
revision material to check what you missed.</p>"""))

B21.append(summary([
  "The eight questions — purpose, communication, data received, mechanism, effect, survival, failure, and the lecture alternative — explain any class in the system.",
  "Every syllabus concept has a home in the project; Table 21.1 maps all of them.",
  "The three most defensible design alternatives are raw JDBC versus JdbcTemplate, files versus a database, and hand wiring versus a DI framework.",
  "A design choice is worth defending with reasons, not with a reference to the lecture notes.",
]))

B21.append(keyterms([
  "<b>Design alternative</b> — a different but defensible way of achieving the same requirement.",
  "<b>Traceability</b> — the ability to follow a piece of data from its origin to its visible effect.",
  "<b>Responsibility</b> — the single job a class exists to do.",
]))

B21.append("</div>")

HTML = "".join(P + B20 + B21)
