"""PART II — Java I/O and Persistent Files.  Chapters 4-9.

Every chapter is assembled by appending to a list of HTML fragments, which avoids
the string-concatenation fragility of interleaving raw HTML with helper calls.
"""
from . import *

P = []          # PART II opener
B4 = []         # Chapter 4
B5 = []         # Chapter 5
B6 = []         # Chapter 6
B7 = []         # Chapter 7
B8 = []         # Chapter 8
B9 = []         # Chapter 9

P.append("""
<div class="part-page">
  <div class="pnum">PART II</div>
  <h1>Java I/O and Persistent Files</h1>
  <div class="prule"></div>
  <div class="pintro">Everything an application knows arrives through a stream and everything it
  remembers leaves through one. This part builds the stream model from the ground up, layers
  wrappers on top of it, adds in-memory and piped variants, and finishes with object
  serialization — then shows all four mechanisms doing four different jobs in one program.</div>
  <div class="chapters">
    <div><span>4</span>What Is a Stream?</div>
    <div><span>5</span>Reading and Writing Files</div>
    <div><span>6</span>Buffering, Data Streams and Stream Wrappers</div>
    <div><span>7</span>In-Memory and Piped Streams</div>
    <div><span>8</span>Serialization, Deserialization and Session Persistence</div>
    <div><span>9</span>How BasinWatch Uses Java I/O</div>
  </div>
</div>
""")

# ======================================================================
# CHAPTER 4
# ======================================================================
B4.append(chapter(4, "What Is a Stream?",
"The stream abstraction, source and destination, direction, and the four hierarchies that organise the whole java.io package."))

B4.append("""
<h3><span class="n">4.1</span>The problem a stream solves</h3>
<p>Suppose you want to copy a large file. You could read the whole thing into memory as a
<span class="mono">byte[]</span> and then write it out. That works for a small file and fails for
a large one, because the file must fit in memory. It also fails for data that has no end yet — a
network socket, a pipe from another process, or a sensor feed that runs for hours.</p>

<p>A stream is the abstraction that solves this. Instead of handling all the data at once, you
handle it in pieces: read some, process it, read some more. The stream hides whether the bytes
come from a file, memory, a socket or another thread. That is why one
<span class="mono">read()</span> method can serve a disk file and a pipe.</p>
""")

B4.append(defbox("Stream",
"an ordered, one-directional sequence of data with a source or a destination, consumed or produced incrementally rather than all at once."))

B4.append(core("""<p>Three properties define every stream in <span class="mono">java.io</span>,
and every question about streams reduces to them:</p>
<ol>
<li><b>Direction.</b> Input or output — read or write, never both.</li>
<li><b>Unit.</b> Bytes (8-bit) or characters (16-bit, with an encoding).</li>
<li><b>Source or destination.</b> A file, memory, a pipe, or another stream.</li>
</ol>
<p>Name those three and you have named the class you need.</p>"""))

B4.append("""
<h3><span class="n">4.2</span>Source, destination and direction</h3>
<p>Direction is the first thing to fix, because it determines which of two class families you are
in. A <b>source</b> is where data comes from: for an input stream, the source is the file or pipe
you read. A <b>destination</b> is where data goes: for an output stream, the destination is the
file or pipe you write.</p>

<p>The naming is always from the <i>program's</i> point of view, not the device's. A
<span class="mono">FileInputStream</span> reads <i>into</i> the program from a file. A
<span class="mono">FileOutputStream</span> writes <i>out of</i> the program to a file. This is the
single most common source of confusion for beginners, and it disappears once you say the direction
aloud.</p>
""")

B4.append(figure("d03_byte_vs_char", "5", "Byte streams versus character streams",
"The same file seen two ways: as raw 8-bit units that only a program can interpret, and as 16-bit characters encoded through a charset such as UTF-8.",
"landscape"))

B4.append("""
<h3><span class="n">4.3</span>Byte streams versus character streams</h3>
<p>This is the first real decision you make with any stream, and it is a decision about meaning
rather than performance.</p>
""")

B4.append(table(
  ["", "Byte stream", "Character stream"],
  [
    ["Abstract roots", "<span class='mono'>InputStream</span> / <span class='mono'>OutputStream</span>",
     "<span class='mono'>Reader</span> / <span class='mono'>Writer</span>"],
    ["Unit", "one byte (8 bits)", "one character (16 bits)"],
    ["Encoding", "none — bytes are just bytes", "an explicit charset converts characters to bytes, and back"],
    ["Main methods", "<span class='mono'>read()</span>, <span class='mono'>read(byte[])</span>, <span class='mono'>write(int)</span>, <span class='mono'>write(byte[])</span>",
     "<span class='mono'>read()</span>, <span class='mono'>read(char[])</span>, <span class='mono'>write(int)</span>, <span class='mono'>write(String)</span>"],
    ["Convenience", "none — you assemble values yourself", "<span class='mono'>readLine()</span>, <span class='mono'>newLine()</span>, <span class='mono'>append()</span>"],
    ["Correct for", "images, audio, compressed data, typed measurements, serialized objects",
     "logs, reports, configuration, CSV, HTML, any text a person reads"],
    ["Wrong for", "text you intend a human to read", "binary data — encoding will corrupt it"],
  ],
  caption="<b>Table 4.1</b> — The byte/character decision, stated as a comparison."))

B4.append(mistake("""<p>Using a character stream on binary data. Reading a PNG through a
<span class='mono'>FileReader</span> does not merely look wrong — it silently replaces byte
sequences that are not valid in the current charset with a substitution character, and the file is
destroyed. The rule is simple: if a human is meant to read it, use characters; otherwise use
bytes.</p>"""))

B4.append(further("""<p>Why are characters 16-bit when bytes are 8-bit? Because Java's
<span class='mono'>char</span> is a UTF-16 code unit, chosen so that the common characters of the
world's writing systems fit in one unit. The bridge between a 16-bit character and 8-bit storage
is the <i>charset</i> — UTF-8, UTF-16, ISO-8859-1 and so on. A character stream always uses one,
either explicitly or through the platform default.</p>"""))

B4.append(distinct("""<p><b>Encoding</b> is not <b>encryption</b> and it is not compression.
Encoding is a reversible mapping from characters to bytes. Nothing is hidden and nothing is made
smaller — UTF-8 often makes text larger than a single-byte encoding would.</p>"""))

B4.append(practice("""<p>BasinWatch uses character streams where a human reads the output and
byte streams where a machine must reproduce values exactly:</p>
<pre class="long"><span class="cm">// character: a person can open this file and read it</span>
writer = Files.newBufferedWriter(path, StandardCharsets.UTF_8,
        StandardOpenOption.CREATE, StandardOpenOption.APPEND);

<span class="cm">// bytes: values keep their exact type and size</span>
output = new DataOutputStream(new BufferedOutputStream(Files.newOutputStream(path,
        StandardOpenOption.CREATE, StandardOpenOption.APPEND)));</pre>
<div class="codecap"><b>Listing 4.1</b> — from BasinWatch, <span class="mono">io/OperationalJournal.java</span> and <span class="mono">io/SensorArchive.java</span></div>
<p>Both files store rainfall and water level, and both are correct. The difference is who reads
them. <span class="mono">operations.log</span> is for an operator; the archive is for the
program.</p>"""))

B4.append("""
<h3><span class="n">4.4</span>The four hierarchies</h3>
<p>The entire <span class="mono">java.io</span> package is organised around four abstract roots,
and every concrete class descends from exactly one of them.</p>
""")

B4.append(figure("d04_io_hierarchy", "6", "The Java I/O class hierarchies",
"Four abstract roots — InputStream, OutputStream, Reader, Writer — and the concrete classes that specialise the source or destination. The wrapper classes take another stream in their constructor, which is what makes layering possible.",
"portrait"))

B4.append("""
<p>Two things are worth noticing in that diagram.</p>

<p><b>There is a symmetry.</b> Almost every capability exists in four forms. File access is
<span class="mono">FileInputStream</span>, <span class="mono">FileOutputStream</span>,
<span class="mono">FileReader</span>, <span class="mono">FileWriter</span>. In-memory access is
<span class="mono">ByteArrayInputStream</span>, <span class="mono">ByteArrayOutputStream</span>,
<span class="mono">StringReader</span>, <span class="mono">StringWriter</span>. Pipe access is
<span class="mono">PipedInputStream</span>, <span class="mono">PipedOutputStream</span>,
<span class="mono">PipedReader</span>, <span class="mono">PipedWriter</span>. Learn one family and
you have learned the others.</p>

<p><b>Wrapper classes break the pattern deliberately.</b>
<span class="mono">BufferedInputStream</span>, <span class="mono">DataInputStream</span> and
<span class="mono">ObjectInputStream</span> are not sources at all — they are <i>filters</i> that
take another stream and add a capability to it. They sit under
<span class="mono">FilterInputStream</span>, which is the base class for exactly this purpose.</p>
""")

B4.append(connect("""<p>Chapter 6 is entirely about those wrappers. The idea they implement —
add a capability by wrapping, without changing the underlying source — is the <b>decorator
pattern</b>, and it is why a single chain of objects can read a typed
<span class="mono">double</span> efficiently from a file while the file stream itself knows
nothing about doubles.</p>"""))

B4.append("""
<h3><span class="n">4.5</span>The methods that actually matter</h3>
<p>Java's stream API is large, but a small number of methods carry almost all the work. These are
the ones to know by name and return type.</p>
""")

B4.append(table(
  ["Method", "Class", "Returns", "Meaning"],
  [
    ["<span class='mono'>read()</span>", "InputStream / Reader", "int",
     "The next byte or character as an <span class='mono'>int</span> in 0–255 (or 0–65535), or <b>-1</b> at end of stream."],
    ["<span class='mono'>read(byte[] b)</span>", "InputStream", "int",
     "How many bytes were read into the array, or -1 at end."],
    ["<span class='mono'>read(char[] c)</span>", "Reader", "int", "How many characters were read, or -1 at end."],
    ["<span class='mono'>write(int b)</span>", "OutputStream / Writer", "void",
     "Writes the low byte, or the character."],
    ["<span class='mono'>write(byte[] b)</span>", "OutputStream", "void", "Writes the whole array."],
    ["<span class='mono'>write(String s)</span>", "Writer", "void", "Writes a string, encoded."],
    ["<span class='mono'>flush()</span>", "both output families", "void",
     "Pushes buffered data to the destination. Does not close."],
    ["<span class='mono'>close()</span>", "all four roots", "void",
     "Flushes if applicable and releases the underlying resource. Idempotent."],
    ["<span class='mono'>readLine()</span>", "BufferedReader", "String",
     "One line without its terminator, or <b>null</b> at end of stream."],
    ["<span class='mono'>newLine()</span>", "BufferedWriter", "void", "Writes the platform line separator."],
  ],
  caption="<b>Table 4.2</b> — The core stream methods. Note that <span class='mono'>read()</span> returns <span class='mono'>int</span>, not <span class='mono'>byte</span>."))

B4.append(distinct("""<p><b>Why does <span class='mono'>read()</span> return an
<span class='mono'>int</span> instead of a <span class='mono'>byte</span>?</b> Because a byte
cannot represent the end-of-stream marker. Every byte value from 0 to 255 is a legal data byte, so
a separate signal is needed: <span class='mono'>-1</span>. Widening the return type to
<span class='mono'>int</span> makes room for it. This is why the idiom is
<span class='mono'>int b; while ((b = in.read()) != -1)</span> and why casting to
<span class='mono'>byte</span> too early loses the end marker.</p>"""))

B4.append(mistake("""<p>Forgetting that <span class='mono'>readLine()</span> returns
<span class='mono'>null</span> at end of stream while <span class='mono'>read()</span> returns
<span class='mono'>-1</span>. Mixing them up produces an infinite loop that appears to work until
the input ends. BasinWatch's intake loop is written correctly:</p>
<pre><span class="ty">String</span> line;
<span class="kw">while</span> ((line = source.readLine()) != <span class="kw">null</span>) { ... }</pre>
<p>The assignment happens inside the condition, so the loop stops the moment the writer closes the
pipe.</p>"""))

B4.append("""
<h3><span class="n">4.6</span>What happens when things go wrong</h3>
<p>Almost every stream method declares a checked exception. There are only a few you meet in
practice, and they mean different things.</p>
""")

B4.append(table(
  ["Exception", "Thrown when", "Typical cause"],
  [
    ["<span class='mono'>IOException</span>", "Any I/O failure", "Disk full, file locked, pipe closed, permission denied"],
    ["<span class='mono'>FileNotFoundException</span>", "A file cannot be opened for reading",
     "The path does not exist, or the directory does"],
    ["<span class='mono'>EOFException</span>", "A read hits the end before a full value was read",
     "A truncated archive or an incomplete typed record — a <i>subclass</i> of IOException"],
    ["<span class='mono'>UnsupportedEncodingException</span>", "The named charset is unavailable",
     "A typo in a charset name"],
    ["<span class='mono'>NullPointerException</span>", "A null stream or null array is passed",
     "Not an IOException, and not checked — usually a programming error"],
  ],
  caption="<b>Table 4.3</b> — Stream exceptions and what they indicate."))

B4.append(exam("""<p>Two facts about stream exceptions are asked constantly. First,
<span class='mono'>IOException</span> is <i>checked</i>, so the compiler forces you to handle or
declare it — that is deliberate, because I/O failure is normal rather than exceptional. Second,
<span class='mono'>EOFException</span> <i>extends</i> <span class='mono'>IOException</span>, so
catching the parent also catches it. BasinWatch relies on that relationship when it validates an
archive header:</p>
<pre><span class="kw">catch</span> (<span class="ty">java.io.EOFException</span> ex) {
    <span class="kw">throw</span> <span class="kw">new</span> <span class="ty">IOException</span>(<span class="st">"Sensor archive header is incomplete."</span>, ex);
}</pre>"""))

B4.append("""
<h3><span class="n">4.7</span>The one rule about closing</h3>
<p>Every stream holds an operating-system resource: a file handle, a pipe buffer, a socket. Those
are finite. Failing to release them leaks them, and a long-running application will eventually
fail to open anything at all.</p>

<p>Java gives you two ways to guarantee release, and both are used in BasinWatch.</p>
""")

B4.append(code('''// (a) try-with-resources — the preferred form
try (BufferedWriter writer = Files.newBufferedWriter(report, StandardCharsets.UTF_8)) {
    writer.write("BASINWATCH · SITUATION REPORT");
    writer.newLine();
    // ... more writes
}   // close() runs here, even if an exception was thrown

// (b) implementing AutoCloseable on a component that owns a stream
public final class OperationalJournal implements AutoCloseable {
    private final BufferedWriter writer;
    private int pendingLines;

    public OperationalJournal(Path path) throws IOException {
        writer = Files.newBufferedWriter(path, StandardCharsets.UTF_8,
                StandardOpenOption.CREATE, StandardOpenOption.APPEND);
    }

    @Override
    public synchronized void close() throws IOException {
        writer.flush();
        writer.close();
    }
}''', "from BasinWatch, io/ReportWriter.java and io/OperationalJournal.java — both release patterns."))

B4.append(core("""<p>Resources are released in <b>reverse order of acquisition</b>. In
<span class='mono'>try (BufferedInputStream in = new BufferedInputStream(Files.newInputStream(p)))</span>
the buffered stream is closed first, which flushes it into the file stream, which is then closed.
That order is what makes the last bytes reach the disk.</p>"""))

B4.append(summary([
  "A stream is an ordered, one-directional sequence of data, consumed or produced incrementally rather than all at once.",
  "Every stream is described by three properties: direction, unit (byte or character), and source or destination.",
  "Four abstract roots: <span class='mono'>InputStream</span>, <span class='mono'>OutputStream</span>, <span class='mono'>Reader</span>, <span class='mono'>Writer</span>.",
  "Byte streams carry raw 8-bit units and preserve data exactly; character streams carry 16-bit characters through a charset and are correct for text.",
  "<span class='mono'>read()</span> returns <span class='mono'>int</span> so that -1 can mark end of stream; <span class='mono'>readLine()</span> returns <span class='mono'>null</span> instead.",
  "Stream failures are checked <span class='mono'>IOException</span>s; <span class='mono'>EOFException</span> is a subclass indicating a truncated read.",
  "Streams are released by try-with-resources or by implementing <span class='mono'>AutoCloseable</span>, in reverse order of acquisition.",
]))

B4.append(keyterms([
  "<b>Stream</b> — an incremental, one-directional sequence of data.",
  "<b>Charset</b> — the reversible mapping between characters and bytes, for example UTF-8.",
  "<b>Filter stream</b> — a stream that wraps another stream and adds a capability.",
  "<b>try-with-resources</b> — a statement that closes every declared resource automatically, in reverse order.",
  "<b>End of stream</b> — the signal that no more data will arrive: -1 from <span class='mono'>read()</span>, null from <span class='mono'>readLine()</span>.",
]))

B4.append("</div>")

# ======================================================================
# CHAPTER 5
# ======================================================================
B5.append(chapter(5, "Reading and Writing Files",
"The file streams and character streams, their constructors and methods, complete read and write workflows, and the resource rules that keep them safe."))

B5.append("""
<h3><span class="n">5.1</span>From a stream to an actual file</h3>
<p>Chapter 4 described streams in the abstract. To make one real you attach it to a file, and that
requires two different objects in modern Java: a <span class="mono">Path</span> that names the
file, and a stream that reads or writes its contents.</p>
""")

B5.append(distinct("""<p><b>A <span class="mono">File</span> or <span class="mono">Path</span> is
not the file's contents.</b> It is a description of where the file is. You can ask it whether the
file exists, what it is called, how large it is and when it was modified — all without opening it.
Only when you create a stream do you touch the data. BasinWatch uses this distinction
deliberately: it lists saves by inspecting metadata, and reads contents only when a save is
actually restored.</p>"""))

B5.append(code('''public static List<Path> list(Path directory) throws IOException {
    File folder = directory.toFile();
    File[] files = folder.listFiles((parent, name) -> name.toLowerCase().endsWith(".bws"));
    if (files == null) {
        throw new IOException("Unable to list session saves in " + directory.toAbsolutePath());
    }
    return Arrays.stream(files)
            .filter(File::isFile)
            .sorted(Comparator.comparingLong(File::lastModified).reversed())
            .map(File::toPath)
            .toList();
}''', "from BasinWatch, io/SaveCatalog.java — listing saves needs metadata only, no stream at all."))

B5.append("""
<p>Three details in that method repay attention. The filter runs on the directory listing, so
non-matching names are never even considered. The sort is by last-modified time, newest first,
which is what an operator expects from a restore dialog. And the null check matters: an unreadable
or non-existent directory makes <span class="mono">listFiles</span> return
<span class="mono">null</span> rather than an empty array, and a
<span class="mono">NullPointerException</span> here would be far less useful than the explicit
<span class="mono">IOException</span>.</p>

<h3><span class="n">5.2</span>The file-stream classes</h3>
<p>Java has two generations of file-stream API, and both are still in use. Knowing which you are
reading matters.</p>
""")

B5.append(table(
  ["Class", "Family", "How it is built", "Notes"],
  [
    ["<span class='mono'>FileInputStream</span>", "byte input",
     "<span class='mono'>new FileInputStream(path)</span> or <span class='mono'>new FileInputStream(file)</span>",
     "The classic class. Throws <span class='mono'>FileNotFoundException</span>, a subclass of IOException."],
    ["<span class='mono'>FileOutputStream</span>", "byte output",
     "<span class='mono'>new FileOutputStream(path, true)</span> for append",
     "Without the boolean it truncates the file. The second argument is easy to forget."],
    ["<span class='mono'>FileReader</span>", "character input",
     "<span class='mono'>new FileReader(path, StandardCharsets.UTF_8)</span>",
     "Without a charset it uses the platform default, which differs between machines."],
    ["<span class='mono'>FileWriter</span>", "character output",
     "<span class='mono'>new FileWriter(path, StandardCharsets.UTF_8, true)</span>",
     "Same truncate/append trap, and the same platform-default trap."],
    ["<span class='mono'>Files.newInputStream</span>", "byte input",
     "<span class='mono'>Files.newInputStream(path, StandardOpenOption.READ)</span>",
     "The modern equivalent. Options are explicit; failures are plain <span class='mono'>IOException</span>."],
    ["<span class='mono'>Files.newBufferedWriter</span>", "character output",
     "<span class='mono'>Files.newBufferedWriter(path, UTF_8, CREATE, APPEND)</span>",
     "Buffered and charset-explicit in one call. This is what BasinWatch uses."],
  ],
  caption="<b>Table 5.1</b> — The file-stream classes and how each is constructed."))

B5.append(mistake("""<p>Two classic bugs live in that table. First, forgetting the append flag:
<span class='mono'>new FileOutputStream(path)</span> <i>truncates</i> the file to zero length, so a
log that was supposed to grow silently restarts. Second, omitting the charset:
<span class='mono'>new FileWriter(path)</span> uses the platform default encoding, so a file
written on one machine can be unreadable on another. BasinWatch never omits either — it uses
<span class='mono'>StandardCharsets.UTF_8</span> and
<span class='mono'>StandardOpenOption.APPEND</span> explicitly at every site.</p>"""))

B5.append("""
<h3><span class="n">5.3</span>A complete write workflow</h3>
<p>Here is the full sequence for writing text to a file, using the modern API. Read it as a
template; the same five steps appear in every write in this book.</p>
""")

B5.append(code('''import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

public class WriteWorkflow {
    public static void main(String[] args) throws IOException {
        Path target = Path.of("demo", "notes.txt");
        Files.createDirectories(target.getParent());          // 1. ensure the folder exists

        try (BufferedWriter writer =                         // 2. open in try-with-resources
                     Files.newBufferedWriter(target, StandardCharsets.UTF_8)) {
            writer.write("first line");                       // 3. write content
            writer.newLine();                                 //    a real line separator
            writer.write("second line");
            writer.newLine();
            writer.flush();                                   // 4. push buffered bytes out
        }                                                     // 5. close() runs automatically
        System.out.println("Wrote " + Files.size(target) + " bytes");
    }
}''', "illustrative — the canonical text-write workflow, mirroring ReportWriter.write"))

B5.append("""
<p>The five steps are: create the parent directory, open inside try-with-resources, write the
content, flush, and let the block close the stream. The flush at step four is technically optional
here because <span class="mono">close()</span> flushes, but writing it explicitly documents the
intent and matters when a stream is kept open across many writes.</p>
""")

B5.append(practice("""<p>BasinWatch's report writer is the same five steps with real content. Note
that the whole file is produced inside one try-with-resources block, so a failure halfway through
still closes the stream:</p>
<pre class="long"><span class="kw">public static</span> <span class="ty">Path</span> write(<span class="ty">Path</span> directory, <span class="ty">BasinSnapshot</span> snapshot) <span class="kw">throws</span> <span class="ty">IOException</span> {
    <span class="ty">String</span> filename = <span class="st">"basin-status-"</span> + FILE_TIME.format(<span class="ty">Instant</span>.now())
            + <span class="st">"-"</span> + <span class="ty">UUID</span>.randomUUID().toString().substring(0, 8) + <span class="st">".txt"</span>;
    <span class="ty">Path</span> report = directory.resolve(filename);
    <span class="kw">try</span> (<span class="ty">BufferedWriter</span> writer = <span class="ty">Files</span>.newBufferedWriter(report, <span class="ty">StandardCharsets</span>.UTF_8)) {
        writer.write(<span class="st">"BASINWATCH · SITUATION REPORT"</span>);
        writer.newLine();
        writer.write(<span class="st">"Generated: "</span> + <span class="ty">Instant</span>.now());
        writer.newLine();
        <span class="cm">// ... zone conditions, resources, missions, recent activity</span>
    }
    <span class="kw">return</span> report;
}</pre>
<div class="codecap"><b>Listing 5.1</b> — from BasinWatch, <span class="mono">io/ReportWriter.java</span></div>
<p>The filename carries a timestamp and eight characters of a UUID. That combination means two
reports generated in the same second still get distinct names, and the operator can tell when each
was produced without opening it.</p>"""))

B5.append(figure("d07_file_lifecycle", "7", "File persistence lifecycles",
"Each file is opened, written, flushed and closed on a different schedule. The log appends for the lifetime of the session; the archive is opened once and appended to per observation; the snapshot is written once and replaced atomically; a report is written once and never reopened.",
"landscape"))

B5.append("""
<h3><span class="n">5.4</span>A complete read workflow</h3>
<p>Reading has one extra consideration: you do not know how many lines there are, so the loop must
be driven by the read itself.</p>
""")

B5.append(code('''import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

public class ReadWorkflow {
    public static void main(String[] args) throws IOException {
        Path source = Path.of("demo", "notes.txt");
        if (!Files.isRegularFile(source)) {
            throw new IOException("No such file: " + source.toAbsolutePath());
        }
        int lines = 0;
        try (BufferedReader reader =
                     Files.newBufferedReader(source, StandardCharsets.UTF_8)) {
            String line;
            while ((line = reader.readLine()) != null) {   // null marks end of stream
                lines++;
                System.out.println(lines + ": " + line);
            }
        }
        System.out.println("Read " + lines + " line(s)");
    }
}''', "illustrative — the canonical text-read workflow, mirroring SensorIntake's loop"))

B5.append("""
<p>Three habits are worth copying. The existence check produces a clearer message than a raw
<span class="mono">FileNotFoundException</span>. The charset is explicit, so the file reads
identically everywhere. And the loop condition performs the read, so there is no possibility of
testing for end-of-stream and then reading anyway — a bug that would skip or duplicate the last
line.</p>
""")

B5.append(practice("""<p><span class="mono">SensorIntake.run</span> is this workflow applied to a
pipe rather than a file, with validation folded in:</p>
<pre class="long"><span class="kw">try</span> (source) {                                  <span class="cm">// source is the BufferedReader</span>
    <span class="ty">String</span> line;
    <span class="kw">while</span> ((line = source.readLine()) != <span class="kw">null</span>) {
        <span class="ty">BasinEvent</span> event;
        <span class="kw">try</span> {
            <span class="kw">if</span> (line.startsWith(<span class="st">"PULSE|"</span>)) {
                event = <span class="kw">new</span> <span class="ty">SimulationPulse</span>(<span class="ty">Long</span>.parseLong(line.substring(6)));
            } <span class="kw">else</span> {
                event = <span class="ty">SensorReading</span>.parse(line);
            }
        } <span class="kw">catch</span> (<span class="ty">IllegalArgumentException</span> ex) {
            warningReporter.accept(<span class="st">"Discarded malformed sensor record: "</span> + ex.getMessage());
            <span class="kw">continue</span>;                            <span class="cm">// skip, keep reading</span>
        }
        <span class="cm">// ... put(event) into the buffer</span>
    }
} <span class="kw">catch</span> (<span class="ty">IOException</span> ex) {
    warningReporter.accept(<span class="st">"Sensor intake ended with an I/O error: "</span> + ex.getMessage());
}</pre>
<div class="codecap"><b>Listing 5.2</b> — from BasinWatch, <span class="mono">engine/SensorIntake.java</span></div>
<p>Note the two different failure responses. A <i>malformed record</i> is reported and skipped,
because one bad line should not stop the stream. An <i>I/O error</i> ends the loop, because the
stream itself is broken and there is nothing left to read. Distinguishing recoverable bad data
from an unrecoverable channel failure is a design decision, not a detail.</p>"""))

B5.append("""
<h3><span class="n">5.5</span>Appending versus replacing</h3>
<p>Two very different intentions share the same class, and the difference is one boolean or one
option.</p>
""")

B5.append(table(
  ["Intention", "How to open", "Effect on existing content"],
  [
    ["Replace the file", "<span class='mono'>Files.newBufferedWriter(p, UTF_8)</span>",
     "Truncated to zero length immediately on open"],
    ["Add to the file", "<span class='mono'>Files.newBufferedWriter(p, UTF_8, CREATE, APPEND)</span>",
     "Existing content is preserved; new writes go to the end"],
    ["Create if absent", "<span class='mono'>CREATE</span>", "A missing file is created"],
    ["Fail if it already exists", "<span class='mono'>CREATE_NEW</span>",
     "Throws <span class='mono'>FileAlreadyExistsException</span> — useful for safety"],
  ],
  caption="<b>Table 5.2</b> — Open options and their effect on existing data."))

B5.append(practice("""<p>BasinWatch makes both choices, and each is right for its artefact. The
operational journal appends, because it is a running record of everything that has happened:</p>
<pre><span class="cm">// OperationalJournal — append</span>
writer = Files.newBufferedWriter(path, StandardCharsets.UTF_8,
        StandardOpenOption.CREATE, StandardOpenOption.APPEND);</pre>
<p>The report writer replaces, because each report is a fresh snapshot of the current situation
and carries a unique name anyway:</p>
<pre><span class="cm">// ReportWriter — create a new file</span>
<span class="kw">try</span> (<span class="ty">BufferedWriter</span> writer = <span class="ty">Files</span>.newBufferedWriter(report, <span class="ty">StandardCharsets</span>.UTF_8)) { ... }</pre>
<p>Getting this backwards would be a serious defect: a truncating journal would erase history on
every restart, and an appending report would mix yesterday's situation into today's
document.</p>"""))

B5.append("""
<h3><span class="n">5.6</span>Flushing: when data actually reaches the disk</h3>
<p>A buffered stream keeps data in memory until the buffer fills or you flush. This means that
"the write succeeded" and "the bytes are on disk" are different statements.</p>
""")

B5.append(practice("""<p>The journal manages this explicitly, with a policy rather than a reflex.
It flushes when twelve lines have accumulated, or immediately when the message is operationally
significant:</p>
<pre class="long"><span class="kw">public synchronized void</span> append(<span class="ty">ActivityEntry</span> entry) <span class="kw">throws</span> <span class="ty">IOException</span> {
    writer.write(<span class="ty">DateTimeFormatter</span>.ISO_INSTANT.format(entry.at()));
    writer.write(<span class="st">" | "</span>);
    writer.write(entry.category().replace(<span class="st">'\\n'</span>, <span class="st">' '</span>));
    writer.write(<span class="st">" | "</span>);
    writer.write(entry.message().replace(<span class="st">'\\n'</span>, <span class="st">' '</span>));
    writer.newLine();
    pendingLines++;
    <span class="kw">if</span> (pendingLines &gt;= 12 || entry.category().contains(<span class="st">"WARNING"</span>)
            || entry.category().contains(<span class="st">"COMPLETE"</span>)
            || entry.category().contains(<span class="st">"ALLOCATED"</span>)) {
        writer.flush();
        pendingLines = 0;
    }
}</pre>
<div class="codecap"><b>Listing 5.3</b> — from BasinWatch, <span class="mono">io/OperationalJournal.java</span></div>
<p>This is a real engineering trade-off. Flushing every line would guarantee durability but cost a
system call per line. Never flushing would be fast but could lose a burst of activity in a crash.
Flushing on the important categories means that an allocation, a completion or a warning is on
disk immediately, while routine readings can wait a few lines.</p>"""))

B5.append(further("""<p>The two <span class='mono'>replace('\\n', ' ')</span> calls are not
cosmetic. An activity message could contain a newline — from an exception message, for example —
and a newline inside a log line would break the file's one-line-per-entry structure. Replacing it
with a space preserves the format without losing information.</p>"""))

B5.append(distinct("""<p><b><span class='mono'>flush()</span> and <span class='mono'>close()</span>
are not the same.</b> <span class='mono'>flush()</span> pushes buffered data to the operating
system but leaves the stream usable. <span class='mono'>close()</span> flushes <i>and</i> releases
the file handle, after which any further write throws <span class='mono'>IOException</span>.
Calling <span class='mono'>close()</span> twice is safe and has no additional effect.</p>"""))

B5.append("""
<h3><span class="n">5.7</span>What a real write failure looks like</h3>
<p>I/O failures are ordinary events, not exotic ones, and the code should read as though it
expects them. BasinWatch's engine treats a journal failure as something to report but not to
propagate into the event-processing path:</p>
""")

B5.append(code('''IOException journalFailure = null;
for (String message : messages) {
    ActivityEntry entry = new ActivityEntry(Instant.now(), event.category(), message);
    try {
        journal.append(entry);
    } catch (IOException ex) {
        if (journalFailure == null) {
            journalFailure = ex;
        } else {
            journalFailure.addSuppressed(ex);      // keep every failure, lose none
        }
    }
}
// ... archive and database work still happen
if (journalFailure != null) {
    throw journalFailure;                          // reported after the rest of the work
}''', "from BasinWatch, engine/BasinEngine.java — collect failures, continue the work, report at the end."))

B5.append("""
<p>The pattern is worth learning because it appears throughout professional code: attempt every
independent piece of work, accumulate the failures, and report them once at the end. It is the
opposite of stopping at the first problem, and it matters here because a log failure should not
prevent the archive and database writes that follow.</p>
""")

B5.append(exam("""<p>A very common exam question asks you to write a method that copies a text file
line by line and to say what happens if the destination cannot be opened. The expected answer
mentions: try-with-resources so both streams close; an explicit charset; the
<span class='mono'>readLine() != null</span> loop; and that an
<span class='mono'>IOException</span> from the <i>opening</i> of the destination means the source
is never read. Say the order of operations explicitly — examiners look for it.</p>"""))

B5.append(summary([
  "A <span class='mono'>Path</span> or <span class='mono'>File</span> describes where data is; only a stream reads or writes the data itself.",
  "Four classic file classes exist for each direction and unit; the modern <span class='mono'>Files.newXxx</span> methods make options and charsets explicit.",
  "Opening a file for output truncates it unless an append flag or option is supplied.",
  "A complete write workflow is: create the parent, open in try-with-resources, write, flush, close.",
  "A complete read workflow is: check existence, open with an explicit charset, loop on <span class='mono'>readLine() != null</span>, close.",
  "Recoverable bad data should be skipped and reported; an unrecoverable stream failure should end the loop.",
  "<span class='mono'>flush()</span> pushes data onward and keeps the stream open; <span class='mono'>close()</span> flushes and releases the handle.",
]))

B5.append(keyterms([
  "<b>Append mode</b> — opening an output stream so new writes follow existing content.",
  "<b>Truncate</b> — reducing a file to zero length when it is opened for output.",
  "<b>Flush</b> — forcing buffered data out to the destination without closing the stream.",
  "<b>Suppressed exception</b> — a secondary failure attached to a primary one so neither is lost.",
  "<b>Metadata</b> — information about a file (name, size, modification time) as opposed to its contents.",
]))

B5.append("</div>")

# ======================================================================
# CHAPTER 6
# ======================================================================
B6.append(chapter(6, "Buffering, Data Streams and Stream Wrappers",
"How a wrapper adds a capability without changing the source, why buffering changes performance by orders of magnitude, and how typed values are written to a binary file."))

B6.append("""
<h3><span class="n">6.1</span>The problem with one byte at a time</h3>
<p>Every <span class="mono">read()</span> call on a raw file stream is a system call. The operating
system has to leave user code, consult its file-system layer, copy a byte, and return. That
overhead is roughly the same whether you asked for one byte or eight thousand.</p>

<p>So reading a megabyte one byte at a time means a million system calls to move data that would
fit in 128 calls of 8 KB. The CPU spends its time in the kernel boundary rather than on your
program. Buffering fixes this by adding an intermediate array.</p>
""")

B6.append(core("""<p>A <b>buffer</b> is a memory array that sits between your code and the
underlying resource. On the first read the buffer is filled with one large request; subsequent
reads are served from memory until the buffer is exhausted, at which point it is refilled. Writing
works in reverse: bytes accumulate in the buffer and are written out in one large operation when
the buffer fills, when you flush, or when you close.</p>"""))

B6.append("""
<h3><span class="n">6.2</span>Layering: the decorator pattern</h3>
<p>The classes that add buffering, typing and object support are not sources. They take another
stream in their constructor and wrap it. That single design choice is what makes stream code
composable.</p>
""")

B6.append(figure("d05_wrapped_streams", "8", "Wrapped and buffered streams",
"Reading a file through three layers. Each wrapper delegates downward and adds exactly one capability: the buffered stream adds an array, the data stream adds type interpretation. Data flows upward through the same layers.",
"portrait"))

B6.append("""
<p>Read that diagram from the bottom up, because that is the direction data travels on a read. The
file stream delivers raw bytes. The buffered stream collects them into an array so the file stream
is called rarely. The data stream interprets the next four bytes as a <span class="mono">double</span>
and the next four as an <span class="mono">int</span>. Each layer knows only the layer beneath it.</p>

<p>The same chain on a write goes the other way: your code calls
<span class="mono">writeDouble</span>, the data stream converts the value to eight bytes, the
buffered stream collects those bytes, and the file stream eventually writes them out.</p>
""")

B6.append(practice("""<p>BasinWatch's archive writer is exactly this chain, built in one
statement:</p>
<pre class="long"><span class="kw">private static</span> <span class="ty">DataOutputStream</span> openArchive(<span class="ty">Path</span> path) <span class="kw">throws</span> <span class="ty">IOException</span> {
    <span class="kw">boolean</span> fresh = !<span class="ty">Files</span>.isRegularFile(path) || <span class="ty">Files</span>.size(path) == 0;
    <span class="ty">DataOutputStream</span> output = <span class="kw">new</span> <span class="ty">DataOutputStream</span>(<span class="kw">new</span> <span class="ty">BufferedOutputStream</span>(
            <span class="ty">Files</span>.newOutputStream(path, <span class="ty">StandardOpenOption</span>.CREATE, <span class="ty">StandardOpenOption</span>.APPEND)));
    <span class="kw">if</span> (fresh) {
        output.writeInt(MAGIC);
        output.writeInt(FORMAT_VERSION);
        output.flush();
    }
    <span class="kw">return</span> output;
}</pre>
<div class="codecap"><b>Listing 6.1</b> — from BasinWatch, <span class="mono">io/SensorArchive.java</span></div>
<p>Three layers, three capabilities: <span class="mono">Files.newOutputStream</span> talks to the
file, <span class="mono">BufferedOutputStream</span> batches the bytes, and
<span class="mono">DataOutputStream</span> converts typed values to bytes. The
<span class="mono">fresh</span> test decides whether the header must be written — an archive that
already contains data must not get a second header.</p>"""))

B6.append("""
<h3><span class="n">6.3</span>Buffered streams and buffered readers</h3>
<p>Buffering exists in both families, and the character version adds something the byte version
cannot have: line awareness.</p>
""")

B6.append(table(
  ["Class", "Wraps", "Adds", "Characteristic method"],
  [
    ["<span class='mono'>BufferedInputStream</span>", "any <span class='mono'>InputStream</span>",
     "an internal byte array, default 8192 bytes", "<span class='mono'>mark()</span> / <span class='mono'>reset()</span> become usable"],
    ["<span class='mono'>BufferedOutputStream</span>", "any <span class='mono'>OutputStream</span>",
     "an internal byte array", "<span class='mono'>flush()</span> actually matters now"],
    ["<span class='mono'>BufferedReader</span>", "any <span class='mono'>Reader</span>",
     "a character array <i>and</i> line splitting", "<span class='mono'>readLine()</span>"],
    ["<span class='mono'>BufferedWriter</span>", "any <span class='mono'>Writer</span>",
     "a character array and platform line separators", "<span class='mono'>newLine()</span>"],
  ],
  caption="<b>Table 6.1</b> — The four buffering classes and what each adds."))

B6.append(distinct("""<p><b><span class='mono'>readLine()</span> exists only on
<span class='mono'>BufferedReader</span>.</b> It is not on <span class='mono'>Reader</span>, not on
<span class='mono'>FileReader</span>, and not on <span class='mono'>InputStream</span>. This is
why the standard idiom is
<span class='mono'>new BufferedReader(new FileReader(path))</span> — the outer class supplies the
convenience method, the inner one supplies the source. BasinWatch's intake wraps its
<span class='mono'>PipedReader</span> in a <span class='mono'>BufferedReader</span> for exactly
this reason.</p>"""))

B6.append("""
<h3><span class="n">6.4</span>Data streams: typed values in a binary file</h3>
<p>A character stream can store the text <span class="mono">"12.5"</span>. A data stream can store
the <i>number</i> 12.5 — eight bytes in a defined format that any Java program can read back
without parsing.</p>
""")

B6.append(defbox("DataInputStream / DataOutputStream",
"filter streams that read and write Java's primitive types and UTF-8 strings in a fixed binary format, independent of locale and of how the value would be printed."))

B6.append(table(
  ["Method", "Bytes written", "Notes"],
  [
    ["<span class='mono'>writeBoolean(boolean)</span>", "1", "A single byte, 0 or 1"],
    ["<span class='mono'>writeInt(int)</span>", "4", "Big-endian, most significant byte first"],
    ["<span class='mono'>writeLong(long)</span>", "8", "Big-endian"],
    ["<span class='mono'>writeDouble(double)</span>", "8", "IEEE 754 double-precision, big-endian"],
    ["<span class='mono'>writeUTF(String)</span>", "2 + n", "A two-byte length, then modified UTF-8 bytes — maximum 65535 bytes"],
    ["<span class='mono'>writeChars(String)</span>", "2 × n", "Two bytes per character, no length prefix"],
  ],
  caption="<b>Table 6.2</b> — Data-stream methods and their exact sizes. These sizes are what makes the format self-describing."))

B6.append(core("""<p>Every data-stream write has exactly one matching read, and the <b>order must be
identical</b>. A file written as <span class='mono'>writeInt</span> then
<span class='mono'>writeDouble</span> must be read as <span class='mono'>readInt</span> then
<span class='mono'>readDouble</span>. There is no self-describing metadata inside a data stream —
the sequence of calls <i>is</i> the schema. Change the order in one place and every subsequent
read returns garbage, usually without an exception.</p>"""))

B6.append(mistake("""<p>Reading a data stream in the wrong order is the classic silent corruption.
Because every method simply consumes the next n bytes, a
<span class='mono'>readDouble()</span> where a <span class='mono'>readInt()</span> was expected
does not throw — it returns a perfectly valid but completely wrong number. The only defence is to
keep the write order and the read order adjacent in the codebase and to version the format
explicitly, which BasinWatch does with <span class='mono'>FORMAT_VERSION</span>.</p>"""))

B6.append("""
<h3><span class="n">6.5</span>A complete typed-record workflow</h3>
<p>Here is the write side and the read side of one record, side by side. BasinWatch writes a
header once and then one record per accepted observation.</p>
""")

B6.append(code('''// --- the header, written once when the archive is created ---
static final int MAGIC = 0x42574154;          // "BWAT"
static final int FORMAT_VERSION = 1;

output.writeInt(MAGIC);                       // 4 bytes: identifies the file
output.writeInt(FORMAT_VERSION);              // 4 bytes: which layout follows

// --- one record per accepted observation ---
output.writeLong(reading.tick());             // 8 bytes
output.writeUTF(reading.stationId());         // 2 + n bytes
output.writeUTF(reading.zoneId());            // 2 + n bytes
output.writeDouble(reading.rainfallMillimeters());    // 8 bytes
output.writeDouble(reading.observedRiseCentimeters()); // 8 bytes''',
"from BasinWatch, io/SensorArchive.java — the write order defines the format."))

B6.append(code('''// --- reading the header back, and validating it ---
int magic = input.readInt();
if (magic != MAGIC) {
    throw new IOException("Sensor archive has an unexpected signature.");
}
int version = input.readInt();
if (version != FORMAT_VERSION) {
    throw new IOException("Unsupported sensor archive version: " + version);
}

// --- reading records until the file ends ---
while (true) {
    try {
        long tick = input.readLong();
        String stationId = input.readUTF();
        String zoneId = input.readUTF();
        double rainfall = input.readDouble();
        double rise = input.readDouble();
        // ... build a SensorReading and report it
    } catch (EOFException end) {
        break;                                 // a clean end of file, not an error
    }
}''', "from BasinWatch, io/SensorArchive.java — the matching read order, with EOF as the terminator."))

B6.append("""
<p>Four things in those listings are worth naming, because they are the difference between a toy
binary format and a usable one.</p>

<p><b>A magic number identifies the file.</b> The constant 0x42574154 spells "BWAT" in ASCII. If
someone points the reader at a different file, the first read fails immediately with a clear
message rather than producing nonsense.</p>

<p><b>A version number allows the format to change.</b> When the layout gains a field, the version
is incremented and the reader can decide what to do. Without it, an old reader would silently
misinterpret a new file.</p>

<p><b>End of file is the terminator.</b> There is no record count, so the loop reads until
<span class="mono">EOFException</span> and treats that as the normal end. This is why the record
must be written completely: a half-written record produces an
<span class="mono">EOFException</span> in the middle of a record, which the reader cannot
distinguish from a clean end unless it tracks how far it got.</p>

<p><b>The strings use writeUTF.</b> Each string carries its own length, so there is no ambiguity
about where one ends and the next begins. That is precisely what
<span class="mono">writeChars</span> cannot offer.</p>
""")

B6.append(connect("""<p>Compare this with Chapter 8's session snapshot, which stores whole objects
rather than typed primitives. Both are binary, both are byte streams — but the data stream gives
you a format you control field by field, while object serialization gives you a format the JDK
controls and that you must actively secure. Neither is universally better; the archive chose
control, the snapshot chose convenience plus validation.</p>"""))

B6.append("""
<h3><span class="n">6.6</span>Where each wrapper belongs</h3>
<p>Choosing a chain is a small design decision you make constantly. The pattern is always the
same: start with the source or destination, then add one wrapper per capability you need.</p>
""")

B6.append(table(
  ["Task", "Chain", "Why"],
  [
    ["Read a large file quickly, byte by byte",
     "<span class='mono'>BufferedInputStream</span> → <span class='mono'>FileInputStream</span>",
     "Buffering removes the per-byte system call."],
    ["Read a text file line by line",
     "<span class='mono'>BufferedReader</span> → <span class='mono'>FileReader</span>",
     "<span class='mono'>readLine()</span> lives on the buffered reader."],
    ["Read typed numbers from a binary file quickly",
     "<span class='mono'>DataInputStream</span> → <span class='mono'>BufferedInputStream</span> → <span class='mono'>FileInputStream</span>",
     "Typing on the outside, buffering in the middle, the file at the core."],
    ["Write a log line by line",
     "<span class='mono'>BufferedWriter</span> → <span class='mono'>FileWriter</span>",
     "Line methods plus batching, with an explicit charset."],
    ["Build bytes in memory then hand them to a socket",
     "<span class='mono'>DataOutputStream</span> → <span class='mono'>ByteArrayOutputStream</span>",
     "Chapter 7 covers the in-memory destination."],
  ],
  caption="<b>Table 6.3</b> — Common wrapper chains and the reason for each layer."))

B6.append(exam("""<p>If asked "why wrap a <span class='mono'>FileInputStream</span> in a
<span class='mono'>BufferedInputStream</span>?", the precise answer is about call frequency, not
speed in the abstract: buffering reduces the number of system calls by roughly the ratio of buffer
size to read size, and each system call has a fixed cost that dominates for small reads. Saying
"it's faster" without the mechanism usually loses marks.</p>"""))

B6.append(summary([
  "A buffer is a memory array between your code and the resource, turning many small operations into few large ones.",
  "Wrapper classes take another stream in their constructor and add exactly one capability — the decorator pattern.",
  "Reading travels upward through the chain; writing travels downward. Each layer knows only the layer beneath it.",
  "<span class='mono'>readLine()</span> exists only on <span class='mono'>BufferedReader</span>, which is why buffering is not optional for line-based text.",
  "Data streams write primitives in a fixed binary format whose write order defines the schema; the matching read order must be identical.",
  "A usable binary format has a magic number, a version, self-describing strings via <span class='mono'>writeUTF</span>, and a defined end condition.",
  "A <span class='mono'>BufferedOutputStream</span> makes <span class='mono'>flush()</span> significant — without it, bytes may sit in memory.",
]))

B6.append(keyterms([
  "<b>Decorator pattern</b> — adding behaviour by wrapping an object in another object of the same interface.",
  "<b>Filter stream</b> — a wrapper stream; its constructor takes the stream it wraps.",
  "<b>Magic number</b> — a constant at the start of a file identifying its format.",
  "<b>Format version</b> — a number that lets a reader detect an incompatible layout.",
  "<b>writeUTF</b> — a data-stream method that writes a two-byte length followed by modified UTF-8 bytes.",
]))

B6.append("</div>")

# ======================================================================
# CHAPTER 7
# ======================================================================
B7.append(chapter(7, "In-Memory and Piped Streams",
"Streams whose source is memory, and streams that connect two threads. This chapter covers byte-array streams, piped streams, and the producer–consumer pattern."))

B7.append("""
<h3><span class="n">7.1</span>Why a stream with no file?</h3>
<p>Not every stream is attached to a device. Two important sources and destinations are entirely
inside the program: a byte array in memory, and a pipe connecting two threads.</p>

<p>The in-memory case is useful because it lets you reuse the whole stream API for something that
never touches a disk. Building a payload with <span class="mono">DataOutputStream</span> gives you
the same typed writes as a file, and the result is a <span class="mono">byte[]</span> you can hand
to a network call, a cache or a test assertion.</p>

<p>The piped case is useful because it solves a real problem: two threads that must exchange a
stream of data without sharing a data structure.</p>
""")

B7.append("""
<h3><span class="n">7.2</span>Byte-array streams</h3>
<p>A <span class="mono">ByteArrayOutputStream</span> collects everything written to it in an
internal growable array; <span class="mono">toByteArray()</span> hands you the contents. A
<span class="mono">ByteArrayInputStream</span> reads from an array you already have.</p>
""")

B7.append(code('''import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;

public class InMemoryPayload {
    public static void main(String[] args) throws IOException {
        byte[] payload;

        // write typed values into memory
        try (ByteArrayOutputStream buffer = new ByteArrayOutputStream();
             DataOutputStream out = new DataOutputStream(buffer)) {
            out.writeInt(7);                 // a tick
            out.writeUTF("MIL");             // a zone
            out.writeDouble(42.5);           // rainfall
            out.flush();
            payload = buffer.toByteArray();
        }

        System.out.println("payload size = " + payload.length + " bytes");

        // read them back, with no file anywhere
        try (DataInputStream in = new DataInputStream(new ByteArrayInputStream(payload))) {
            System.out.println("tick   = " + in.readInt());
            System.out.println("zone   = " + in.readUTF());
            System.out.println("rain   = " + in.readDouble());
        }
    }
}''', "illustrative — the same typed format, entirely in memory"))

B7.append("""
<p>Expected output, and the arithmetic behind the size:</p>
<pre>payload size = 17 bytes
tick   = 7
zone   = MIL
rain   = 42.5</pre>
""")

B7.append(visual("""<p>Seventeen bytes is not a coincidence. <span class='mono'>writeInt</span>
contributes 4, <span class='mono'>writeUTF("MIL")</span> contributes 2 for the length plus 3 for
the characters, and <span class='mono'>writeDouble</span> contributes 8. Four plus five plus eight
is seventeen. If you can predict that number before running the program, you understand the
format.</p>"""))

B7.append(distinct("""<p><b>Closing a byte-array stream has no effect on the array.</b> There is no
operating-system resource to release, so <span class='mono'>close()</span> is a no-op. It is still
worth calling — through try-with-resources — because it means the same code shape works when the
destination later becomes a file or a socket. BasinWatch's archive code is written so that only the
innermost source changes.</p>"""))

B7.append("""
<h3><span class="n">7.3</span>Piped streams</h3>
<p>A pipe is a matched pair: a writer at one end, a reader at the other, with a bounded buffer
between them. What the writer writes, the reader reads, in order.</p>
""")

B7.append(defbox("Piped stream",
"a connected pair of streams, <span class='mono'>PipedWriter</span>/<span class='mono'>PipedReader</span> or <span class='mono'>PipedOutputStream</span>/<span class='mono'>PipedInputStream</span>, that transfers data from one thread to another through an internal buffer."))

B7.append(figure("d06_piped_producer_consumer", "9", "The piped-stream producer and consumer",
"SensorFeed writes encoded observation lines into a PipedWriter. SensorIntake reads them from a PipedReader wrapped in a BufferedReader, validates each line, and places accepted events into the bounded EventBuffer. The pipe provides the thread boundary; the buffer provides the queue.",
"portrait"))

B7.append("""
<p>Three properties of that arrangement matter, and each is a design decision.</p>

<p><b>The pipe is the only shared object.</b> The producer never sees the buffer, the queue or the
model. The consumer never sees the producer. Each thread's dependencies are visible in its
constructor.</p>

<p><b>The pipe is bounded, so it provides back-pressure.</b> BasinWatch constructs it with an
8,192-character buffer. If the producer runs faster than the consumer, the producer blocks on
<span class="mono">write</span> instead of filling memory. This is the same property a bounded
queue has, obtained for free.</p>

<p><b>Both ends must be closed for the reader to finish cleanly.</b> The writer closing is what
turns the reader's next <span class="mono">readLine()</span> into a
<span class="mono">null</span>, ending the loop. If the writer never closes, the reader waits
forever.</p>
""")

B7.append(mistake("""<p><b>A pipe is not automatically thread-safe in the sense people assume.</b>
A <span class='mono'>PipedReader</span> and its <span class='mono'>PipedWriter</span> are intended
to be used by <i>different</i> threads. Using both ends in one thread is a classic deadlock: the
reader blocks waiting for data that only the same thread could write. If you need a stream in one
thread, use a byte-array stream.</p>"""))

B7.append("""
<h3><span class="n">7.4</span>The producer side</h3>
<p>The producer is a thread with a loop, a cadence and a stop flag. Its job is to encode a value
and write it as one line.</p>
""")

B7.append(code('''public final class SensorFeed extends Thread {
    private final Writer destination;
    private final List<String> zoneIds;
    private final SimulationSettings settings;
    private final AtomicLong tickSequence;
    private final Consumer<String> failureReporter;
    private volatile boolean running = true;

    @Override
    public void run() {
        Random random = new Random();
        try {
            while (running && !isInterrupted()) {
                long tick = tickSequence.incrementAndGet();
                for (String zoneId : zoneIds) {
                    SensorReading reading = new SensorReading(tick, stationId(zoneId), zoneId,
                            round1(random.nextDouble() * settings.rainfallMillimeters()),
                            round1(random.nextDouble() * settings.riseCentimeters()));
                    destination.write(reading.encode());
                    destination.write(System.lineSeparator());
                }
                destination.flush();
                Thread.sleep(settings.tickIntervalMillis());
            }
        } catch (InterruptedException ex) {
            Thread.currentThread().interrupt();      // restore the flag and stop
        } catch (IOException ex) {
            failureReporter.accept("Sensor feed stopped: " + ex.getMessage());
        } finally {
            closeQuietly();
        }
    }
}''', "from BasinWatch, engine/SensorFeed.java — encode one line per observation, then flush."))

B7.append("""
<p>Five details in that loop are worth studying, because each one is a concurrency decision.</p>

<p><b><span class="mono">running</span> is volatile.</b> It is written by one thread (the caller of
<span class="mono">requestStop()</span>) and read by another (this loop). Without
<span class="mono">volatile</span>, the reader could cache a stale value and never stop.</p>

<p><b>The loop checks both the flag and the interrupt.</b> Either mechanism alone is enough, but
checking both means a stop request works whether it arrives between iterations or during the
sleep.</p>

<p><b><span class="mono">InterruptedException</span> restores the flag.</b> Catching the exception
clears the thread's interrupt status, so
<span class="mono">Thread.currentThread().interrupt()</span> puts it back. This is the correct
handling and it is easy to get wrong.</p>

<p><b>The line separator is platform-independent at the source.</b> Using
<span class="mono">System.lineSeparator()</span> means the encoding matches what
<span class="mono">readLine()</span> expects on the same machine.</p>

<p><b>The writer is closed in a finally block.</b> That is what makes the consumer's loop
terminate, even if the producer stopped because of an error.</p>
""")

B7.append("""
<h3><span class="n">7.5</span>The consumer side</h3>
<p>The consumer reads lines, validates them and passes accepted events onward. It is a
<span class="mono">Runnable</span> rather than a thread, because the engine owns the thread.</p>
""")

B7.append(code('''public final class SensorIntake implements Runnable {
    private final BufferedReader source;
    private final EventBuffer buffer;
    private final Consumer<String> warningReporter;
    private final Consumer<String> statusReporter;

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
                    continue;                        // one bad line must not stop the stream
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
}''', "from BasinWatch, engine/SensorIntake.java — read, parse, report, enqueue."))

B7.append(connect("""<p>Note the interaction of three mechanisms in twelve lines. The pipe supplies
characters (<span class='mono'>readLine()</span>). Parsing supplies validation
(<span class='mono'>SensorReading.parse</span> throws on bad data). The bounded queue supplies
hand-off to the workers (<span class='mono'>buffer.put</span> blocks when full). Chapter 3 named
these as three separate mechanisms; here they are one loop.</p>"""))

B7.append("""
<h3><span class="n">7.6</span>Wiring the pair, and shutting it down</h3>
<p>Creating a connected pipe requires the writer to exist before the reader, and the reader's
constructor to receive the writer. That ordering is why the engine builds both in one method.</p>
""")

B7.append(code('''private void startFeed() throws IOException {
    PipedWriter writer = new PipedWriter();
    PipedReader reader = new PipedReader(writer, 8_192);   // explicit buffer size
    feedWriter = writer;
    intakeThread = new Thread(new SensorIntake(new BufferedReader(reader), eventBuffer,
            this::reportFailure, ignored -> publishDiagnosticsStatus()), "basin-sensor-intake");
    sensorFeed = new SensorFeed(writer, List.of("UPR", "MIL", "NOR", "OLD", "MAR", "SOU"),
            settings, tickSequence, this::reportFailure);
    intakeThread.start();
    sensorFeed.start();
}

// --- and the shutdown, in the order that lets the consumer finish ---
public synchronized void closeEngine() {
    try {
        if (sensorFeed != null) {
            sensorFeed.requestStop();          // 1. stop producing
        }
        if (feedWriter != null) {
            feedWriter.close();                // 2. closing the writer ends readLine()
        }
        if (intakeThread != null) {
            intakeThread.join(2_000);          // 3. wait for the consumer to drain
        }
        eventBuffer.close();                   // 4. wake any waiting workers
        // ... archive drain, journal flush, final snapshot
    } catch (IOException | InterruptedException ex) {
        Thread.currentThread().interrupt();
    }
}''', "from BasinWatch, engine/BasinEngine.java — creation order and shutdown order are both deliberate."))

B7.append("""
<p>The shutdown sequence is the part students most often get wrong, so it is worth stating as a
rule. The four steps are ordered by dependency: you must stop the producer before closing the pipe,
close the pipe before waiting for the consumer (otherwise the consumer blocks forever), and close
the queue after the consumer has drained it (otherwise accepted events are lost).</p>
""")

B7.append(trace("Shutdown ordering, and what breaks if it is wrong", [
  "<b>Stop the producer.</b> <span class='mono'>requestStop()</span> sets the flag; the feed loop exits at the next check.",
  "<b>Close the writer.</b> This flushes any buffered characters into the pipe and signals end of stream.",
  "<b>Join the intake thread.</b> The consumer's <span class='mono'>readLine()</span> now returns null, the loop ends, and the thread finishes. A bounded join with a timeout means shutdown cannot hang forever.",
  "<b>Close the buffer.</b> Waiting workers are woken by <span class='mono'>notifyAll</span> and see the closed flag, so they exit instead of waiting for events that will never come.",
  "<i>If you close the writer before stopping the producer:</i> the producer throws IOException on its next write and reports a spurious failure.",
  "<i>If you close the buffer before joining the consumer:</i> events already read from the pipe are discarded, so the log and database lose the last few observations.",
  "<i>If you never close the writer:</i> the consumer blocks in <span class='mono'>readLine()</span> forever and the application will not exit.",
]))

B7.append("""
<h3><span class="n">7.7</span>Reading a file, an in-memory payload, and a pipe</h3>
<p>The three cases look almost identical at the call site, which is the point of the stream
abstraction. Only the constructor differs.</p>
""")

B7.append(table(
  ["", "From a file", "From memory", "Through a pipe"],
  [
    ["Source", "<span class='mono'>Files.newBufferedReader(path, UTF_8)</span>",
     "<span class='mono'>new ByteArrayInputStream(bytes)</span>",
     "<span class='mono'>new BufferedReader(new PipedReader(writer))</span>"],
    ["Blocking behaviour", "blocks on disk read", "never blocks — data is already present",
     "blocks until the writer produces data"],
    ["End of stream", "when the file ends", "when the array is exhausted", "when the writer closes"],
    ["Resource to release", "an OS file handle", "nothing", "a thread waiting at the other end"],
    ["Thread safety", "one reader per stream", "safe if the array is not mutated", "designed for two different threads"],
    ["Used in BasinWatch", "restoring a session snapshot, listing reports", "building a payload before writing",
     "the live sensor feed"],
  ],
  caption="<b>Table 7.1</b> — The same read loop, three different sources."))

B7.append(exam("""<p>A frequently asked question is "why does Java need a separate
<span class='mono'>PipedReader</span> when a shared queue would do?" The strongest answer covers
three points: the pipe enforces a one-directional contract so neither thread can reach the other's
state; the pipe's buffer gives back-pressure without extra code; and the pipe's close protocol gives
a natural end-of-stream signal, which a queue must simulate with a sentinel value.</p>"""))

B7.append(summary([
  "A byte-array stream uses the whole stream API with no device attached; closing it releases nothing.",
  "A pipe is a matched writer/reader pair with a bounded internal buffer, intended for two different threads.",
  "The pipe is the only object the producer and consumer share, which narrows both contracts.",
  "A bounded pipe provides back-pressure: a fast producer blocks instead of exhausting memory.",
  "The producer must close the writer for the consumer's read loop to terminate.",
  "Shutdown order is stop producer, close writer, join consumer, close queue — each step depends on the previous.",
  "The same read loop works for a file, an in-memory array and a pipe; only the constructor changes.",
]))

B7.append(keyterms([
  "<b>Back-pressure</b> — a bounded channel making a fast producer wait rather than buffer without limit.",
  "<b>End of stream</b> — in a pipe, the signal produced by closing the writer.",
  "<b>volatile</b> — a field modifier guaranteeing that a write by one thread becomes visible to another.",
  "<b>Interrupt</b> — a cooperative request for a thread to stop; it does not force termination.",
  "<b>Bounded join</b> — waiting for a thread with a timeout so shutdown cannot hang indefinitely.",
]))

B7.append("</div>")

# ======================================================================
# CHAPTER 8
# ======================================================================
B8.append(chapter(8, "Serialization, Deserialization and Session Persistence",
"How objects are turned into bytes and back, why that is dangerous by default, and how a real application makes it safe."))

B8.append("""
<h3><span class="n">8.1</span>The problem: saving an object graph</h3>
<p>A data stream can save a <span class="mono">double</span> because a double has a fixed size and
layout. But what about an object? An object has fields of different types, may contain other
objects, may contain collections of objects, and may have a class hierarchy. Writing it out field by
field is tedious and breaks whenever a field is added.</p>

<p>Object serialization solves this by letting the runtime do the traversal. You declare that a class
is serializable, and the JVM writes the object's class identity and its non-transient field values,
recursing into any objects those fields reference.</p>
""")

B8.append(defbox("Serialization",
"the process of converting an object into a byte sequence that can be written to a stream and later reconstructed, preserving the object's class and field values."))

B8.append(defbox("Deserialization",
"the reverse process: reading that byte sequence and reconstructing an object graph, including the classes it contains."))

B8.append("""
<h3><span class="n">8.2</span>How it works</h3>
<p>Two classes do the work, and they are both filter streams, so they follow exactly the pattern from
Chapter 6.</p>
""")

B8.append(code('''import java.io.*;

public class SerializeDemo {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        Path path = Path.of("demo", "sample.ser");

        // ---- serialization: object -> bytes -> file ----
        try (ObjectOutputStream out = new ObjectOutputStream(
                new BufferedOutputStream(Files.newOutputStream(path,
                        StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING)))) {
            out.writeObject(new Sample("MIL", 2.45, 12));
            out.flush();
        }

        // ---- deserialization: file -> bytes -> object ----
        try (ObjectInputStream in = new ObjectInputStream(
                new BufferedInputStream(Files.newInputStream(path)))) {
            Object restored = in.readObject();
            System.out.println("restored = " + restored);
        }
    }

    static final class Sample implements Serializable {
        private static final long serialVersionUID = 1L;
        private final String zone;
        private final double level;
        private final int residents;
        Sample(String zone, double level, int residents) {
            this.zone = zone; this.level = level; this.residents = residents;
        }
        @Override public String toString() {
            return zone + " " + level + " m / " + residents + " residents";
        }
    }
}''', "illustrative — the minimal serialization round trip"))

B8.append("""
<p>Expected output:</p>
<pre>restored = MIL 2.45 m / 12 residents</pre>
""")

B8.append(figure("d08_serialization", "10", "Serialization and deserialization",
"An object graph becomes a byte stream headed by the class descriptor and the serialVersionUID, then a field-value sequence. Deserialization reverses it: read the descriptor, load and check the class, then allocate and populate the object without calling its constructor.",
"portrait"))

B8.append("""
<h3><span class="n">8.3</span>The five facts that matter</h3>

<p><b>1. A class must implement <span class="mono">Serializable</span>.</b> It is a marker
interface: it declares no methods. Its only purpose is to permit the runtime to write the object.
Any class that does not implement it, and is not an ancestor, causes
<span class="mono">NotSerializableException</span> at write time.</p>

<p><b>2. Fields must be serializable too, or marked transient.</b> Serialization recurses, so every
non-transient field must itself be serializable or a primitive. A
<span class="mono">Thread</span>, an open <span class="mono">Stream</span>, a
<span class="mono">Connection</span> — none of these can be serialized, and trying produces an
exception naming the offending field.</p>

<p><b>3. <span class="mono">transient</span> excludes a field.</b> A transient field is skipped
entirely and, on deserialization, receives its default value: <span class="mono">null</span>, 0 or
<span class="mono">false</span>. This is how you exclude a cache, a lock or a derived value.</p>

<p><b>4. <span class="mono">static</span> fields are not serialized.</b> They belong to the class,
not the object, so they are not part of the instance state being written.</p>

<p><b>5. The constructor is not called on deserialization.</b> The object is allocated and its fields
are set directly by the runtime. This is why the no-argument constructor that serialization
conventionally requires need not do anything, and why validation placed in a constructor will
<i>not</i> run when an object is restored.</p>
""")

B8.append(core("""<p>Fact five is the one that surprises people, and it is the reason a real
application cannot simply trust the objects it reads. If a constructor enforces "water level must be
between 0 and 8", that rule is bypassed entirely by deserialization. BasinWatch therefore validates
the restored state explicitly after reading it, rather than assuming the invariants held.</p>"""))

B8.append("""
<h3><span class="n">8.4</span>serialVersionUID and version compatibility</h3>
<p>Every serializable class has an identity that the stream records. If you declare it yourself, the
compiler uses your value. If you do not, the compiler derives one from the class's structure — its
name, its modifiers, its interfaces and every method and field signature.</p>
""")

B8.append(table(
  ["Situation", "Without an explicit serialVersionUID", "With an explicit serialVersionUID"],
  [
    ["Add a harmless method", "The derived UID changes", "Nothing changes"],
    ["Change a field's type", "The derived UID changes", "Deserialization fails with a field-type error"],
    ["Add a new field", "The derived UID changes", "The new field receives its default value — old files still load"],
    ["Remove a field", "The derived UID changes", "The removed field is ignored — old files still load"],
    ["Recompile the same source", "The derived UID is stable for the same compiler", "Stable by construction"],
  ],
  caption="<b>Table 8.1</b> — Why an explicit <span class='mono'>serialVersionUID</span> is worth declaring."))

B8.append(mistake("""<p>Relying on the computed <span class='mono'>serialVersionUID</span>. Two
builds of the "same" class on different JDK versions or with different compilers can produce
different values, and then every saved file becomes unreadable with
<span class='mono'>InvalidClassException: local class incompatible</span>. Declaring the constant
explicitly is one line and removes a whole class of support problems.</p>"""))

B8.append("""
<h3><span class="n">8.5</span>Why default serialization is unsafe</h3>
<p>Deserialization reconstructs an object graph from bytes that may come from anywhere. The runtime
will happily instantiate whatever classes the stream names. That is a security problem, not a
theoretical one: a crafted stream can instantiate classes you never intended, and the "gadget
chains" that made several widely reported vulnerabilities possible all relied on exactly this.</p>
""")

B8.append(defbox("Deserialization vulnerability",
"the risk that a malicious byte stream causes the runtime to instantiate and initialise classes of the attacker's choosing, because deserialization bypasses constructors and honours the class names in the stream."))

B8.append("""
<p>There are four independent defences, and a robust implementation uses all of them rather than
picking one.</p>
""")

B8.append(table(
  ["Defence", "What it prevents", "How it is expressed"],
  [
    ["Bound the input size", "Denial of service by an enormous or deeply nested stream",
     "Check the file length against a constant before opening the stream"],
    ["Filter the classes that may be constructed", "Instantiating an attacker-chosen class",
     "<span class='mono'>ObjectInputFilter</span> via <span class='mono'>setObjectInputFilter</span>"],
    ["Validate after reading", "Accepting a structurally valid but semantically impossible object",
     "Explicit range and consistency checks on the restored values"],
    ["Check a format version", "Reading a file written by an incompatible build",
     "A version field written in the header and compared on read"],
  ],
  caption="<b>Table 8.2</b> — The four defences, all of which BasinWatch implements."))

B8.append("""
<h3><span class="n">8.6</span>How BasinWatch saves and restores a session</h3>
<p>The project's snapshot store is a careful implementation of the four defences, and reading it is
the best way to see them in practice. It writes to a temporary file and then replaces the real file
atomically, so a crash during a save cannot leave a half-written snapshot in place.</p>
""")

B8.append(code('''public final class SnapshotStore {
    static final int FORMAT_VERSION = 1;
    static final long MAX_SAVE_BYTES = 4L * 1024 * 1024;   // 4 MB is generous for this model

    public void save(Path target, SessionSnapshot snapshot) throws IOException {
        Files.createDirectories(target.toAbsolutePath().getParent());
        Path temporary = target.resolveSibling(target.getFileName() + ".tmp");
        try (ObjectOutputStream out = new ObjectOutputStream(new BufferedOutputStream(
                Files.newOutputStream(temporary, StandardOpenOption.CREATE,
                        StandardOpenOption.TRUNCATE_EXISTING)))) {
            out.writeInt(FORMAT_VERSION);      // written first, so a reader can check it early
            out.writeObject(snapshot);
            out.flush();
        }
        try {
            Files.move(temporary, target, StandardCopyOption.REPLACE_EXISTING,
                    StandardCopyOption.ATOMIC_MOVE);       // atomic replace
        } catch (AtomicMoveNotSupportedException ex) {
            Files.move(temporary, target, StandardCopyOption.REPLACE_EXISTING);
        }
    }
}''', "from BasinWatch, io/SnapshotStore.java — write to a temporary file, then move it into place."))

B8.append("""
<p>Two things in the write path are deliberate. The version is written <i>before</i> the object, so a
reader can reject an incompatible file without attempting to interpret it. And the save goes to
<span class="mono">name.bws.tmp</span> first, with the real file replaced only when the write has
succeeded. If the process dies mid-save, the previous good snapshot is still intact.</p>
""")

B8.append(code('''public SessionSnapshot load(Path source) throws IOException, ClassNotFoundException {
    if (!Files.isRegularFile(source)) {
        throw new IOException("Session save not found: " + source.toAbsolutePath());
    }
    if (Files.size(source) > MAX_SAVE_BYTES) {              // defence 1: bound the input
        throw new IOException("Session save is unexpectedly large: " + Files.size(source) + " bytes");
    }
    try (ObjectInputStream in = new ObjectInputStream(new BufferedInputStream(
            Files.newInputStream(source)))) {
        in.setObjectInputFilter(SnapshotStore::allowOnlySafeClasses);   // defence 2: filter classes
        int version = in.readInt();
        if (version != FORMAT_VERSION) {                    // defence 4: version check
            throw new IOException("Unsupported session format version: " + version);
        }
        Object payload = in.readObject();
        if (!(payload instanceof SessionSnapshot snapshot)) {
            throw new IOException("Session save does not contain a session snapshot.");
        }
        snapshot.validate();                                // defence 3: validate the domain state
        return snapshot;
    }
}

private static ObjectInputFilter.Status allowOnlySafeClasses(ObjectInputFilter.FilterInfo info) {
    Class<?> type = info.serialClass();
    if (type == null || type.isPrimitive()) {
        return ObjectInputFilter.Status.ALLOWED;
    }
    String name = type.getName();
    if (name.startsWith("com.basinwatch.") || name.startsWith("java.lang.")
            || name.startsWith("java.util.") || name.startsWith("java.time.")) {
        return ObjectInputFilter.Status.ALLOWED;
    }
    return ObjectInputFilter.Status.REJECTED;               // everything else is refused
}''', "from BasinWatch, io/SnapshotStore.java — all four defences in one method."))

B8.append(visual("""<p>Read the <span class='mono'>load</span> method as four gates. Gate one is the
size check, before the stream is even opened. Gate two is the filter, which runs on every class the
stream tries to construct. Gate three is the version check, immediately after the header. Gate four
is <span class='mono'>snapshot.validate()</span>, after the object exists. A file must pass all four
to be accepted.</p>"""))

B8.append("""
<h3><span class="n">8.7</span>What validation has to check</h3>
<p>Because deserialization skips constructors, the restored object can be structurally valid and
semantically impossible. The validation method is where the invariants are re-established.</p>
""")

B8.append(code('''public void validate() {
    if (tick < 0) {
        throw new IllegalStateException("Session tick cannot be negative.");
    }
    if (zones == null || zones.size() != 6) {
        throw new IllegalStateException("A session must describe exactly six zones.");
    }
    for (SavedZone zone : zones) {
        if (zone == null || zone.waterLevelMeters() < 0.0 || zone.waterLevelMeters() > 8.0) {
            throw new IllegalStateException("Session contains an impossible water level.");
        }
    }
    if (missions == null || resources == null || recentActivity == null) {
        throw new IllegalStateException("Session is missing a required section.");
    }
    for (Map.Entry<ResourceType, Integer> entry : resources.entrySet()) {
        if (entry.getValue() == null || entry.getValue() < 0) {
            throw new IllegalStateException("Session contains a negative resource count.");
        }
    }
}''', "from BasinWatch, io/SessionSnapshot.java — the invariants the constructors would have enforced."))

B8.append("""
<p>Notice that every check here corresponds to a rule that a constructor would normally apply: a
non-negative tick, exactly six zones, water levels inside the physical range, a non-negative
inventory. That correspondence is not a coincidence — it is the whole point. Validation after
deserialization exists to re-apply the rules that deserialization bypassed.</p>
""")

B8.append(connect("""<p>Compare this with the sensor archive in Chapter 6. The archive also has a
magic number and a version, but it never deserializes objects, so it needs no class filter — the
format is a fixed sequence of primitives that cannot name a class. That is a real advantage of the
data-stream approach and a real reason to prefer it where the shape is known.</p>"""))

B8.append("""
<h3><span class="n">8.8</span>Serialization versus the alternatives</h3>
<p>Object serialization is convenient and, as the previous section showed, needs care. Knowing when
it is the wrong tool is part of understanding it.</p>
""")

B8.append(table(
  ["Approach", "Stores", "Readable by", "Best for", "Used in BasinWatch for"],
  [
    ["Text with a character stream", "Characters", "a human, and any text tool", "Logs, reports, configuration", "The operational journal and reports"],
    ["Data streams", "Typed primitives in a fixed order", "a Java program that knows the format", "Measurement records, wire formats", "The sensor archive"],
    ["Object serialization", "An object graph with class descriptors", "a Java program with the same classes", "Whole-state save and restore", "Session snapshots"],
    ["A database", "Rows and columns", "any SQL client", "Selective queries over many records", "Optional SQLite history"],
    ["JSON or XML", "A structured text document", "almost anything", "Interchange with other languages", "<b>Not used</b> — see Chapter 18"],
  ],
  caption="<b>Table 8.3</b> — Five persistence formats and the question each answers."))

B8.append(exam("""<p>Questions on serialization cluster around four points: what makes a class
serializable; what <span class='mono'>transient</span> and <span class='mono'>static</span> do; why
the constructor is bypassed; and what <span class='mono'>serialVersionUID</span> is for. The
constructor point is the one that separates a memorised answer from an understood one — if you can
explain that the runtime allocates the object without invoking a constructor, and therefore that
validation must be repeated explicitly, you have answered all four coherently.</p>"""))

B8.append(summary([
  "Serialization converts an object graph into bytes; deserialization reconstructs it.",
  "A class must implement <span class='mono'>Serializable</span>, and every non-transient field must be serializable.",
  "<span class='mono'>transient</span> and <span class='mono'>static</span> fields are not written; a transient field restores to its default value.",
  "Deserialization bypasses constructors, so constructor validation does not run on restore.",
  "Declaring <span class='mono'>serialVersionUID</span> explicitly prevents unrelated recompiles from invalidating saved files.",
  "Default deserialization is unsafe: bound the size, filter the permitted classes, check a version, and validate the restored state.",
  "BasinWatch writes to a temporary file and moves it into place, so an interrupted save cannot corrupt an existing snapshot.",
]))

B8.append(keyterms([
  "<b>Serializable</b> — a marker interface permitting an object to be serialized.",
  "<b>serialVersionUID</b> — the explicit version identity of a serializable class.",
  "<b>transient</b> — a modifier excluding a field from serialization.",
  "<b>ObjectInputFilter</b> — a hook that approves or rejects each class a deserialization stream tries to construct.",
  "<b>Atomic move</b> — replacing a file in a single step, so no intermediate state is observable.",
]))

B8.append("</div>")

# ======================================================================
# CHAPTER 9
# ======================================================================
B9.append(chapter(9, "How BasinWatch Uses Java I/O",
"Four file mechanisms, four different purposes. This chapter consolidates Part II into a verified case study of the project's file layer."))

B9.append("""
<h3><span class="n">9.1</span>The design question, stated properly</h3>
<p>An application that needs to keep data could write everything to one file. BasinWatch uses four
different file mechanisms, and the reason is that each answers a different question.</p>
""")

B9.append(figure("d10_three_persistence", "11", "Three persistence mechanisms, three questions",
"File persistence split by the question it answers: a readable log for humans, a typed archive for measurements, and a versioned snapshot for whole-state recovery. The database column is the subject of Part III.",
"landscape"))

B9.append(table(
  ["Artefact", "The question it answers", "Mechanism", "Who reads it"],
  [
    ["<span class='mono'>operations.log</span>",
     "\u201cWhat has the application been doing?\u201d",
     "Character stream, UTF-8, append-only, line per event", "An operator, or a text editor"],
    ["<span class='mono'>sensors.bin</span>",
     "\u201cWhat exactly did the stations report?\u201d",
     "Byte stream with data-stream typing, header plus fixed records", "The program, during diagnosis"],
    ["<span class='mono'>*.bws</span>",
     "\u201cHow do I get the whole situation back?\u201d",
     "Object serialization of a versioned snapshot DTO, atomic replace", "The program, on restore"],
    ["<span class='mono'>*.txt</span> reports",
     "\u201cWhat is the situation right now?\u201d",
     "Character stream, UTF-8, one document per request", "A person, outside the application"],
  ],
  caption="<b>Table 9.1</b> — The four file artefacts and the question each one answers."))

B9.append(core("""<p>None of these four is interchangeable with the others, and that is the design
lesson of Part II. A log cannot restore a session because it records events, not state. A snapshot
cannot answer "what happened at 14:03" because it records only the present. An archive cannot be read
by a person because it is binary. A report cannot be queried because it is prose. Choosing the format
is choosing which questions the file will be able to answer.</p>"""))

B9.append("""
<h3><span class="n">9.2</span>Where the files live</h3>
<p>All paths are derived from one place, so the layout is defined once and cannot drift.</p>
""")

B9.append(code('''public final class AppPaths {
    private static final Path ROOT = Path.of("data");

    public static Path logsDirectory() { return ROOT.resolve("logs"); }
    public static Path logFile() { return logsDirectory().resolve("operations.log"); }
    public static Path archiveDirectory() { return ROOT.resolve("archive"); }
    public static Path archiveFile() { return archiveDirectory().resolve("sensors.bin"); }
    public static Path savesDirectory() { return ROOT.resolve("saves"); }
    public static Path lastSessionFile() { return savesDirectory().resolve("last-session.bws"); }
    public static Path reportsDirectory() { return ROOT.resolve("reports"); }

    public static void ensureDirectories() throws IOException {
        for (Path directory : List.of(logsDirectory(), archiveDirectory(),
                savesDirectory(), reportsDirectory())) {
            Files.createDirectories(directory);
        }
    }
}''', "from BasinWatch, io/AppPaths.java — one place that defines the on-disk layout."))

B9.append("""
<p>This small class is more important than it looks. Because every path comes from a method, there
are no string literals scattered through the codebase, and a test can reason about the layout
without touching the file system. It is the file-system equivalent of a schema.</p>
""")

B9.append("""
<h3><span class="n">9.3</span>The operational log</h3>
<p>This is the human-facing record. It is a character stream, it appends, and it flushes on a
policy.</p>
""")

B9.append(code('''data/logs/operations.log
2026-03-04T09:15:22.104Z | OBSERVATION | MIL rainfall 12.4 mm, rise 3.1 cm
2026-03-04T09:15:22.109Z | RISK | Risk increased: MIL WATCH -> WARNING
2026-03-04T09:15:31.882Z | ALLOCATED | Deploy portable pump -> NOR using PUMP x1, FIELD_CREW x1
2026-03-04T09:15:39.440Z | COMPLETE | Reinforce levee on UPR finished; levee reinforced''',
"from BasinWatch — the actual line format written by OperationalJournal."))

B9.append("""
<p>Four properties make this file useful, and each was a decision.</p>

<p><b>The timestamp is ISO-8601 with a Z suffix.</b> That is
<span class="mono">DateTimeFormatter.ISO_INSTANT</span>, which sorts lexicographically in the same
order as it sorts chronologically. A log that sorts correctly as text is a log you can grep.</p>

<p><b>The category is a separate field.</b> Because it is delimited by
<span class="mono">" | "</span>, an operator can filter for <span class="mono">RISK</span> or
<span class="mono">ALLOCATED</span> with ordinary text tools.</p>

<p><b>Newlines inside a message are replaced.</b> Chapter 5 covered this: it keeps one entry on one
line, which is what makes the file greppable in the first place.</p>

<p><b>Flushing is category-aware.</b> Routine observations can wait; warnings, completions and
allocations are written through immediately, because those are the entries an investigation would
want after a crash.</p>
""")

B9.append("""
<h3><span class="n">9.4</span>The typed sensor archive</h3>
<p>Where the log is for reading, the archive is for measurement. It stores exactly what each station
reported, in a format that cannot drift.</p>
""")

B9.append(code('''data/archive/sensors.bin
[ 4 bytes ] magic     0x42574154  ("BWAT")
[ 4 bytes ] version   1
   --- one record per accepted observation ---
[ 8 bytes ] tick                    long
[ 2+n     ] stationId               UTF
[ 2+n     ] zoneId                  UTF
[ 8 bytes ] rainfallMillimeters     double
[ 8 bytes ] observedRiseCentimeters double''',
"from BasinWatch — the sensor archive layout, as written by SensorArchive."))

B9.append(visual("""<p>Count the bytes of a typical record and you get a feel for why the format is
compact. A tick is 8 bytes. Two short identifiers, "MIL-ST-2" and "MIL", cost 2+7 and 2+3, so 14
bytes. Two doubles cost 16. The whole record is 38 bytes, plus the 8-byte header for the first one.
A text version of the same record would be roughly 45 characters and would need parsing and
locale-independent number formatting to read back.</p>"""))

B9.append("""
<h3><span class="n">9.5</span>The session snapshot</h3>
<p>The snapshot is the only artefact that can bring the application back to where it was. It is
written on request, and automatically on a clean shutdown, into
<span class="mono">last-session.bws</span>.</p>
""")

B9.append(code('''public static SessionSnapshot from(BasinSnapshot snapshot) {
    ArrayList<SavedZone> zones = new ArrayList<>();
    for (ZoneSnapshot zone : snapshot.zones()) {
        zones.add(new SavedZone(zone.id(), zone.name(), zone.waterLevelMeters(),
                zone.lastRainMillimeters(), zone.exposedResidents(),
                zone.leveeReinforced(), zone.lastReadingTick()));
    }
    ArrayList<SavedMission> missions = new ArrayList<>();
    for (MissionSnapshot mission : snapshot.activeMissions()) {
        missions.add(new SavedMission(mission.id(), mission.type().name(), mission.zoneId(),
                mission.startedTick(), mission.completesAtTick(), mission.status().name()));
    }
    return new SessionSnapshot(snapshot.tick(), List.copyOf(zones),
            Map.copyOf(snapshot.resources()), List.copyOf(missions),
            List.copyOf(snapshot.recentActivity()));
}''', "from BasinWatch, io/SessionSnapshot.java — a deliberate copy from immutable snapshots into serializable DTOs."))

B9.append(distinct("""<p><b>Why a separate <span class='mono'>SessionSnapshot</span> rather than
serializing <span class='mono'>BasinSnapshot</span> directly?</b> Three reasons, and all three
matter. First, the domain types may contain things that cannot or should not be serialized.
Second, the on-disk format should be a deliberate contract rather than an accident of the current
field list — a DTO lets the model change without changing the file. Third, records and enums carry
serialization constraints that plain final classes avoid. The DTO is a boundary object, and boundary
objects should be explicit.</p>"""))

B9.append("""
<h3><span class="n">9.6</span>Reports</h3>
<p>A report is a document, not a record. It is written once, read once, and never parsed.</p>
""")

B9.append(code('''BASINWATCH · SITUATION REPORT
Generated: 2026-03-04T09:16:02.331Z
Simulation tick: 214

ZONE CONDITIONS
  MIL  Middle Basin     2.71 m  WARNING   42 residents   12.4 mm last interval
  UPR  Upper Reach      3.62 m  CRITICAL  18 residents    9.8 mm last interval
  ...

RESOURCE BOARD
  PUMP            available 2 of 4
  FIELD_CREW      available 1 of 3
  ...

ACTIVE MISSIONS
  M-0007  Deploy portable pump -> NOR   started tick 208, completes tick 216

RECENT ACTIVITY
  09:15:22  OBSERVATION  MIL rainfall 12.4 mm, rise 3.1 cm
  ...''', "from BasinWatch — the report structure produced by ReportWriter."))

B9.append("""
<p>The report duplicates information that exists elsewhere, and that is correct. Its value is that it
is complete, self-contained and readable without the application. An operator can attach it to an
incident note; a reviewer can read it a year later. A format optimised for machine reading would be
worse at exactly that job.</p>
""")

B9.append(figure("d09_io_class_responsibilities", "12", "Which class uses which stream, and why",
"Every stream class in the project mapped to the class that uses it and the reason that stream was the right choice. The mapping is the argument of this chapter in one picture.",
"landscape"))

B9.append("""
<h3><span class="n">9.7</span>The four mechanisms side by side</h3>
""")

B9.append(table(
  ["", "Operational log", "Sensor archive", "Session snapshot", "Report"],
  [
    ["Stream family", "character (Writer)", "byte (DataOutputStream)", "byte (ObjectOutputStream)", "character (Writer)"],
    ["Unit of data", "one line per event", "one fixed record per observation", "one object graph", "one document"],
    ["Open mode", "append", "append, header if fresh", "replace, via temporary file", "replace, new name"],
    ["Reader", "a person", "the program", "the program", "a person"],
    ["Can restore state?", "no", "no", "yes", "no"],
    ["Can be queried?", "with text tools", "only by the program", "no", "no"],
    ["Versioned?", "no — append-only", "yes, in the header", "yes, before the object", "no"],
    ["Failure policy", "collect and report at the end", "worker thread reports", "propagate; the temp file is discarded", "propagate to the caller"],
  ],
  caption="<b>Table 9.2</b> — The four file mechanisms compared on the properties that matter."))

B9.append("""
<h3><span class="n">9.8</span>Why not one file for everything</h3>
<p>It is worth answering the obvious objection directly. Suppose you wrote everything to the log as
text. You would then face four problems.</p>

<ol>
<li><b>Restoring state would mean replaying.</b> To recover the model you would have to re-apply every
event ever logged, in order, and hope the replay logic still matches the original.</li>
<li><b>Numbers would lose precision.</b> A <span class="mono">double</span> printed as text and parsed
back may not be bit-identical, and any aggregation over thousands of readings would accumulate error.</li>
<li><b>Diagnosis would mean parsing.</b> A tool wanting "every reading for MIL above 20 mm" would have
to parse the whole file rather than seek.</li>
<li><b>One corrupt line would break everything.</b> A truncated final line in an append-only log is
normal after a crash; if that log were also the only save file, the session would be unrecoverable.</li>
</ol>

<p>Conversely, if everything were one binary snapshot, you would lose the audit trail entirely. The
four-mechanism design exists because the questions are genuinely different.</p>
""")

B9.append(exam("""<p>This chapter's comparison table is one of the highest-yield things in the book
for a viva. If asked "why does your project have both a log file and a database?", the answer follows
directly: the log records what happened, in order, for a human; the database records structured rows
that can be queried selectively. The log is an audit trail; the database is an index. Chapter 10
makes that distinction precise.</p>"""))

B9.append(summary([
  "BasinWatch has four file artefacts because each answers a different question: audit, measurement, recovery, communication.",
  "All paths derive from <span class='mono'>AppPaths</span>, so the on-disk layout is defined in exactly one place.",
  "The operational log is UTF-8 text, appended, with ISO-8601 timestamps and category-aware flushing.",
  "The sensor archive is binary with a magic number, a version and fixed typed records — compact and unambiguous, but unreadable by a person.",
  "The session snapshot serializes a deliberate DTO, not the live model, and writes through a temporary file.",
  "Reports are complete, self-contained documents that duplicate other data on purpose.",
  "None of the four mechanisms can substitute for another, because the format determines which questions the file can answer.",
]))

B9.append(keyterms([
  "<b>Audit trail</b> — an ordered record of what happened, for later inspection.",
  "<b>DTO (data transfer object)</b> — a deliberately separate object used at a boundary, such as persistence or the network.",
  "<b>Atomic replace</b> — writing to a temporary file then moving it into place so no partial state is visible.",
  "<b>Header</b> — metadata at the start of a binary file identifying its format and version.",
  "<b>Append-only</b> — a file opened so that existing content is never modified, only added to.",
]))

B9.append("</div>")

HTML = "".join(P + B4 + B5 + B6 + B7 + B8 + B9)
