"""Part I-II diagrams: architecture, concept map, streams, file I/O, serialization."""
from diagramkit import *  # noqa
from diagramkit import Canvas, SEM

SVG = "/workspace/book/assets/svg"
PNG = "/workspace/book/assets/png"


def d01_architecture_overview():
    c = Canvas(1180, 1000)
    c.title(40, 46, "Diagram 1 — BasinWatch: the complete Java system",
            "Verified runtime architecture. Every box is a real class in the repository.")
    c.text(1140, 46, "FULL PAGE", size=11, fill=MUTED, anchor="end",
           weight="bold", spacing="1.2")

    # --- user
    c.box(430, 74, 320, 52, "USER / OPERATOR", "Swing window · mouse, keyboard, zone selector",
          sem="navy", rx=26, title_size=13)
    c.arrow(590, 126, 590, 162)

    # --- Swing UI
    c.frame(60, 162, 1060, 118, "SWING USER INTERFACE  —  the event-dispatch thread (EDT)", "teal")
    c.box(84, 186, 232, 78, "MainFrame", ["JFrame · JButton · JList", "JSlider · Timer · panels"], sem="teal")
    c.box(330, 186, 232, 78, "BasinMapPanel", ["JPanel.paintComponent", "custom 2-D rendering"], sem="teal")
    c.box(576, 186, 232, 78, "DatabaseHistoryPanel", ["JTable + AbstractTableModel", "CompletableFuture consumer"], sem="teal")
    c.box(822, 186, 274, 78, "BasinWatchApp (main)", ["UIManager · SwingUtilities.invokeLater", "window listener"], sem="teal")
    c.arrow(590, 280, 590, 314)
    c.label(660, 300, "user actions call engine commands")

    # --- commands
    c.box(300, 314, 580, 48, "APPLICATION COMMANDS  —  BasinEngine public API",
          "start() · pause() · step() · dispatch() · injectStorm() · save() · load() · exportReport()",
          sem="purple", title_size=12.5, sub_size=11)
    c.arrow(590, 362, 590, 396)

    # --- engine
    c.frame(60, 396, 1060, 206, "DOMAIN / ENGINE LAYER  —  BasinEngine owns lifecycle", "purple")
    c.box(84, 420, 240, 76, "BasinModel (aggregate)", ["6 BasinZone · missions", "activity ring buffer · invariants"], sem="purple")
    c.box(340, 420, 200, 76, "ResourceAllocator", ["synchronized reserve/release", "all-or-nothing"], sem="purple")
    c.box(556, 420, 200, 76, "ResponseMission", ["progress by simulation tick", "PUMP / LEVEE / EVAC"], sem="purple")
    c.box(772, 420, 324, 76, "ResponseWorker × 3 (Runnable)", ["take() → process() → publish", "never blocks the EDT"], sem="purple")
    c.box(84, 508, 456, 76, "Immutable snapshots published to the EDT",
          ["BasinSnapshot → ZoneSnapshot / MissionSnapshot / ActivityEntry",
           "listeners wrapped in SwingUtilities.invokeLater"], sem="teal", title_size=12.5)
    c.box(556, 508, 540, 76, "EngineDiagnostics",
          ["thread states · queue depth · waiting consumers / producers · archive backlog"],
          sem="slate", title_size=12.5)

    # incoming path left
    c.arrow(200, 396, 200, 362, color=GREEN)
    c.arrow(200, 362, 200, 330, color=GREEN)
    c.label(200, 348, "events in", size=10.5, fill=GREEN)

    # --- sensor input path
    c.frame(60, 636, 1060, 108, "SENSOR INPUT / I-O PATH  —  character streams and a pipe", "green")
    c.box(84, 660, 214, 66, "SensorFeed (Thread)", ["writes encoded lines", "PipedWriter"], sem="green")
    c.arrow(300, 693, 344, 693, color=GREEN)
    c.label(322, 683, "pipe", size=10, fill=GREEN)
    c.box(346, 660, 214, 66, "SensorIntake (Runnable)", ["BufferedReader.readLine", "parse + validate"], sem="green")
    c.arrow(562, 693, 606, 693, color=GREEN)
    c.box(608, 660, 230, 66, "EventBuffer (bounded 96)", ["put() waits / take() waits", "wait() + notifyAll()"], sem="green")
    c.arrow(840, 693, 884, 693, color=GREEN)
    c.box(886, 660, 210, 66, "ArchiveWorker (Thread)", ["ArrayBlockingQueue", "SensorArchive"], sem="green")

    # --- persistence split
    c.arrow(590, 744, 590, 782)
    c.box(330, 782, 520, 44, "ACCEPTED EVENTS  —  persisted on separate paths", None,
          sem="slate", title_size=12.5, rx=22)
    c.arrow(590, 826, 590, 852)
    c.line(300, 852, 880, 852, stroke=MUTED, sw=1.6)
    c.arrow(300, 852, 300, 880)
    c.arrow(880, 852, 880, 880)

    # --- file persistence
    c.frame(60, 880, 520, 96, "FILE PERSISTENCE  —  java.io", "amber")
    c.box(80, 902, 152, 58, "Journal / Report", ["BufferedWriter", "UTF-8 text"], sem="amber", title_size=11.5)
    c.box(244, 902, 152, 58, "SensorArchive", ["DataOutputStream", "typed binary"], sem="amber", title_size=11.5)
    c.box(408, 902, 152, 58, "SnapshotStore", ["ObjectOutputStream", "atomic replace"], sem="amber", title_size=11.5)

    # --- jdbc
    c.frame(600, 880, 520, 96, "JDBC LAYER  —  java.sql", "red")
    c.box(620, 902, 232, 58, "DatabaseService", ["1-thread executor", "optional · off-EDT"], sem="red", title_size=11.5)
    c.box(864, 902, 240, 58, "Repositories → SQLite", ["PreparedStatement", "ResultSet · transactions"], sem="red", title_size=11.5)
    c.arrow(880, 902, 880, 852, color=RED)
    c.arrow(984, 902, 984, 840, color=RED)
    c.label(1060, 872, "history read back to Swing", size=10.5, fill=RED, anchor="end")

    c.save("d01_architecture_overview", SVG, PNG, 1.9)


def d02_concept_map():
    c = Canvas(1180, 900)
    c.title(40, 44, "Diagram 2 — Java concepts connection map",
            "One page that places every syllabus concept inside the running application.")
    c.text(1140, 44, "FULL PAGE", size=11, fill=MUTED, anchor="end", weight="bold",
           spacing="1.2")

    c.box(400, 66, 380, 46, "BASINWATCH — ONE RUNNING JAVA APPLICATION", None,
          sem="navy", rx=23, title_size=12.5)

    cols = [
        (40, "LANGUAGE FOUNDATIONS", "purple", [
            ("Classes & objects", "BasinModel, BasinZone"),
            ("Interfaces", "BasinEvent contract"),
            ("Polymorphism", "process(BasinEvent)"),
            ("Inheritance", "SensorFeed extends Thread"),
            ("Enums", "RiskLevel, MissionType"),
            ("Records", "SensorReading, snapshots"),
            ("Encapsulation", "private fields + methods"),
            ("POJO vs JavaBean", "record vs getX/setX"),
        ]),
        (320, "JAVA I/O", "amber", [
            ("Byte streams", "SensorArchive file"),
            ("Character streams", "operations.log"),
            ("Buffered streams", "BufferedWriter / BufferedOutputStream"),
            ("Data streams", "writeInt / writeUTF / writeDouble"),
            ("File & metadata", "AppPaths, SaveCatalog"),
            ("Serialization", "SessionSnapshot"),
            ("Byte-array streams", "in-memory save payload"),
            ("Piped streams", "feed → intake pipe"),
        ]),
        (600, "CONCURRENCY", "green", [
            ("Thread", "SensorFeed, ArchiveWorker"),
            ("Runnable", "SensorIntake, ResponseWorker"),
            ("Monitors", "EventBuffer, allocator"),
            ("wait / notifyAll", "bounded queue signalling"),
            ("Producer / consumer", "feed → buffer → workers"),
            ("interrupt / join", "orderly shutdown"),
            ("Deadlock avoidance", "one short inventory lock"),
            ("Priority (hint only)", "archive worker experiment"),
        ]),
        (880, "DATA, UI & BUILD", "red", [
            ("JDBC driver", "sqlite-jdbc in pom.xml"),
            ("Connection", "openConnection()"),
            ("PreparedStatement", "parameter binding"),
            ("ResultSet", "findRecent mapping"),
            ("Transactions", "commit / rollback"),
            ("Swing components", "JFrame, JTable, JPanel"),
            ("Event handling", "ActionListener → engine"),
            ("Maven & pom.xml", "dependency → jar"),
        ]),
    ]
    for x, head, sem, items in cols:
        c.band(x, 140, 260, 38, head, sem, size=12)
        y = 196
        for name, where in items:
            c.rect(x, y, 260, 56, fill=PAPER, stroke=BORDER, rx=7, sw=1.2)
            c.rect(x, y, 4, 56, fill=SEM[sem][2], stroke=SEM[sem][2], rx=2, sw=0)
            c.text(x + 13, y + 22, name, size=11.5, fill=INK, weight="bold")
            c.text(x + 13, y + 40, where, size=10.2, fill=MUTED)
            y += 63
        c.arrow(x + 130, 140, x + 130, 128, color=SEM[sem][2], head=False)
        c.line(x + 130, 128, 590, 128, stroke=BORDER, sw=1.2)
        c.arrow(590, 128, 590, 114, color=NAVY)

    c.note(40, 712, 1100,
           ["Reading the map: each concept belongs to a real component. Chapters 4–8 build the I/O column, "
            "Chapters 10–14 the database column, Chapter 15–16 the interface column.",
            "The arrows point inward because every technology exists to serve one application, not four separate subjects."],
           sem="teal", size=11.5)
    c.save("d02_concept_map", SVG, PNG, 1.9)


def d03_byte_vs_char():
    c = Canvas(1180, 720)
    c.title(40, 44, "Diagram 5 — Byte streams versus character streams",
            "The same file is a sequence of bytes; a character stream adds encoding on top.")

    # byte side
    c.frame(40, 70, 530, 520, "BYTE-ORIENTED  ·  java.io.InputStream / OutputStream", "teal")
    c.box(70, 104, 470, 54, "8-bit units — raw bytes, no text interpretation", None,
          sem="teal", title_size=12.5, rx=10)
    y = 182
    c.text(70, y, "A file on disk (sensors.bin)", size=12, fill=INK, weight="bold")
    c.rect(70, y + 12, 470, 46, fill=CANVAS, stroke=BORDER, rx=6)
    for i, b in enumerate(["00", "42", "57", "41", "52", "00", "00", "00", "01", "3F", "F0"]):
        c.rect(80 + i * 41, y + 22, 34, 26, fill=PAPER, stroke=TEAL, rx=4, sw=1.1)
        c.mtext(97 + i * 41, y + 39, b, size=10.5, anchor="middle", fill=TEAL)
    c.text(70, y + 82, "…  bytes have no letters, no newlines, no charset", size=11, fill=MUTED, italic=True)

    c.text(70, y + 130, "BasinWatch: SensorArchive", size=12, fill=INK, weight="bold")
    c.mtext(70, y + 152, "output.writeLong(tick);", size=11.5)
    c.mtext(70, y + 172, "output.writeUTF(stationId);", size=11.5)
    c.mtext(70, y + 192, "output.writeDouble(rainfall);", size=11.5)
    c.text(70, y + 222, "Typed and compact. Rebuilt by reading in the same order.",
           size=11, fill=MUTED)
    c.box(70, y + 242, 470, 84, "WHEN TO USE",
          ["Binary payloads, images, typed measurements, serialized objects,",
           "anything that must survive byte-for-byte."], sem="slate", title_size=12)

    # char side
    c.frame(610, 70, 530, 520, "CHARACTER-ORIENTED  ·  java.io.Reader / Writer", "amber")
    c.box(640, 104, 470, 54, "16-bit units — text, with an explicit charset", None,
          sem="amber", title_size=12.5, rx=10)
    y = 182
    c.text(640, y, "The same idea, as text (operations.log)", size=12, fill=INK, weight="bold")
    c.rect(640, y + 12, 470, 46, fill=CANVAS, stroke=BORDER, rx=6)
    for i, ch in enumerate(["1", "7", ":", "0", "4", " ", "|", " ", "S", "Y", "S"]):
        c.rect(650 + i * 41, y + 22, 34, 26, fill=PAPER, stroke=AMBER, rx=4, sw=1.1)
        c.mtext(667 + i * 41, y + 39, ch, size=10.5, anchor="middle", fill=AMBER)
    c.text(640, y + 82, "…  characters map to bytes through UTF-8 when written", size=11,
           fill=MUTED, italic=True)

    c.text(640, y + 130, "BasinWatch: OperationalJournal", size=12, fill=INK, weight="bold")
    c.mtext(640, y + 152, "writer.write(entry.message());", size=11.5)
    c.mtext(640, y + 172, "writer.newLine();", size=11.5)
    c.mtext(640, y + 192, "writer.flush();", size=11.5)
    c.text(640, y + 222, "Readable by a human and by any text tool. Newlines are real.",
           size=11, fill=MUTED)
    c.box(640, y + 242, 470, 84, "WHEN TO USE",
          ["Logs, reports, configuration, CSV, anything a person",
           "must open and read without a program."], sem="slate", title_size=12)

    c.arrow(575, 330, 605, 330, color=MUTED, head=False)
    c.arrow(605, 330, 575, 330, color=MUTED, head=False)
    c.label(590, 322, "encodes / decodes", size=10, fill=MUTED)
    c.save("d03_byte_vs_char", SVG, PNG, 1.9)


def d04_io_hierarchy():
    c = Canvas(1180, 880)
    c.title(40, 44, "Diagram 6 — The Java I/O class hierarchies",
            "Four abstract roots. Concrete classes specialise the source or destination.")

    def tree(x, y, root, children, sem, w=250):
        c.box(x, y, w, 46, root, None, sem=sem, rx=8, title_size=13)
        yy = y + 62
        for name, note in children:
            c.line(x + 30, yy - 16, x + 30, yy - 8, stroke=SEM[sem][2], sw=1.4)
            c.line(x + 30, yy - 8, x + 30, yy, stroke=SEM[sem][2], sw=1.4)
            c.box(x, yy, w, 42, name, note, sem="white", rx=7, title_size=11.5,
                  sub_size=9.5, title_fill=INK, sub_fill=MUTED, pad=8)
            yy += 52
        return yy

    tree(40, 76, "InputStream", [
        ("FileInputStream", "bytes from a file"),
        ("ByteArrayInputStream", "bytes from a byte[]"),
        ("PipedInputStream", "bytes from a connected pipe"),
        ("FilterInputStream", "base for wrappers"),
        ("BufferedInputStream", "adds a memory buffer"),
        ("DataInputStream", "reads int / double / UTF"),
        ("ObjectInputStream", "reads serialized objects"),
    ], "teal")

    tree(320, 76, "OutputStream", [
        ("FileOutputStream", "bytes to a file"),
        ("ByteArrayOutputStream", "grows an in-memory byte[]"),
        ("PipedOutputStream", "bytes to a connected pipe"),
        ("FilterOutputStream", "base for wrappers"),
        ("BufferedOutputStream", "adds a memory buffer"),
        ("DataOutputStream", "writes int / double / UTF"),
        ("ObjectOutputStream", "writes serialized objects"),
    ], "green")

    tree(610, 76, "Reader", [
        ("FileReader", "characters from a file"),
        ("InputStreamReader", "bytes → characters"),
        ("BufferedReader", "readLine() and buffering"),
        ("PipedReader", "characters from a connected pipe"),
        ("StringReader", "characters from a String"),
    ], "amber")

    tree(890, 76, "Writer", [
        ("FileWriter", "characters to a file"),
        ("OutputStreamWriter", "characters → bytes"),
        ("BufferedWriter", "buffering and newLine()"),
        ("PipedWriter", "characters to a connected pipe"),
        ("StringWriter", "characters into a String"),
    ], "purple")

    c.note(40, 500, 1100,
           ["The four roots are abstract. You never write new InputStream(); you choose a concrete source or destination.",
            "Wrapper classes take another stream in their constructor — that is what makes layering possible (see Diagram 5)."],
           sem="teal", size=11.5)
    c.box(40, 596, 1100, 118, "THE DECORATOR PATTERN IN ONE SENTENCE",
          ["A concrete stream (FileOutputStream) supplies the destination. Each wrapper (BufferedOutputStream,",
           "DataOutputStream) adds exactly one responsibility and passes everything else through to the stream it wraps.",
           "The result is a chain that behaves like one stream but performs several jobs."],
          sem="navy", title_size=13, sub_size=11.5, title_fill=NAVY, sub_fill=BODY)
    c.box(40, 730, 1100, 110, "HOW BASINWATCH LAYERS THEM",
          ["SnapshotStore.save():  byte[] payload  →  BufferedOutputStream( Files.newOutputStream(temp) )",
           "SensorArchive():       SensorReading  →  DataOutputStream( BufferedOutputStream( file ) )",
           "BasinEngine feed:      PipedWriter  →  PipedReader(8192)  →  BufferedReader"],
          sem="slate", title_size=12.5, sub_size=11, title_fill=INK, sub_fill=BODY)
    c.save("d04_io_hierarchy", SVG, PNG, 1.9)


def d05_wrapped_streams():
    c = Canvas(1180, 780)
    c.title(40, 44, "Diagram 8 — Wrapped and buffered streams",
            "Data written by the application travels down the wrapper chain to the device.")

    # layered stack
    layers = [
        ("APPLICATION CODE", "archive.append(reading)", "purple", 470, 70),
        ("DataOutputStream", "writeLong · writeUTF · writeDouble — adds TYPES", "teal", 470, 70),
        ("BufferedOutputStream", "collects bytes in an 8 KB array — adds BATCHING", "green", 470, 70),
        ("Files.newOutputStream(path)", "operating-system file handle — the real destination", "amber", 470, 70),
        ("data/archive/sensors.bin", "bytes on disk", "slate", 470, 70),
    ]
    y = 84
    for i, (name, note, sem, w, h) in enumerate(layers):
        c.box(70, y, w, h, name, note, sem=sem, rx=10, title_size=13, sub_size=11)
        if i < len(layers) - 1:
            c.arrow(305, y + h, 305, y + h + 22)
        y += h + 22

    # buffer detail
    c.frame(600, 84, 540, 300, "WHAT THE BUFFER ACTUALLY DOES", "green")
    c.text(624, 122, "Without buffering — one call per field", size=11.5, fill=INK,
           weight="bold")
    for i in range(6):
        c.rect(624 + i * 44, 134, 36, 26, fill=RED_L, stroke=RED, rx=4, sw=1.1)
        c.mtext(642 + i * 44, 151, "sys", size=9, anchor="middle", fill=RED)
    c.text(624, 182, "writeLong → writeUTF → writeDouble → writeUTF … each reaches the OS",
           size=10.5, fill=MUTED)
    c.text(624, 222, "With buffering — one call per full buffer", size=11.5, fill=INK,
           weight="bold")
    c.rect(624, 234, 264, 30, fill=GREEN_L, stroke=GREEN, rx=5, sw=1.3)
    c.mtext(756, 254, "8 KB byte[]  in memory", size=10.5, anchor="middle", fill=GREEN)
    c.arrow(900, 249, 942, 249, color=GREEN)
    c.rect(946, 234, 60, 30, fill=RED_L, stroke=RED, rx=5, sw=1.1)
    c.mtext(976, 254, "sys", size=9.5, anchor="middle", fill=RED)
    c.text(624, 292, "Many small logical writes collapse into few large physical writes.",
           size=10.5, fill=MUTED)
    c.text(624, 312, "Flush pushes the tail out; close() flushes and releases the handle.",
           size=10.5, fill=MUTED)
    c.text(624, 340, "In BasinWatch, flush happens per accepted batch and on close().",
           size=10.5, fill=TEAL, weight="bold")

    # reading side
    c.frame(600, 400, 540, 300, "READING REVERSES THE SAME CHAIN", "teal")
    rl = [
        ("new FileInputStream(path)", "raw bytes from disk", "amber"),
        ("new BufferedInputStream(...)", "one 8 KB read serves many small reads", "green"),
        ("new DataInputStream(...)", "readInt · readUTF · readDouble — typed values back", "teal"),
    ]
    yy = 436
    for name, note, sem in rl:
        c.box(624, yy, 492, 56, name, note, sem=sem, rx=8, title_size=11.8,
              sub_size=10.5)
        c.arrow(870, yy + 56, 870, yy + 72)
        yy += 72
    c.box(624, yy, 492, 58, "SensorArchive header check",
          ["readInt() != MAGIC  →  IOException(\"marker or format version is invalid\")"],
          sem="slate", rx=8, title_size=11.8, sub_size=10.2)
    c.text(624, 690, "Order matters: values must be read in exactly the order they were written.",
           size=11, fill=MUTED)
    c.save("d05_wrapped_streams", SVG, PNG, 1.9)


def d06_piped_producer_consumer():
    c = Canvas(1180, 760)
    c.title(40, 44, "Diagram 9 — Piped streams: a producer, a consumer, and a thread boundary",
            "SensorFeed and SensorIntake run on different threads and never call each other directly.")

    c.box(60, 96, 250, 96, "SensorFeed", ["extends Thread", "\"basin-sensor-feed\""],
          sem="green", title_size=14)
    c.box(60, 214, 250, 74, "loop each interval", ["build SensorReading", "encode() → one text line"],
          sem="white", title_size=12, sub_size=10.5)

    # pipe
    c.rect(370, 96, 220, 300, fill=TEAL_LIGHT, stroke=TEAL, rx=14, sw=1.6)
    c.text(480, 128, "THE PIPE", size=12.5, fill=INK, anchor="middle",
           weight="bold", spacing="1")
    c.text(480, 150, "PipedWriter → PipedReader", size=10.5, fill=TEAL,
           anchor="middle")
    for i in range(7):
        c.rect(392, 168 + i * 32, 176, 24, fill=PAPER, stroke=TEAL, rx=4, sw=1)
        c.mtext(404, 185 + i * 32, ["READ|42|G-MIL|MIL|17.500|3.200",
                                    "READ|42|G-NOR|NOR|9.100|1.400",
                                    "PULSE|42", "…", "8 192-character buffer",
                                    "writer blocks when full", "reader blocks when empty"][i],
                size=9.3, fill=TEAL if i < 3 else MUTED)

    c.box(660, 96, 250, 96, "SensorIntake", ["implements Runnable", "\"basin-sensor-intake\""],
          sem="teal", title_size=14)
    c.box(660, 214, 250, 74, "readLine() loop", ["parse + validate record", "enqueue or discard"],
          sem="white", title_size=12, sub_size=10.5)
    c.box(660, 310, 250, 74, "malformed record?", ["warningReporter.accept(...)", "continue — no crash"],
          sem="amber", title_size=12, sub_size=10.5)

    c.arrow(310, 144, 368, 144, color=GREEN, sw=2.2)
    c.label(339, 134, "write()", size=10.5, fill=GREEN)
    c.arrow(658, 144, 592, 144, color=TEAL, sw=2.2)
    c.label(625, 134, "read()", size=10.5, fill=TEAL)
    c.arrow(785, 288, 785, 308)

    c.box(960, 96, 180, 96, "EventBuffer", ["bounded 96", "put() / take()"],
          sem="purple", title_size=13)
    c.arrow(912, 144, 958, 144, color=PURPLE, sw=2.2)

    c.box(960, 214, 180, 74, "3 ResponseWorkers", ["consume events", "process + persist"],
          sem="purple", title_size=12, sub_size=10.5)

    c.note(60, 420, 1080,
           ["Why a pipe at all?  It gives the feed a real blocking endpoint, so intake can wait for data instead of",
            "polling a shared list. The two threads share no mutable object — they share a stream, which is a much",
            "narrower contract. This is the textbook piped-stream idea used for a genuine purpose."],
           sem="green", size=11.5)

    c.box(60, 540, 1080, 76, "WHAT BELONGS TO WHOM",
          ["The PIPE owns transport and back-pressure  ·  the THREAD owns execution and lifecycle  ·  ",
           "the BUFFER owns queuing policy  ·  the MODEL owns domain state and invariants."],
          sem="navy", title_size=13, sub_size=11.5, title_fill=NAVY, sub_fill=BODY)
    c.note(60, 640, 1080,
           ["Blocking read: readLine() returns null only when the writer closes. Shutdown therefore closes the",
            "writer (SensorFeed.requestStop) so intake ends its loop naturally instead of being killed."],
           sem="teal", size=11.5)
    c.save("d06_piped_producer_consumer", SVG, PNG, 1.9)


def d07_file_lifecycle():
    c = Canvas(1180, 800)
    c.title(40, 44, "Diagram 7 — File persistence lifecycles in BasinWatch",
            "Four different files, four different reasons. None is a substitute for another.")

    lanes = [
        ("operations.log", "OperationalJournal", "amber",
         ["open: Files.newBufferedWriter(CREATE, APPEND, UTF-8)",
          "append: timestamp | category | message + newLine()",
          "flush: every 12 lines, or on WARNING / COMPLETE / ALLOCATED",
          "close: flush() then close() — journal.close() on shutdown"],
         "Human-readable audit trail"),
        ("sensors.bin", "SensorArchive + ArchiveWorker", "teal",
         ["open: check MAGIC 0x42574152 and version, else write header",
          "append: writeLong tick, writeUTF station, writeUTF zone, 2 × writeDouble",
          "worker: ArrayBlockingQueue(512) drained on its own thread",
          "close: finish() sentinel → archive.close()"],
         "Typed measurements for replay"),
        ("*.bws", "SnapshotStore + SessionSnapshot", "purple",
         ["save: encode() → byte[] in memory (ByteArrayOutputStream)",
          "write: BufferedOutputStream to a temporary sibling file",
          "replace: Files.move(ATOMIC_MOVE, REPLACE_EXISTING) — fallback plain move",
          "failure: temporary file is deleted in a finally block"],
         "Recoverable session state"),
        ("*.txt report", "ReportWriter", "green",
         ["name: basin-status-<yyyyMMdd-HHmmss>-<uuid8>.txt",
          "write: try-with-resources BufferedWriter, UTF-8",
          "content: zones, resources, missions, recent activity",
          "close: automatic at the end of the try block"],
         "Operator-readable summary"),
    ]
    y = 82
    for name, owner, sem, steps, purpose in lanes:
        c.rect(40, y, 1100, 158, fill=PAPER, stroke=BORDER, rx=10, sw=1.3)
        c.rect(40, y, 6, 158, fill=SEM[sem][2], stroke=SEM[sem][2], rx=3, sw=0)
        c.text(64, y + 30, name, size=14, fill=INK, weight="bold", font=MONO)
        c.text(64, y + 50, owner, size=11, fill=MUTED)
        c.text(64, y + 138, purpose, size=11, fill=SEM[sem][2], weight="bold")
        xx = 300
        for i, s in enumerate(steps):
            c.rect(xx, y + 20, 200, 118, fill=CANVAS, stroke=BORDER, rx=7, sw=1.1)
            c.text(xx + 10, y + 40, f"STEP {i+1}", size=9, fill=MUTED,
                   weight="bold", spacing="0.8")
            words = s.split(" ")
            lines, cur = [], ""
            for w in words:
                if len(cur) + len(w) > 25:
                    lines.append(cur)
                    cur = w
                else:
                    cur = (cur + " " + w).strip()
            lines.append(cur)
            c.lines(xx + 10, y + 60, lines[:6], size=9.6, fill=BODY, lh=13)
            if i < len(steps) - 1:
                c.arrow(xx + 200, y + 79, xx + 222, y + 79, color=MUTED, sw=1.5)
            xx += 222
        y += 170

    c.note(40, 762, 1100,
           ["Compare with Diagram 20 (persistence matrix): a log is append-only text, an archive is typed binary,",
            "a snapshot is a whole-object replacement, and a report is a throw-away artefact for a person."],
           sem="slate", size=11)
    c.save("d07_file_lifecycle", SVG, PNG, 1.9)


def d08_serialization():
    c = Canvas(1180, 820)
    c.title(40, 44, "Diagram 10 — Serialization, validation and session restoration",
            "How a live object graph becomes a safe file and comes back as a validated model.")

    # save side
    c.frame(40, 76, 530, 420, "SAVE  ·  live model → bytes", "purple")
    steps = [
        ("BasinSnapshot", "immutable record from model.snapshot()"),
        ("SessionSnapshot.from()", "copies into serializable DTOs"),
        ("SavedZone[] / SavedMission[] / SavedActivity[]", "plain fields, serialVersionUID = 1"),
        ("ObjectOutputStream → ByteArrayOutputStream", "encode() returns byte[]"),
        ("size check  ≤ 5 MB", "reject oversized payloads"),
        ("BufferedOutputStream → temporary file", "\"<name>.pending\" beside the target"),
        ("Files.move(ATOMIC_MOVE, REPLACE_EXISTING)", "fallback: plain move"),
    ]
    y = 110
    for i, (t, s) in enumerate(steps):
        c.box(66, y, 478, 46, t, s, sem="purple" if i < 4 else "slate", rx=8,
              title_size=11.5, sub_size=10, pad=8)
        if i < len(steps) - 1:
            c.arrow(305, y + 46, 305, y + 54, color=PURPLE, sw=1.6)
        y += 54

    # load side
    c.frame(610, 76, 530, 420, "LOAD  ·  bytes → validated model", "teal")
    lsteps = [
        ("Files.isRegularFile + size 1…5 MB", "cheap guards before decoding"),
        ("BufferedInputStream.readNBytes", "read at most limit + 1 byte"),
        ("ObjectInputStream.setObjectInputFilter", "depth ≤ 12, refs ≤ 2000, bytes ≤ 5 MB"),
        ("class allowlist", "SessionSnapshot, Saved*, String, primitives"),
        ("instanceof SessionSnapshot", "reject any other object graph"),
        ("version == CURRENT_VERSION", "else \"unsupported format version\""),
        ("invariant validation", "6 zones · resource balance · mission limits"),
        ("BasinModel.restore(snapshot)", "rebuild locks, allocator and threads fresh"),
    ]
    y = 110
    for i, (t, s) in enumerate(lsteps):
        c.box(636, y, 478, 42, t, s, sem="teal" if i < 5 else "slate", rx=8,
              title_size=11, sub_size=9.6, pad=7)
        if i < len(lsteps) - 1:
            c.arrow(875, y + 42, 875, y + 48, color=TEAL, sw=1.5)
        y += 48

    c.box(40, 514, 1100, 96, "WHAT IS DELIBERATELY NOT SERIALIZED",
          ["Locks, monitors, running threads, open streams, Swing components and the ResourceAllocator itself.",
           "These are runtime resources, not data. They are recreated after load so the restored model is safe and consistent.",
           "BasinWatch also declares a transient field (sourcePathHint) to prove the point in code."],
          sem="red", title_size=12.5, sub_size=11, title_fill=INK, sub_fill=BODY)

    c.note(40, 628, 1100,
           ["TECHNICAL CLARIFICATION: plain Java serialization is not a safe way to read files from untrusted sources.",
            "Deserializing attacker-controlled bytes can construct arbitrary objects and run their code. BasinWatch reduces",
            "the risk with an ObjectInputFilter, an allowlist and size limits — and still treats saves as local app data only."],
           sem="amber", size=11.5)
    c.box(40, 742, 1100, 56, "The lesson",
          ["Serialization solves state capture. It does not, by itself, solve trust, validation or versioning — those must be added."],
          sem="navy", title_size=12.5, title_fill=NAVY)
    c.save("d08_serialization", SVG, PNG, 1.9)


def d09_io_class_responsibilities():
    c = Canvas(1180, 700)
    c.title(40, 44, "Diagram 12 — Which BasinWatch class uses which stream, and why",
            "Nine I/O classes, one purpose each. Choosing the wrong one changes the meaning of the data.")

    rows = [
        ["Class", "Stream family", "What it stores", "Why that family"],
        ["AppPaths", "java.nio.file.Path / Files", "directory layout and the database path", "Paths are metadata, not content"],
        ["SaveCatalog", "java.io.File", "list of *.bws saves, newest first", "Listing needs metadata only"],
        ["OperationalJournal", "BufferedWriter (Writer)", "timestamped audit lines, UTF-8", "Humans must read it"],
        ["ReportWriter", "BufferedWriter (Writer)", "a formatted situation report", "A report is text by definition"],
        ["SensorArchive", "DataOutputStream", "typed tick / station / rain / rise", "Values must keep their types"],
        ["ArchiveWorker", "ArrayBlockingQueue + Thread", "off-thread archive writes", "Disk latency must not block intake"],
        ["SnapshotStore", "ObjectOutputStream", "the whole session object graph", "Whole-object state capture"],
        ["SensorFeed", "PipedWriter (Writer)", "encoded observation lines", "Blocking hand-off to intake"],
        ["SensorIntake", "BufferedReader (Reader)", "parsed and validated events", "readLine() matches the format"],
    ]
    c.table(40, 80, [230, 250, 320, 300], rows, row_h=44, size=11.5)
    c.note(40, 588, 1100,
           ["Notice the deliberate split: readable text for people, typed binary for machines, object serialization for",
            "state, and metadata for discovery. This is the practical answer to \"which persistence mechanism should I use?\""],
           sem="teal", size=11.5)
    c.save("d09_io_class_responsibilities", SVG, PNG, 1.9)


ALL = [d01_architecture_overview, d02_concept_map, d03_byte_vs_char,
       d04_io_hierarchy, d05_wrapped_streams, d06_piped_producer_consumer,
       d07_file_lifecycle, d08_serialization, d09_io_class_responsibilities]
