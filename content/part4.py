"""PART IV — Swing and the User Interface.  Chapters 15-16."""
from . import *

P = []
B15, B16 = [], []

P.append("""
<div class="part-page">
  <div class="pnum">PART IV</div>
  <h1>Swing and the User Interface</h1>
  <div class="prule"></div>
  <div class="pintro">An interface is not a drawing of the model; it is a set of listeners, a
  component tree and a repaint loop, all of which must share exactly one thread. This part explains
  Swing from containers outward, walks through the lecture-note login application, and then shows how
  BasinWatch connects a click to a database query and back to a visible table.</div>
  <div class="chapters">
    <div><span>15</span>Swing Fundamentals and Event-Driven Programming</div>
    <div><span>16</span>Connecting Application Logic, JDBC and Swing</div>
  </div>
</div>
""")

# ======================================================================
# CHAPTER 15
# ======================================================================
B15.append(chapter(15, "Swing Fundamentals and Event-Driven Programming",
"Containers, components, layouts, listeners and events — and the lecture-note login application explained line by line."))

B15.append("""
<h3><span class="n">15.1</span>What makes a program event-driven?</h3>
<p>A procedural program runs from top to bottom: it reads input, computes, prints output, and exits. A
graphical program does none of that. It starts, builds a window, and then <i>waits</i>. Everything that
happens afterwards happens because something triggered it — a click, a key press, a timer, a window
being resized.</p>

<p>The structure that makes this work is a loop that never ends and a set of callbacks that the loop
invokes. In Swing, that loop lives on a dedicated thread called the <b>event-dispatch thread</b>, and
every listener you register runs on it.</p>
""")

B15.append(defbox("Event-driven programming",
"a style in which the program declares handlers for events and then waits, letting the framework invoke the appropriate handler when each event occurs, rather than controlling the sequence of execution itself."))

B15.append(core("""<p>Three consequences follow from the event-driven model, and they explain almost
every Swing rule in this chapter.</p>
<ol>
<li><b>You do not control the order of execution.</b> The user does.</li>
<li><b>All event handling and all painting happen on one thread.</b> So any long operation inside a
handler freezes the entire interface.</li>
<li><b>Components must be updated from that thread.</b> Touching a Swing component from another thread
is unsafe.</li>
</ol>"""))

B15.append("""
<h3><span class="n">15.2</span>Containers and components</h3>
<p>Swing's class hierarchy separates things that hold other things from things that display
something.</p>
""")

B15.append(table(
  ["Category", "Base class", "Examples", "Role"],
  [
    ["Top-level container", "<span class='mono'>JFrame</span>, <span class='mono'>JDialog</span>",
     "<span class='mono'>JFrame</span>", "A real operating-system window with a title bar and close button"],
    ["Intermediate container", "<span class='mono'>JPanel</span>, <span class='mono'>JScrollPane</span>, <span class='mono'>JSplitPane</span>",
     "<span class='mono'>JPanel</span>, <span class='mono'>JScrollPane</span>", "Groups and arranges other components; invisible itself"],
    ["Simple component", "<span class='mono'>JComponent</span>",
     "<span class='mono'>JButton</span>, <span class='mono'>JLabel</span>, <span class='mono'>JTable</span>, <span class='mono'>JComboBox</span>, <span class='mono'>JSlider</span>",
     "Displays something or accepts input"],
  ],
  caption="<b>Table 15.1</b> — The three categories of Swing class."))

B15.append(distinct("""<p><b>A <span class='mono'>JFrame</span> is a window; a
<span class='mono'>JPanel</span> is not.</b> You cannot add a <span class='mono'>JPanel</span> to
another window's title bar, and a <span class='mono'>JPanel</span> has no close button. Confusing the
two is behind a large share of beginner layout problems: the top-level container is the window, and
everything else is arranged <i>inside</i> its content pane.</p>"""))

B15.append(figure("d19_swing_component_tree", "21", "The Swing component tree",
"A JFrame containing a toolbar, a central split pane, and a status bar. The split pane holds the map panel on the left and a tabbed panel on the right. Each node is a real component class.",
"portrait"))

B15.append("""
<h3><span class="n">15.3</span>Layout managers</h3>
<p>Swing does not use absolute coordinates. Instead, each container has a layout manager that decides
where its children go. This is why a Swing window resizes sensibly rather than leaving controls
stranded.</p>
""")

B15.append(table(
  ["Layout", "Arrangement", "Best for", "Characteristic"],
  [
    ["<span class='mono'>BorderLayout</span>", "Five regions: NORTH, SOUTH, EAST, WEST, CENTER",
     "The overall frame — toolbar on top, status bar at the bottom, content in the centre",
     "CENTER takes all remaining space; the other four take their preferred size"],
    ["<span class='mono'>FlowLayout</span>", "Left to right, wrapping to the next line",
     "A row of buttons or controls", "The default for <span class='mono'>JPanel</span>"],
    ["<span class='mono'>GridLayout</span>", "A fixed grid of equal-sized cells",
     "A keypad, or a uniform form", "Every cell is the same size"],
    ["<span class='mono'>BoxLayout</span>", "A single row or column",
     "Stacking controls vertically", "Use <span class='mono'>Box.createVerticalStrut</span> for spacing"],
    ["<span class='mono'>GridBagLayout</span>", "A grid with per-component constraints",
     "Complex forms that must align precisely",
     "Powerful and verbose; needs a <span class='mono'>GridBagConstraints</span> per component"],
  ],
  caption="<b>Table 15.2</b> — The common layout managers."))

B15.append(practice("""<p>BasinWatch's main frame uses <span class='mono'>BorderLayout</span> for the
window and nested containers inside it, which is the standard composition:</p>
<pre class="long">setLayout(<span class="kw">new</span> <span class="ty">BorderLayout</span>(8, 8));
add(buildToolbar(), <span class="ty">BorderLayout</span>.NORTH);
add(buildStatusBar(), <span class="ty">BorderLayout</span>.SOUTH);
<span class="ty">JSplitPane</span> split = <span class="kw">new</span> <span class="ty">JSplitPane</span>(<span class="ty">JSplitPane</span>.HORIZONTAL,
        mapPanel, rightPanel);
split.setResizeWeight(0.45);
add(split, <span class="ty">BorderLayout</span>.CENTER);</pre>
<div class="codecap"><b>Listing 15.1</b> — from BasinWatch, <span class="mono">app/MainFrame.java</span></div>
<p>Read the composition: the window is a border layout, the toolbar and status bar take the fixed north
and south regions, and the split pane fills the centre. The split pane divides the centre horizontally,
giving 45 per cent of extra space to the map when the window is resized.</p>"""))

B15.append(screenshot("shot_operations_tab", "S3", "The Operations tab, showing a completed field response",
"The panel on the right is a <span class='mono'>JTabbedPane</span>; this is its second card. "
"The heading reads <i>Field operations</i> with the note <i>Assigned work advances with observation "
"intervals</i>, and the list below shows mission <span class='mono'>BW-0001 · Deploy portable pump</span> "
"against zone <span class='mono'>MAR</span> with status <i>Completed</i>. That mission row is the "
"end of a real chain: a click on the <i>Dispatch response</i> button became a "
"<span class='mono'>DispatchRequest</span> event, which the engine accepted, processed on the next "
"tick, and wrote to SQLite as a single transaction across the <span class='mono'>missions</span>, "
"<span class='mono'>resource_usage</span> and <span class='mono'>operational_events</span> tables "
"(Chapter 13). The zone cards on the left are "
"unchanged by the tab switch — they belong to the map panel, which is outside the tabbed pane.",
"landscape"))

B15.append("""
<h3><span class="n">15.4</span>Events and listeners</h3>
<p>An event is an object describing something that happened. A listener is an object that wants to be
told. Registering a listener connects the two.</p>
""")

B15.append(table(
  ["Listener interface", "Method", "Triggered by", "Event object carries"],
  [
    ["<span class='mono'>ActionListener</span>", "<span class='mono'>actionPerformed(ActionEvent)</span>",
     "A button click, a menu item, pressing Enter in a field", "The source component and an action command string"],
    ["<span class='mono'>MouseListener</span>",
     "<span class='mono'>mouseClicked</span>, <span class='mono'>mousePressed</span>, <span class='mono'>mouseReleased</span>, <span class='mono'>mouseEntered</span>, <span class='mono'>mouseExited</span>",
     "Mouse activity over a component", "The x/y position and which button"],
    ["<span class='mono'>MouseMotionListener</span>", "<span class='mono'>mouseMoved</span>, <span class='mono'>mouseDragged</span>",
     "Movement, with no click", "The x/y position"],
    ["<span class='mono'>KeyListener</span>", "<span class='mono'>keyTyped</span>, <span class='mono'>keyPressed</span>, <span class='mono'>keyReleased</span>",
     "Keyboard input when the component has focus", "The key code and character"],
    ["<span class='mono'>WindowListener</span>", "<span class='mono'>windowClosing</span>, <span class='mono'>windowClosed</span>, …",
     "Window lifecycle", "The window and its new state"],
    ["<span class='mono'>ChangeListener</span>", "<span class='mono'>stateChanged(ChangeEvent)</span>",
     "A slider or tab selection changing", "The source component"],
    ["<span class='mono'>ListSelectionListener</span>", "<span class='mono'>valueChanged(ListSelectionEvent)</span>",
     "A row or list item being selected", "Whether the change is still adjusting"],
  ],
  caption="<b>Table 15.3</b> — The listeners you meet most often."))

B15.append(figure("d20_swing_event_flow", "22", "Swing event handling flow",
"The user's click is delivered to the event-dispatch thread, which dispatches it to every listener registered on the source component. The listener runs its handler on that same thread. Painting is also requested through the same thread, so the handler must return quickly.",
"landscape"))

B15.append("""
<h3><span class="n">15.5</span>The three ways to write a listener</h3>
<p>Java gives you several idioms for the same thing, and each is appropriate in a different
situation.</p>
""")

B15.append(code('''// (1) A separate named class — best when the handler is substantial or reused
final class ExportHandler implements ActionListener {
    private final BasinEngine engine;
    ExportHandler(BasinEngine engine) { this.engine = engine; }
    @Override public void actionPerformed(ActionEvent event) {
        engine.exportReport();
    }
}
button.addActionListener(new ExportHandler(engine));

// (2) An anonymous inner class — the classic style in older Swing code
button.addActionListener(new ActionListener() {
    @Override public void actionPerformed(ActionEvent event) {
        engine.exportReport();
    }
});

// (3) A lambda — correct when the interface has one abstract method
button.addActionListener(event -> engine.exportReport());

// (4) A method reference — when the handler is already a method
button.addActionListener(this::onExportRequested);''', "illustrative — four listener idioms"))

B15.append(core("""<p>All four compile to the same thing. A lambda works because
<span class='mono'>ActionListener</span> is a <b>functional interface</b>: it declares exactly one
abstract method, so the compiler can infer the implementation. This is why Swing code written after
Java 8 is markedly shorter than older examples, and why the anonymous-class form you may see in lecture
notes is now mostly historical.</p>"""))

B15.append("""
<h3><span class="n">15.6</span>The lecture-note login application</h3>
<p>The lecture notes contain a Swing login screen. It is a small program, but it demonstrates most of
the fundamentals at once, so it is worth walking through carefully.</p>
""")

B15.append(figure("d21_login_example", "23", "The lecture-note login application",
"The login frame: a username field, a password field, a login button and a status label, arranged in a grid inside a border layout. The annotated flow shows the button's ActionListener reading both fields and comparing them against the expected credentials.",
"portrait"))

B15.append(code('''import javax.swing.*;
import java.awt.*;

public class LoginApplication {
    private final JFrame frame = new JFrame("Login");
    private final JTextField usernameField = new JTextField(16);
    private final JPasswordField passwordField = new JPasswordField(16);
    private final JButton loginButton = new JButton("Login");
    private final JLabel statusLabel = new JLabel("Enter your credentials", SwingConstants.CENTER);

    public LoginApplication() {
        JPanel form = new JPanel(new GridLayout(2, 2, 8, 8));
        form.add(new JLabel("Username:"));
        form.add(usernameField);
        form.add(new JLabel("Password:"));
        form.add(passwordField);

        JPanel content = new JPanel(new BorderLayout(8, 8));
        content.setBorder(BorderFactory.createEmptyBorder(12, 12, 12, 12));
        content.add(form, BorderLayout.CENTER);
        content.add(loginButton, BorderLayout.SOUTH);
        content.add(statusLabel, BorderLayout.NORTH);

        loginButton.addActionListener(event -> attemptLogin());

        frame.setContentPane(content);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.pack();
        frame.setLocationRelativeTo(null);          // centre on screen
        frame.setVisible(true);
    }

    private void attemptLogin() {
        String username = usernameField.getText().trim();
        char[] password = passwordField.getPassword();
        if (username.isEmpty() || password.length == 0) {
            statusLabel.setText("Both fields are required.");
            return;
        }
        if ("admin".equals(username) && "secret".equals(new String(password))) {
            statusLabel.setText("Welcome, " + username + ".");
        } else {
            statusLabel.setText("Incorrect username or password.");
            passwordField.setText("");              // clear the password on failure
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(LoginApplication::new);
    }
}''', "lecture-note style — the Swing login application, annotated"))

B15.append("""
<h3><span class="n">15.7</span>What the login program actually does</h3>

<p><b>It builds a component tree.</b> A <span class="mono">GridLayout</span> panel holds two label and
field pairs. That panel sits in the centre of a border layout, with the button below and the status
label above. Nothing is positioned by coordinates.</p>

<p><b>It registers one listener.</b> The button's action listener calls
<span class="mono">attemptLogin()</span>. That is the only connection between the user and the
logic.</p>

<p><b>It validates before comparing.</b> An empty username or password produces a specific message,
which is more useful than "incorrect credentials". This is the same validate-at-the-boundary habit as
<span class="mono">SensorReading.parse</span>.</p>

<p><b>It reads the password as a <span class="mono">char[]</span>, not a
<span class="mono">String</span>.</b> That is not stylistic.
<span class="mono">JPasswordField.getPassword()</span> returns a character array precisely so that the
caller can overwrite it when finished. A <span class="mono">String</span> is immutable and its contents
may persist in memory until garbage collection, so a password held in a
<span class="mono">String</span> is readable from a memory dump for longer than necessary.</p>

<p><b>It clears the password on failure.</b> A small detail with a real security purpose: the credential
is not left on screen for someone walking past.</p>

<p><b>It starts on the event-dispatch thread.</b> <span class="mono">main</span> does nothing but
schedule the constructor with <span class="mono">SwingUtilities.invokeLater</span>. Every component is
therefore created on the EDT, which is the rule.</p>
""")

B15.append(clarify("""<p><b>This program checks a hard-coded credential in the client.</b> That is fine
for a demonstration of Swing mechanics and unacceptable for a real system, for three reasons. The
password appears in the compiled code. There is no hashing, so anyone reading the class file learns the
credential. And any check performed in the user interface can be bypassed by anyone who can run
different code. A real login compares a <i>hash</i> of the submitted password against a stored hash, and
it does so on a server the user does not control. The lecture example is a UI exercise, not a security
pattern — and saying so is part of understanding it.</p>"""))

B15.append(mistake("""<p>Calling <span class='mono'>new LoginApplication()</span> directly from
<span class='mono'>main</span> instead of through
<span class='mono'>SwingUtilities.invokeLater</span>. It often appears to work, because the components
happen to be created before the window is shown. But Swing's internals assume single-threaded access,
and creating components off the EDT can produce intermittent, hard-to-reproduce failures in layout or
painting. The fix is one line, and it is not optional.</p>"""))

B15.append("""
<h3><span class="n">15.8</span>Custom painting</h3>
<p>When a component must draw something Swing does not provide — a schematic map, for instance — you
override <span class="mono">paintComponent</span>.</p>
""")

B15.append(code('''@Override
protected void paintComponent(Graphics graphics) {
    super.paintComponent(graphics);              // always first: clears and paints the background
    Graphics2D g = (Graphics2D) graphics;
    g.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
            RenderingHints.VALUE_ANTIALIAS_ON);
    for (ZoneSnapshot zone : snapshot.zones()) {
        Point centre = positionOf(zone.id());
        g.setColor(colourFor(zone.risk()));
        g.fillOval(centre.x - RADIUS, centre.y - RADIUS, RADIUS * 2, RADIUS * 2);
        g.setColor(Color.WHITE);
        g.drawString(zone.id(), centre.x - 12, centre.y + 4);
    }
}''', "from BasinWatch, app/BasinMapPanel.java — custom painting, condensed."))

B15.append("""
<p>Three rules govern <span class="mono">paintComponent</span>, and all three matter.</p>

<p><b>Call <span class="mono">super.paintComponent</span> first.</b> It clears the component's area.
Without it, previous frames are never erased and the drawing smears as the component is repainted.</p>

<p><b>Never perform slow work inside it.</b> Painting runs on the event-dispatch thread, and it runs
whenever the window is uncovered, resized or asked to repaint. Reading a file or running a query here
would freeze the interface repeatedly.</p>

<p><b>Never call <span class="mono">repaint()</span> from inside it.</b> That requests another paint,
which requests another repaint, producing an unresponsive loop. To change what is drawn, change the data
and then call <span class="mono">repaint()</span> from elsewhere.</p>
""")

B15.append(connect("""<p>This is why the engine publishes immutable snapshots. The paint method reads
<span class='mono'>snapshot</span> on the event-dispatch thread while workers may be mutating the model
on other threads. Because the snapshot is an immutable copy, the paint method sees a consistent picture
with no locking at all.</p>"""))

B15.append(exam("""<p>A very common question asks why a long-running task in an
<span class='mono'>ActionListener</span> freezes the interface. The complete answer: the handler runs on
the event-dispatch thread, and that same thread is responsible for delivering subsequent events and
performing all painting. While the handler is busy, neither can happen, so the window appears frozen
even though the application is running. The fix is to move the work to a background thread and post the
result back — the subject of Chapter 16.</p>"""))

B15.append(summary([
  "Swing is event-driven: the program declares handlers and then waits for the framework to call them.",
  "Components fall into top-level containers, intermediate containers and simple components.",
  "Layout is managed by a layout manager per container; BorderLayout for the frame with nested layouts inside it is the standard composition.",
  "Events are dispatched to registered listeners, and all event handling runs on the event-dispatch thread.",
  "A listener can be a named class, an anonymous class, a lambda or a method reference; lambdas work because the listener interfaces are functional.",
  "The lecture-note login application validates input, reads the password as a char array, clears it on failure, and starts on the EDT.",
  "Custom painting goes in paintComponent, must call super first, must be fast, and must never call repaint.",
  "A hard-coded credential check in a UI is a demonstration of mechanics, not a security design.",
]))

B15.append(keyterms([
  "<b>Event-dispatch thread (EDT)</b> — the single thread that runs Swing event handling and painting.",
  "<b>Listener</b> — an object registered to be notified when a particular event occurs.",
  "<b>Functional interface</b> — an interface with exactly one abstract method, so a lambda can implement it.",
  "<b>Layout manager</b> — the object that decides where a container's children are placed.",
  "<b>paintComponent</b> — the method overridden to draw a custom component.",
]))

B15.append("</div>")

# ======================================================================
# CHAPTER 16
# ======================================================================
B16.append(chapter(16, "Connecting Application Logic, JDBC and Swing",
"From a click to a command, through a background thread and a database query, back to a visible table — and the one thread rule that governs all of it."))

B16.append("""
<h3><span class="n">16.1</span>The problem this chapter solves</h3>
<p>Chapter 15 established that all Swing work happens on the event-dispatch thread. Chapter 12
established that a database query is a blocking operation. Put those two facts together and you have a
conflict: running the query in a listener freezes the window.</p>

<p>This chapter is about resolving that conflict without introducing a worse one. The solution has four
parts, and each is a rule rather than a trick.</p>
""")

B16.append(core("""<ol>
<li><b>A listener does not do the work.</b> It asks the engine for an operation and returns.</li>
<li><b>Slow work happens on a background thread.</b> The engine's executors own those threads.</li>
<li><b>The result is delivered as a future.</b> A callback runs when the value arrives.</li>
<li><b>The callback posts to the EDT before touching any component.</b> Every time, without
exception.</li>
</ol>"""))

B16.append("""
<h3><span class="n">16.2</span>Step one: the listener asks, and returns</h3>
<p>BasinWatch's listeners are short by design. Each one translates a user gesture into an engine call
and nothing else.</p>
""")

B16.append(code('''startButton.addActionListener(event -> {
    if (engine.isRunning()) {
        engine.pause();
    } else {
        engine.start();
    }
    refreshControlStates();
});

stepButton.addActionListener(event -> engine.step());
stormButton.addActionListener(event -> engine.injectStorm(1.35, 0.42));
reportButton.addActionListener(event -> engine.exportReport());
saveButton.addActionListener(event -> chooseAndSave());
refreshHistoryButton.addActionListener(event -> historyPanel.reload());''',
"from BasinWatch, app/MainFrame.java and app/DatabaseHistoryPanel.java — six listeners, all of them short."))

B16.append("""
<p>None of those handlers opens a file, runs a query or waits for anything. That is the point. A
listener that returns quickly cannot freeze the interface, and the method names read like the operations
the user is actually performing.</p>
""")

B16.append("""
<h3><span class="n">16.3</span>Step two: the engine runs the work elsewhere</h3>
<p>The engine decides which thread performs an operation. Several executors and named threads are
involved, and each exists for a reason.</p>
""")

B16.append(table(
  ["Thread", "Created by", "Runs", "Why it is separate"],
  [
    ["<span class='mono'>\"event-dispatch\"</span>", "Swing", "Event handling and painting", "Swing requires it"],
    ["<span class='mono'>\"basin-sensor-feed\"</span>", "<span class='mono'>SensorFeed extends Thread</span>",
     "The emission loop and its timed sleep", "It must be interruptible and joinable"],
    ["<span class='mono'>\"basin-sensor-intake\"</span>", "The engine, from a <span class='mono'>Runnable</span>",
     "Reading and validating pipe lines", "It blocks on <span class='mono'>readLine()</span>"],
    ["<span class='mono'>\"basin-response-1..3\"</span>", "A fixed thread pool",
     "Applying events to the model", "Processing is concurrent and CPU-bound"],
    ["<span class='mono'>\"basin-sensor-archive\"</span>", "A single-thread executor",
     "Appending typed records to the archive", "Disk writes must be serialised"],
    ["<span class='mono'>\"basin-control\"</span>", "A single-thread executor",
     "Save, restore and report generation", "Only one control operation at a time"],
    ["<span class='mono'>\"basin-database\"</span>", "A single-thread executor",
     "All JDBC work", "One writer, so no isolation anomalies"],
  ],
  caption="<b>Table 16.1</b> — The threads in the application and why each is separate."))

B16.append(visual("""<p>Count the threads and note that only one of them may touch Swing. Every other
row in that table describes work that would freeze the window if it ran on the event-dispatch thread —
a blocking read, a disk write, a database round trip, a computation over hundreds of events.</p>"""))

B16.append("""
<h3><span class="n">16.4</span>Step three: the result arrives as a future</h3>
<p>An operation that produces a result returns a <span class="mono">CompletableFuture</span>. The caller
attaches a callback and carries on.</p>
""")

B16.append(code('''public CompletableFuture<Path> exportReport() {
    return CompletableFuture.supplyAsync(() -> {
        try {
            BasinSnapshot snapshot = model.snapshot();
            Path report = ReportWriter.write(AppPaths.reportsDirectory(), snapshot);
            publishStatus("Report written to " + report.getFileName());
            return report;
        } catch (IOException ex) {
            publishStatus("Could not write the report: " + ex.getMessage());
            throw new CompletionException(ex);
        }
    }, controlExecutor);
}''', "from BasinWatch, engine/BasinEngine.java — the work is supplied to an executor; the caller gets a future."))

B16.append("""
<p>Three properties of that method are the pattern.</p>

<p><b>The work is a supplier submitted to a named executor.</b>
<span class="mono">supplyAsync(..., controlExecutor)</span> runs on
<span class="mono">"basin-control"</span>, not on the caller's thread and not on the common pool.</p>

<p><b>Failures are converted.</b> <span class="mono">IOException</span> is checked, and a supplier
cannot throw it, so it is wrapped in <span class="mono">CompletionException</span>. The future then
completes exceptionally, and any <span class="mono">whenComplete</span> callback can inspect the
cause.</p>

<p><b>The status is published from the worker thread.</b> <span class="mono">publishStatus</span> is
called inside the supplier, so it runs on the control thread. The listener that receives it must hop to
the EDT — which brings us to step four.</p>
""")

B16.append("""
<h3><span class="n">16.5</span>Step four: the callback posts to the EDT</h3>
<p>This is the rule that everything else depends on.</p>
""")

B16.append(code('''// Registering a listener: the engine may call it from ANY thread
engine.addStatusListener(message ->
        SwingUtilities.invokeLater(() -> statusLabel.setText(message)));

// Attaching a callback to a future: it runs on the completing thread
engine.loadHistory(200).whenComplete((entries, failure) ->
        SwingUtilities.invokeLater(() -> {
            if (failure != null) {
                historyStatus.setText("History unavailable: " + failure.getMessage());
                return;
            }
            historyTableModel.setEntries(entries);
            historyStatus.setText(entries.size() + " entries loaded.");
        }));''', "from BasinWatch, app/MainFrame.java and app/DatabaseHistoryPanel.java — every callback hops to the EDT."))

B16.append(core("""<p>Notice that <span class='mono'>SwingUtilities.invokeLater</span> appears in both
places, and in exactly the same position: <i>wrapping the entire body that touches a component</i>.
That is the rule stated precisely. It is not enough to call it somewhere in the method — the component
access must be inside the lambda that is posted.</p>"""))

B16.append(distinct("""<p><b><span class='mono'>invokeLater</span> and
<span class='mono'>invokeAndWait</span> are different, and one of them is dangerous.</b>
<span class='mono'>invokeLater</span> queues the runnable on the EDT and returns immediately — the
calling thread continues. <span class='mono'>invokeAndWait</span> queues it and blocks until the EDT has
run it, which is a deadlock if you call it <i>from</i> the EDT. BasinWatch uses
<span class='mono'>invokeLater</span> exclusively.</p>"""))

B16.append("""
<h3><span class="n">16.6</span>The complete path, from click to table cell</h3>
<p>Now the two halves of the book can be joined. Here is the whole path for one user action: pressing
"Refresh" in the history panel.</p>
""")

B16.append(figure("d27_end_to_end_sequence", "24", "The complete path from a click to a table cell",
"Fourteen numbered steps crossing four threads: the event-dispatch thread dispatches the click, the database thread runs the query and completes the future, and the callback posts back to the event-dispatch thread to update the table model.",
"portrait"))

B16.append(trace("From a button press to a populated table", [
  "<b>The user clicks Refresh.</b> The operating system delivers a mouse event to the window.",
  "<b>The EDT dispatches it.</b> Swing calls the <span class='mono'>ActionListener</span> registered on that button.",
  "<b>The listener calls one method.</b> <span class='mono'>historyPanel.reload()</span> — and returns immediately.",
  "<b>reload asks the engine for a future.</b> <span class='mono'>engine.loadHistory(200)</span> returns a <span class='mono'>CompletableFuture</span> at once.",
  "<b>The engine checks availability.</b> If the database is unavailable it returns an already-completed future holding an empty list, so no error path is needed.",
  "<b>The engine enqueues the query.</b> A lambda is submitted to the single-threaded database executor.",
  "<b>The database thread opens a connection.</b> <span class='mono'>DatabaseManager.openConnection()</span> on <span class='mono'>basin-database</span>.",
  "<b>The repository prepares and binds.</b> A <span class='mono'>PreparedStatement</span> with one placeholder for the limit.",
  "<b>SQLite executes.</b> The query is planned and the matching rows are returned in descending time order.",
  "<b>The rows are mapped to objects.</b> Each row becomes a <span class='mono'>DatabaseHistoryEntry</span>, inside the result-set loop.",
  "<b>The future completes on the database thread.</b> <span class='mono'>future.complete(entries)</span> runs the <span class='mono'>whenComplete</span> callback on that same thread.",
  "<b>The callback posts to the EDT.</b> <span class='mono'>SwingUtilities.invokeLater</span> queues a runnable.",
  "<b>The EDT runs the runnable.</b> The table model's entries are replaced and the status label is updated.",
  "<b>Swing repaints.</b> The table asks its model for the new row count and redraws only the visible cells.",
]))

B16.append(visual("""<p>Follow the thread changes in that list: EDT, then database thread, then EDT again.
Steps one to four are EDT. Steps five to eleven are the database thread. Steps twelve to fourteen are
EDT again. The two <span class='mono'>invokeLater</span> boundaries are the only places the two threads
touch.</p>"""))

B16.append("""
<h3><span class="n">16.7</span>Why the table model matters</h3>
<p>A <span class="mono">JTable</span> does not store data. It asks a
<span class="mono">TableModel</span> for it, and the model is where the application's data lives.</p>
""")

B16.append(code('''final class HistoryTableModel extends AbstractTableModel {
    private static final String[] COLUMNS = {"Time", "Type", "Zone", "Detail"};
    private List<DatabaseHistoryEntry> entries = List.of();

    void setEntries(List<DatabaseHistoryEntry> entries) {
        this.entries = List.copyOf(entries);       // defensive copy, immutable
        fireTableDataChanged();                    // tell the table to ask again
    }

    @Override public int getRowCount() { return entries.size(); }
    @Override public int getColumnCount() { return COLUMNS.length; }
    @Override public String getColumnName(int column) { return COLUMNS[column]; }

    @Override public Object getValueAt(int row, int column) {
        DatabaseHistoryEntry entry = entries.get(row);
        return switch (column) {
            case 0 -> entry.at();
            case 1 -> entry.type();
            case 2 -> entry.zoneId() == null ? "\\u2014" : entry.zoneId();
            default -> entry.detail();
        };
    }
}''', "from BasinWatch, app/DatabaseHistoryPanel.java — a table model over immutable rows."))

B16.append("""
<p>Three things in that class are worth noting.</p>

<p><b>The model holds the data, and the table renders it.</b> Replacing the entries and calling
<span class="mono">fireTableDataChanged()</span> is what makes the table update. Without the
notification, the table would keep displaying stale rows, because it has no way to know the model
changed.</p>

<p><b><span class="mono">setEntries</span> takes an immutable copy.</b> The list came from the database
thread; copying it removes any possibility of concurrent modification while the EDT is reading.</p>

<p><b>The nullable zone is handled in the view.</b>
<span class="mono">operational_events.zone_id</span> is nullable by design, and the model renders null as
a dash rather than the text "null".</p>
""")

B16.append(connect("""<p>Compare this with the login application in Chapter 15. That program put its
logic directly in a private method of the frame class. BasinWatch puts the logic in the engine and gives
the panel only a table model. Both are Swing programs; the difference is that one is a demonstration of
mechanics and the other is an application with a persistence layer behind it. Neither is wrong — but the
second is what you need when the data comes from a database.</p>"""))

B16.append(related("""<p>Some applications use <span class='mono'>SwingWorker</span> instead of futures.
It is a JDK class with <span class='mono'>doInBackground()</span> on a worker thread and
<span class='mono'>process()</span> and <span class='mono'>done()</span> on the EDT, and it solves the
same problem. BasinWatch does not use it, for one reason: the engine must work without a user interface,
so its operations cannot depend on a Swing type. Returning
<span class='mono'>CompletableFuture</span> keeps the engine independent of Swing, and the interface
chooses how to consume the result. If you are asked which is better, the honest answer is that
<span class='mono'>SwingWorker</span> is more convenient inside a UI and
<span class='mono'>CompletableFuture</span> is more flexible outside one.</p>"""))

B16.append(exam("""<p>The highest-value question in this part is "trace the path of a user action that
reads from the database." Answer it as a thread journey, not a class list: the EDT handles the click,
the call returns a future immediately, the query runs on the database thread, the future completes there,
and the callback posts back to the EDT to update the model. Mention
<span class='mono'>invokeLater</span> explicitly, and mention that the interface never blocks.</p>"""))

B16.append(summary([
  "A listener must return quickly, so it asks the engine for an operation rather than performing one.",
  "The engine owns several executors and named threads, each with a specific job.",
  "Operations that produce a result return <span class='mono'>CompletableFuture</span>s, so the caller never blocks.",
  "Any code touching a Swing component must be wrapped in <span class='mono'>SwingUtilities.invokeLater</span>, including callbacks from futures.",
  "<span class='mono'>invokeLater</span> queues and returns; <span class='mono'>invokeAndWait</span> blocks and can deadlock if called from the EDT.",
  "A complete click-to-table path crosses the EDT, the database thread, and the EDT again.",
  "A <span class='mono'>JTable</span> renders whatever its <span class='mono'>TableModel</span> provides, and the model must call <span class='mono'>fireTableDataChanged</span> to trigger an update.",
  "The engine returns futures rather than using <span class='mono'>SwingWorker</span>, so that it remains independent of Swing.",
]))

B16.append(keyterms([
  "<b>invokeLater</b> — queueing a runnable to run on the event-dispatch thread, without waiting.",
  "<b>CompletionException</b> — the wrapper used when a checked exception must be thrown from an asynchronous supplier.",
  "<b>TableModel</b> — the object supplying data to a <span class='mono'>JTable</span>.",
  "<b>fireTableDataChanged</b> — the notification that tells a table its model's contents have changed.",
  "<b>Thread confinement</b> — the rule that a particular object may only be accessed from one thread; Swing components are confined to the EDT.",
]))

B16.append("</div>")

HTML = "".join(P + B15 + B16)
