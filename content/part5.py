"""PART V — Configuration and Related Techniques.  Chapters 17-19."""
from . import *

P = []
B17, B18, B19 = [], [], []

P.append("""
<div class="part-page">
  <div class="pnum">PART V</div>
  <h1>Configuration and Related Techniques</h1>
  <div class="prule"></div>
  <div class="pintro">An application is more than its source files. This part explains how
  dependencies reach the classpath, how a build produces a runnable artefact, what XML, schemas,
  namespaces and annotations are for, and how Spring's JdbcTemplate relates to the raw JDBC you have
  just studied.</div>
  <div class="chapters">
    <div><span>17</span>Maven, pom.xml and Project Dependencies</div>
    <div><span>18</span>XML, Schemas, Namespaces, Annotations and JavaBeans</div>
    <div><span>19</span>Raw JDBC versus Spring JdbcTemplate</div>
  </div>
</div>
""")

# ======================================================================
# CHAPTER 17
# ======================================================================
B17.append(chapter(17, "Maven, pom.xml and Project Dependencies",
"How a Java project declares what it needs, how the build turns source into a runnable artefact, and why the JDBC driver is on the classpath at all."))

B17.append("""
<h3><span class="n">17.1</span>The problem a build tool solves</h3>
<p>Compiling a single file is easy: <span class="mono">javac Hello.java</span>. Compiling a project is
not. A real project has hundreds of source files, depends on third-party libraries, needs those
libraries' own dependencies, must be compiled in the right order, and must be packaged into something
distributable. Doing all of that by hand does not scale.</p>

<p>A build tool automates four things: resolving dependencies, compiling, testing, and packaging. Maven
is one such tool, and it is the one BasinWatch uses.</p>
""")

B17.append(defbox("Build tool",
"a program that reads a project description, downloads and resolves the libraries the project depends on, compiles the sources in the correct order, runs tests, and produces a packaged artefact."))

B17.append(figure("d22_maven_build", "25", "The Maven build workflow",
"The pom.xml declares coordinates, dependencies and plugins. Maven resolves the dependency tree from a repository into the local cache, compiles the sources against that classpath, runs the tests, and packages the result. The shade plugin then merges the dependency classes into one runnable jar.",
"portrait"))

B17.append("""
<h3><span class="n">17.2</span>Coordinates: how a dependency is named</h3>
<p>Maven identifies every library by three values, and it identifies your project the same way.</p>
""")

B17.append(table(
  ["Coordinate", "Meaning", "BasinWatch's project", "The SQLite driver"],
  [
    ["<span class='mono'>groupId</span>", "The organisation or namespace", "<span class='mono'>com.basinwatch</span>", "<span class='mono'>org.xerial</span>"],
    ["<span class='mono'>artifactId</span>", "The project or library name", "<span class='mono'>basinwatch</span>", "<span class='mono'>sqlite-jdbc</span>"],
    ["<span class='mono'>version</span>", "The release identifier", "<span class='mono'>1.0.0</span>", "<span class='mono'>3.50.3.0</span>"],
  ],
  caption="<b>Table 17.1</b> — Maven coordinates, for this project and for its one dependency."))

B17.append(core("""<p>Those three values are the complete address of a jar in a repository. Given
<span class='mono'>org.xerial:sqlite-jdbc:3.50.3.0</span>, Maven can find, download and cache the exact
file — and it does the same for every library that library itself needs. That transitive resolution is
the main reason build tools replaced hand-managed jars.</p>"""))

B17.append("""
<h3><span class="n">17.3</span>The pom.xml, section by section</h3>
<p>The Project Object Model is the project's description. BasinWatch's is short, and every section has a
purpose.</p>
""")

B17.append(code('''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.basinwatch</groupId>
    <artifactId>basinwatch</artifactId>
    <version>1.0.0</version>
    <name>BasinWatch</name>
    <description>Offline floodplain operations console and planning simulation</description>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <maven.compiler.release>17</maven.compiler.release>
        <sqlite-jdbc.version>3.50.3.0</sqlite-jdbc.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.xerial</groupId>
            <artifactId>sqlite-jdbc</artifactId>
            <version>${sqlite-jdbc.version}</version>
        </dependency>
    </dependencies>
    <!-- build section follows -->
</project>''', "from BasinWatch, pom.xml — coordinates, properties and the single dependency.", lang="none"))

B17.append("""
<p>Three things are worth pointing out.</p>

<p><b>There is exactly one dependency.</b> The project uses only the JDK, Swing and the SQLite driver.
Everything else — streams, threads, collections, futures — is standard library. A short dependency list is
a real advantage: fewer things to update, fewer vulnerabilities, fewer surprises.</p>

<p><b>The version is a property, not a literal.</b>
<span class="mono">&lt;sqlite-jdbc.version&gt;</span> is declared once in
<span class="mono">&lt;properties&gt;</span> and referenced as
<span class="mono">${sqlite-jdbc.version}</span>. Upgrading the driver means changing one line.</p>

<p><b>The source encoding is declared.</b> UTF-8 is stated explicitly, so the compiler reads the source
files the same way on every machine. This is the build-file equivalent of the explicit charsets in
Chapter 5 — the same discipline applied to a different artefact.</p>
""")

B17.append("""
<h3><span class="n">17.4</span>Plugins and the build lifecycle</h3>
<p>Maven's build is a fixed sequence of <b>phases</b>. Running a later phase runs every earlier one.</p>
""")

B17.append(table(
  ["Phase", "What happens", "Plugins involved"],
  [
    ["<span class='mono'>validate</span>", "The project description is checked", "Core"],
    ["<span class='mono'>compile</span>", "Sources in <span class='mono'>src/main/java</span> are compiled to <span class='mono'>target/classes</span>",
     "<span class='mono'>maven-compiler-plugin</span>"],
    ["<span class='mono'>test</span>", "Tests in <span class='mono'>src/test/java</span> are compiled and run",
     "<span class='mono'>maven-surefire-plugin</span>"],
    ["<span class='mono'>package</span>", "Compiled classes are packaged into a jar in <span class='mono'>target/</span>",
     "<span class='mono'>maven-jar-plugin</span>, then <span class='mono'>maven-shade-plugin</span>"],
    ["<span class='mono'>verify</span>", "Additional checks run", "Any verification plugin"],
    ["<span class='mono'>install</span>", "The artefact is copied into the local repository", "Core"],
    ["<span class='mono'>deploy</span>", "The artefact is uploaded to a remote repository", "Core"],
  ],
  caption="<b>Table 17.2</b> — The Maven lifecycle phases and what each produces."))

B17.append("""
<p>So <span class="mono">mvn package</span> compiles, tests and packages. The commands you will actually
type are short.</p>
""")

B17.append(code('''mvn compile            # compile only
mvn test               # compile and run the test suite
mvn package            # compile, test, and produce target/basinwatch-1.0.0.jar
mvn clean package      # delete target/ first, then do all of the above
mvn dependency:tree    # print the resolved dependency tree''', "the four commands you need in practice", lang="none"))

B17.append("""
<h3><span class="n">17.5</span>Where the JDBC driver comes from</h3>
<p>Chapter 11 asked why the driver is on the classpath and answered "a Maven dependency". Here is the
mechanism.</p>
""")

B17.append(trace("How the SQLite driver reaches the running program", [
  "<b>Declared.</b> <span class='mono'>pom.xml</span> names <span class='mono'>org.xerial:sqlite-jdbc:3.50.3.0</span>.",
  "<b>Resolved.</b> Maven downloads the jar from a repository into the local cache, typically <span class='mono'>~/.m2/repository</span>.",
  "<b>Added to the compile classpath.</b> The compiler can now resolve any driver-specific types referenced in the source.",
  "<b>Added to the runtime classpath.</b> When the program runs, the jar is on the class path, so <span class='mono'>org.sqlite.JDBC</span> is loadable.",
  "<b>Discovered automatically.</b> The jar contains <span class='mono'>META-INF/services/java.sql.Driver</span>, so the JDK registers the driver without any code.",
  "<b>Selected by URL.</b> <span class='mono'>DriverManager.getConnection(\"jdbc:sqlite:…\")</span> asks each registered driver whether it accepts the URL; the SQLite driver says yes.",
]))

B17.append(mistake("""<p>Forgetting that the driver must be on the <i>runtime</i> classpath, not just the
compile classpath. This is the classic cause of
<span class='mono'>SQLException: No suitable driver found</span> in a program that compiles perfectly. The
dependency is present when the compiler runs and absent when the program runs — usually because the jar was
built without it, which is the next section's subject.</p>"""))

B17.append("""
<h3><span class="n">17.6</span>Packaging a runnable jar</h3>
<p>A plain jar contains only your own compiled classes. Run it and the driver is missing. Maven's
<span class="mono">shade</span> plugin solves this by producing an "uber jar": your classes plus the
dependency classes, merged into one file.</p>
""")

B17.append(code('''<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-shade-plugin</artifactId>
    <version>3.6.0</version>
    <executions>
        <execution>
            <phase>package</phase>
            <goals><goal>shade</goal></goals>
            <configuration>
                <createDependencyReducedPom>false</createDependencyReducedPom>
                <transformers>
                    <!-- CRITICAL: merge META-INF/services files from every jar -->
                    <transformer implementation="org.apache.maven.plugins.shade.resource.ServicesResourceTransformer"/>
                    <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                        <mainClass>com.basinwatch.app.BasinWatchApp</mainClass>
                    </transformer>
                </transformers>
            </configuration>
        </execution>
    </executions>
</plugin>''', "from BasinWatch, pom.xml — the shade plugin and the transformer that matters.", lang="none"))

B17.append(core("""<p><b>The <span class='mono'>ServicesResourceTransformer</span> is not optional.</b>
Without it, the shading process would keep only one
<span class='mono'>META-INF/services/java.sql.Driver</span> file and discard the others. The merged jar
would then contain the SQLite driver's classes but no registration, and the application would fail with
"No suitable driver found" — even though the driver is physically inside the jar. This is one of the most
confusing failures in Java packaging, and the transformer is the fix.</p>"""))

B17.append("""
<p>The <span class="mono">ManifestResourceTransformer</span> sets
<span class="mono">Main-Class</span> in the jar's manifest, which is what makes
<span class="mono">java -jar basinwatch-1.0.0.jar</span> start the application instead of printing an
error.</p>
""")

B17.append(visual("""<p>Diagram 25 shows both jars Maven produces. The thin jar in
<span class='mono'>target/</span> contains only the project's own classes and is not runnable alone. The
shaded jar contains the project plus the driver's classes plus the merged service files, and it is the
artefact you distribute.</p>"""))

B17.append("""
<h3><span class="n">17.7</span>Why this matters to the rest of the book</h3>
<p>The build file is not administrative overhead. It is the answer to three questions the other chapters
raise.</p>

<ul>
<li><b>Why does the JDBC code compile?</b> Because <span class="mono">java.sql</span> is in the JDK and the
driver is on the compile classpath.</li>
<li><b>Why does the JDBC code run?</b> Because the driver is on the runtime classpath and registers itself
through a service file.</li>
<li><b>Why does the application start with one command?</b> Because the shade plugin merged everything into
one jar and set <span class="mono">Main-Class</span>.</li>
</ul>

<p>Remove any one of those and the application stops working, even though no Java source changed. That is
the lesson of this chapter: the build is part of the program.</p>
""")

B17.append(exam("""<p>A likely question is "how does your application get its database driver?" The complete
answer has three parts: it is declared as a Maven dependency with groupId, artifactId and version; Maven
resolves it and places it on the classpath; and the driver registers itself through
<span class='mono'>META-INF/services</span>, which the shade plugin must be configured to merge. That last
clause is what distinguishes an answer that has read the pom from one that has not.</p>"""))

B17.append(summary([
  "A build tool resolves dependencies, compiles, tests and packages; Maven is the one this project uses.",
  "Every library is identified by groupId, artifactId and version, and Maven resolves their transitive dependencies automatically.",
  "The pom.xml declares coordinates, properties, dependencies and build plugins.",
  "BasinWatch has exactly one dependency — the SQLite JDBC driver — because everything else is in the JDK.",
  "Maven's lifecycle is a fixed sequence of phases, and a later phase runs every earlier one.",
  "The JDBC driver reaches the runtime classpath as a Maven dependency and registers itself through a service file.",
  "The shade plugin builds an uber jar containing the dependency classes, and its ServicesResourceTransformer is required for driver registration to survive.",
  "The build configuration is part of the program: change it and the application's behaviour changes without any Java source changing.",
]))

B17.append(keyterms([
  "<b>pom.xml</b> — the Project Object Model, Maven's description of a project.",
  "<b>Coordinate</b> — the groupId, artifactId and version triple identifying a library.",
  "<b>Transitive dependency</b> — a library required by a library you depend on directly.",
  "<b>Build lifecycle</b> — Maven's ordered sequence of phases.",
  "<b>Uber jar</b> — a jar containing a project's classes plus all its dependencies' classes.",
  "<b>ServicesResourceTransformer</b> — the shade transformer that merges service provider files so driver registration survives packaging.",
]))

B17.append("</div>")

# ======================================================================
# CHAPTER 18
# ======================================================================
B18.append(chapter(18, "XML, Schemas, Namespaces, Annotations and JavaBeans",
"Structured text, the rules that constrain it, and the two ways Java records metadata about code — with a clear statement of what this project does and does not use."))

B18.append("""
<h3><span class="n">18.1</span>XML: a tree of labelled text</h3>
<p>XML is a way of writing structured data as text. Everything in it is either an <b>element</b> with a
name, or <b>text</b> inside an element. Elements nest, forming a tree.</p>
""")

B18.append(code('''<?xml version="1.0" encoding="UTF-8"?>
<basin name="Northreach" revision="3">
    <zone id="UPR" waterLevelMeters="3.62">
        <name>Upper Reach</name>
        <residents>18</residents>
    </zone>
    <zone id="MIL" waterLevelMeters="2.71">
        <name>Middle Basin</name>
        <residents>42</residents>
    </zone>
</basin>''', "illustrative — the same zone data the project holds in Java, expressed as XML", lang="none"))

B18.append(table(
  ["Term", "Meaning", "In the example"],
  [
    ["Element", "A labelled node with a start tag and an end tag", "<span class='mono'>&lt;zone&gt;…&lt;/zone&gt;</span>"],
    ["Attribute", "A name-value pair inside a start tag", "<span class='mono'>id=\"UPR\"</span>"],
    ["Text content", "Characters between tags", "<span class='mono'>Upper Reach</span>"],
    ["Root element", "The single outermost element", "<span class='mono'>&lt;basin&gt;</span>"],
    ["Well-formed", "Every tag closed, correctly nested, one root, quoted attributes", "The example is well-formed"],
    ["Valid", "Well-formed <i>and</i> conforming to a schema", "A separate question — see below"],
  ],
  caption="<b>Table 18.1</b> — XML terminology."))

B18.append(distinct("""<p><b>Well-formed and valid are different things.</b> A document is
<i>well-formed</i> if it follows XML's syntax rules: tags match, nesting is correct, there is exactly one
root. It is <i>valid</i> if it also conforms to a schema that says which elements may appear, in what
order, with what types. Every valid document is well-formed; a well-formed document need not be
valid.</p>"""))

B18.append("""
<h3><span class="n">18.2</span>Namespaces</h3>
<p>A namespace is a prefix that qualifies element and attribute names, so that two vocabularies can be
mixed in one document without collision.</p>
""")

B18.append(figure("d23_xml_namespaces_schema", "26", "Namespaces, schemas and validation",
"A document declaring two namespaces, each bound to a URI that identifies a vocabulary. A schema in the xsd namespace describes the elements and types allowed in the document namespace. Validation checks the document against that description.",
"landscape"))

B18.append(code('''<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
</project>''', "from BasinWatch, pom.xml — the namespace declarations at the top of the file you already met.", lang="none"))

B18.append("""
<p>That header is worth decoding, because it is the same pattern everywhere.</p>

<p><span class="mono">xmlns=\"http://maven.apache.org/POM/4.0.0\"</span> declares the <b>default
namespace</b>. Every unprefixed element — <span class="mono">project</span>,
<span class="mono">modelVersion</span>, <span class="mono">dependencies</span> — belongs to it.</p>

<p><span class="mono">xmlns:xsi=\"…XMLSchema-instance\"</span> binds the prefix
<span class="mono">xsi</span> to the XML Schema instance namespace, which defines two attributes used for
validation: <span class="mono">schemaLocation</span> and
<span class="mono">noNamespaceSchemaLocation</span>.</p>

<p><span class="mono">xsi:schemaLocation</span> pairs a namespace URI with the URL of the schema that
describes it. A validating parser can therefore find the schema and check the document.</p>
""")

B18.append(core("""<p><b>A namespace URI is an identifier, not an address.</b>
<span class='mono'>http://maven.apache.org/POM/4.0.0</span> does not have to be fetchable. Its purpose is
to be a globally unique string that everyone agrees means the same vocabulary. That is why the same URI
appears unchanged in every Maven project, and why it is a common examination point.</p>"""))

B18.append("""
<h3><span class="n">18.3</span>XML Schema</h3>
<p>A schema is itself an XML document that describes which elements and attributes another XML document
may contain. Two schema languages exist: DTD and XSD. XSD is the modern one and the one the syllabus
material covers.</p>
""")

B18.append(code('''<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:element name="basin">
        <xs:complexType>
            <xs:sequence>
                <xs:element name="zone" maxOccurs="unbounded">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="name" type="xs:string"/>
                            <xs:element name="residents" type="xs:nonNegativeInteger"/>
                        </xs:sequence>
                        <xs:attribute name="id" type="xs:string" use="required"/>
                        <xs:attribute name="waterLevelMeters" type="xs:decimal" use="required"/>
                    </xs:complexType>
                </xs:element>
            </xs:sequence>
            <xs:attribute name="name" type="xs:string"/>
        </xs:complexType>
    </xs:element>
</xs:schema>''', "illustrative — a schema describing the basin document", lang="none"))

B18.append("""
<p>A schema buys you four things, and each corresponds to something you would otherwise have to check in
code.</p>
""")

B18.append(table(
  ["Schema feature", "What it constrains", "Java equivalent"],
  [
    ["Element and attribute declarations", "Which names may appear", "The fields of a class"],
    ["<span class='mono'>type</span>", "What values are allowed", "The declared type of a field"],
    ["<span class='mono'>use=\"required\"</span>", "Whether something must be present", "A constructor that rejects null"],
    ["<span class='mono'>maxOccurs=\"unbounded\"</span>", "How many times something may repeat", "A <span class='mono'>List</span> field"],
    ["<span class='mono'>xs:sequence</span>", "The required order of children", "The parameter order of a constructor"],
    ["<span class='mono'>xs:nonNegativeInteger</span>", "A value range", "A range check in a compact constructor"],
  ],
  caption="<b>Table 18.2</b> — What a schema expresses, and the Java construct that expresses the same idea."))

B18.append(connect("""<p>That comparison is the useful way to think about schemas. A schema is validation
declared outside the program, in a language a validator can read. BasinWatch does the same work in Java:
<span class='mono'>SensorReading</span>'s compact constructor rejects out-of-range values,
<span class='mono'>SessionSnapshot.validate</span> re-checks restored state, and the database's
<span class='mono'>NOT NULL</span> constraints reject missing columns. Three mechanisms, one
purpose.</p>"""))

B18.append(related("""<p><b>BasinWatch does not read or write any XML of its own.</b> Its only XML file is
<span class='mono'>pom.xml</span>, which Maven reads. The project has no configuration XML, no schema, and
no XML parser on its classpath. The XML material in this chapter is syllabus content and ecosystem
knowledge — it is what you need to understand the build file and to recognise the technique when you meet
it in a framework. It is not part of the application's runtime design, and saying so is more honest than
inventing a use for it.</p>"""))

B18.append("""
<h3><span class="n">18.4</span>Annotations</h3>
<p>An annotation is metadata attached to a declaration. It does not change what the code does by itself; it
records information that a compiler or a framework can read.</p>
""")

B18.append(code('''@Override                                   // read by the compiler
public String toString() { return name; }

@Deprecated                                 // read by the compiler and by tools
public void oldDispatch() { }

@FunctionalInterface                        // read by the compiler
public interface BasinEvent { /* ... */ }

@SuppressWarnings("unchecked")              // read by the compiler
void copy(List<?> source) { }

// An annotation with members — this is the shape frameworks use
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface Component {
    String value() default "";
}''', "illustrative — standard annotations and one framework-style annotation"))

B18.append(table(
  ["Retention", "Available at", "Used for"],
  [
    ["<span class='mono'>SOURCE</span>", "Compile time only; not in the class file", "<span class='mono'>@Override</span>, <span class='mono'>@SuppressWarnings</span>"],
    ["<span class='mono'>CLASS</span>", "In the class file, but not readable at runtime by default", "Some build-tool and analysis annotations"],
    ["<span class='mono'>RUNTIME</span>", "In the class file and readable by reflection at runtime", "Framework annotations such as <span class='mono'>@Component</span>, <span class='mono'>@Autowired</span>"],
  ],
  caption="<b>Table 18.3</b> — The three retention policies, and why the third is the one frameworks need."))

B18.append(core("""<p>That table explains why annotations matter to frameworks. If an annotation's
retention is <span class='mono'>RUNTIME</span>, a framework can discover it by reflection and act on it —
that is the entire mechanism behind Spring's component scanning, JPA's entity mapping and JUnit's test
discovery. Without runtime retention, an annotation is only a message to the compiler.</p>"""))

B18.append(practice("""<p>BasinWatch uses standard annotations only, and each one is doing exactly what
its retention promises:</p>
<pre><span class="an">@Override</span> <span class="kw">public</span> <span class="ty">String</span> toString() { ... }        <span class="cm">// SOURCE — compiler checks the signature</span>
<span class="an">@FunctionalInterface</span> <span class="kw">public interface</span> <span class="ty">BasinEvent</span> { ... }  <span class="cm">// SOURCE — compiler enforces one method</span>
<span class="an">@SuppressWarnings</span>(<span class="st">"unchecked"</span>) ...                              <span class="cm">// SOURCE — silences one warning</span></pre>
<div class="codecap"><b>Listing 18.1</b> — from BasinWatch — standard annotations, no framework annotations.</div>
<p>There is no <span class="mono">@Component</span>, no <span class="mono">@Autowired</span> and no
<span class="mono">@Entity</span> anywhere in the project, because there is no framework to read
them.</p>"""))

B18.append("""
<h3><span class="n">18.5</span>POJO, JavaBean and the wiring they enable</h3>
<p>Chapter 2 introduced the distinction. Here is why it exists, which is the part that matters when you
meet a framework.</p>
""")

B18.append(figure("d26_annotation_bean_wiring", "27", "Hand-written wiring versus framework wiring",
"Left: BasinWatch constructs its services explicitly, passing each dependency through a constructor. Right: a framework scans annotated classes, instantiates JavaBeans reflectively, and injects dependencies by matching types. Both produce the same object graph.",
"landscape"))

B18.append(table(
  ["Aspect", "BasinWatch (hand-written wiring)", "A framework such as Spring"],
  [
    ["How objects are created", "Explicit <span class='mono'>new</span> calls in constructors", "Reflection, driven by annotations or XML"],
    ["How dependencies arrive", "Constructor arguments", "Injected fields, setters or constructors"],
    ["What the classes must look like", "Anything; records and final classes are fine", "Usually a JavaBean: no-argument constructor and setters, or an annotated constructor"],
    ["Where the wiring lives", "In the source, readable with the class", "In annotations plus the framework's scan configuration"],
    ["Compile-time safety", "A missing dependency is a compile error", "A missing bean is a runtime error"],
    ["Discoverability", "Follow the constructor", "Search for the annotation"],
  ],
  caption="<b>Table 18.4</b> — Two ways to assemble an object graph."))

B18.append(related("""<p><b>BasinWatch wires by hand.</b> <span class='mono'>BasinEngine</span> constructs
the <span class='mono'>DatabaseService</span>, which constructs the
<span class='mono'>DatabaseManager</span> and passes it to each repository's constructor. That is
constructor injection, performed manually and visibly. It is a legitimate choice for an application of this
size: there are six packages and roughly two dozen classes, so a framework would add a dependency, a
start-up scan and a class of runtime errors in exchange for saving perhaps thirty lines. A larger
application with hundreds of components would make the opposite trade, which is the subject of
Chapter 19.</p>"""))

B18.append(exam("""<p>If asked "what is the difference between a POJO and a JavaBean?", give the
convention first — no-argument constructor, private fields, public accessors, often Serializable — and then
the reason: a framework needs to instantiate and populate the object without knowing anything about it.
Adding the reason is what turns a definition into an explanation. Then note that every JavaBean is a POJO
but not the reverse, and that a record can never be a JavaBean.</p>"""))

B18.append(summary([
  "XML represents structured data as a tree of elements, attributes and text.",
  "A document is well-formed if it follows XML syntax; it is valid if it also conforms to a schema.",
  "A namespace URI is a unique identifier for a vocabulary, not necessarily a fetchable address.",
  "An XSD schema declares which elements and attributes may appear, in what order and with what types.",
  "An annotation is metadata; its retention policy determines whether it is available at runtime.",
  "Runtime retention is what allows frameworks to discover annotations by reflection.",
  "BasinWatch uses standard annotations only, and contains no XML of its own beyond pom.xml.",
  "A JavaBean's conventions exist so a framework can instantiate and populate it reflectively; BasinWatch instead wires its objects by hand.",
]))

B18.append(keyterms([
  "<b>Well-formed</b> — following XML's syntax rules.",
  "<b>Valid</b> — well-formed and conforming to a schema.",
  "<b>Namespace</b> — a URI-qualified vocabulary that prevents name collisions in a document.",
  "<b>XSD</b> — XML Schema Definition, a schema language written in XML itself.",
  "<b>Annotation retention</b> — how long an annotation survives: source, class or runtime.",
  "<b>Reflection</b> — inspecting and using classes and members at runtime, which is how frameworks read annotations.",
]))

B18.append("</div>")

# ======================================================================
# CHAPTER 19
# ======================================================================
B19.append(chapter(19, "Raw JDBC versus Spring JdbcTemplate",
"The repetitive pattern that raw JDBC forces you to write, the abstraction that removes it, and an honest comparison with what this project actually does."))

B19.append("""
<h3><span class="n">19.1</span>The repetition in raw JDBC</h3>
<p>Look back at any repository method in Chapter 12 and count the lines that are about the query rather
than about the resource handling.</p>
""")

B19.append(code('''public List<DatabaseHistoryEntry> loadRecent(int limit) throws SQLException {
    String sql = "SELECT ... FROM operational_events ORDER BY occurred_at DESC LIMIT ?";
    ArrayList<DatabaseHistoryEntry> entries = new ArrayList<>();
    try (Connection connection = database.openConnection()) {                 // boilerplate
        try (PreparedStatement statement = connection.prepareStatement(sql)) { // boilerplate
            statement.setInt(1, limit);                                       // the actual work
            try (ResultSet rows = statement.executeQuery()) {                 // boilerplate
                while (rows.next()) {                                         // boilerplate
                    entries.add(new DatabaseHistoryEntry(                     // the actual work
                            DatabaseHistoryType.valueOf(rows.getString("event_type")),
                            rows.getString("zone_id"),
                            rows.getString("detail"),
                            Instant.parse(rows.getString("occurred_at"))));
                }
            }
        }
    }
    return List.copyOf(entries);
}''', "from BasinWatch, db/OperationalEventRepository.java — three lines of intent inside ten lines of resource handling."))

B19.append("""
<p>The structure is identical in every method: open a connection, prepare a statement, bind parameters,
execute, iterate, close everything. Only the SQL and the row mapping change. That is the definition of code
that wants to be abstracted.</p>
""")

B19.append(core("""<p><b>Repetition like this is not merely ugly — it is a source of bugs.</b> Every
place that must remember to close a connection is a place that might forget. Every place that must bind
parameters in the right order is a place that might get the order wrong. Raw JDBC in BasinWatch is safe
because it is written carefully in a handful of repository classes; in a larger codebase, the same pattern
repeated two hundred times would not stay safe.</p>"""))

B19.append("""
<h3><span class="n">19.2</span>What Spring JdbcTemplate does</h3>
<p>Spring's <span class="mono">JdbcTemplate</span> is a thin wrapper over the JDBC interfaces you already
know. It performs exactly the steps in that method, and asks you to supply only the two things that vary:
the SQL, and the code that turns a row into an object.</p>
""")

B19.append(code('''// ---- the same query, with JdbcTemplate ----
String sql = "SELECT occurred_at, event_type, zone_id, detail "
           + "FROM operational_events ORDER BY occurred_at DESC LIMIT ?";

List<DatabaseHistoryEntry> entries = jdbcTemplate.query(sql,
        (rows, rowNumber) -> new DatabaseHistoryEntry(
                DatabaseHistoryType.valueOf(rows.getString("event_type")),
                rows.getString("zone_id"),
                rows.getString("detail"),
                Instant.parse(rows.getString("occurred_at"))),
        limit);''', "lecture-note style — the same query expressed with Spring JdbcTemplate"))

B19.append("""
<p>Compare the two listings. The intent is identical and the SQL is identical. What has disappeared is
every line about connections, statements, result sets and closing — because
<span class="mono">JdbcTemplate</span> does all of it. The lambda in the middle is the <b>RowMapper</b>:
given a row, produce an object.</p>
""")

B19.append(table(
  ["Raw JDBC step", "Who does it with JdbcTemplate", "What you still supply"],
  [
    ["Obtain a connection", "<span class='mono'>JdbcTemplate</span>, from its <span class='mono'>DataSource</span>", "Nothing"],
    ["Prepare the statement", "<span class='mono'>JdbcTemplate</span>", "The SQL text with <span class='mono'>?</span> placeholders"],
    ["Bind parameters", "<span class='mono'>JdbcTemplate</span>, from the argument list", "The values, in order"],
    ["Execute", "<span class='mono'>JdbcTemplate</span>", "Nothing"],
    ["Iterate the result set", "<span class='mono'>JdbcTemplate</span>", "The <span class='mono'>RowMapper</span> lambda"],
    ["Close the result set, statement and connection", "<span class='mono'>JdbcTemplate</span>", "Nothing"],
    ["Translate <span class='mono'>SQLException</span>", "<span class='mono'>JdbcTemplate</span>, into a <span class='mono'>DataAccessException</span> hierarchy", "Nothing"],
  ],
  caption="<b>Table 19.1</b> — What JdbcTemplate takes over, and what remains your responsibility."))

B19.append("""
<h3><span class="n">19.3</span>The DataSource, and DriverManagerDataSource</h3>
<p><span class="mono">JdbcTemplate</span> does not call <span class="mono">DriverManager</span> itself. It
asks a <span class="mono">DataSource</span> for connections.</p>
""")

B19.append(defbox("DataSource",
"an interface representing a source of database connections. Code asks it for a connection; how that connection is created — a direct call, a pool, a JNDI lookup — is the DataSource's business."))

B19.append(code('''// ---- a DataSource configured by hand, as the lecture notes show ----
@Bean
public DataSource dataSource() {
    DriverManagerDataSource dataSource = new DriverManagerDataSource();
    dataSource.setDriverClassName("org.sqlite.JDBC");
    dataSource.setUrl("jdbc:sqlite:data/basinwatch.db");
    return dataSource;
}

@Bean
public JdbcTemplate jdbcTemplate(DataSource dataSource) {
    return new JdbcTemplate(dataSource);
}''', "lecture-note style — DriverManagerDataSource and JdbcTemplate declared as beans"))

B19.append("""
<p><span class="mono">DriverManagerDataSource</span> is a simple <span class="mono">DataSource</span>
implementation that creates a brand-new connection on every call and never pools them. It is useful for
teaching and for tests, and it is not what you would use in a production application — there you would use
a pooling implementation such as HikariCP, because opening a physical connection per query is
expensive.</p>
""")

B19.append(clarify("""<p>The lecture material configures these as Spring beans, using either
<span class='mono'>@Bean</span> methods in a configuration class or XML
<span class='mono'>&lt;bean&gt;</span> elements. Both are the same idea expressed two ways: a container
creates and holds the objects, and injects them where needed. The
<span class='mono'>DriverManagerDataSource</span> class itself lives in
<span class='mono'>org.springframework.jdbc.datasource</span> and is a teaching-friendly convenience rather
than a production choice — its own documentation says so.</p>"""))

B19.append(related("""<p><b>BasinWatch does not use JdbcTemplate, Spring, or a DataSource.</b> It calls
<span class='mono'>DriverManager.getConnection</span> directly inside
<span class='mono'>DatabaseManager</span> and passes a <span class='mono'>Connection</span> to each
repository. That is raw JDBC. Nothing in this chapter should be read as a description of the project's
implementation — it is the alternative approach the syllabus teaches, presented so you can compare it with
what the project does.</p>"""))

B19.append("""
<h3><span class="n">19.4</span>Side by side</h3>
""")

B19.append(figure("d25_raw_vs_spring", "28", "Raw JDBC and Spring JdbcTemplate",
"Left: the project's raw path, where the application opens a connection through DriverManager and manages every resource itself. Right: the JdbcTemplate path, where a DataSource supplies connections and the template manages resources, leaving only SQL and row mapping to the application.",
"landscape"))

B19.append(table(
  ["Question", "Raw JDBC (BasinWatch)", "Spring JdbcTemplate"],
  [
    ["Who opens the connection?", "<span class='mono'>DatabaseManager.openConnection()</span>", "The <span class='mono'>DataSource</span> behind the template"],
    ["Who closes it?", "try-with-resources in each repository method", "<span class='mono'>JdbcTemplate</span>"],
    ["Who binds parameters?", "Typed setters, written by hand", "<span class='mono'>JdbcTemplate</span>, from the argument list"],
    ["Who maps rows?", "A loop inside the method", "The <span class='mono'>RowMapper</span> you supply"],
    ["Exception type", "<span class='mono'>SQLException</span>", "<span class='mono'>DataAccessException</span>"],
    ["Transactions", "<span class='mono'>setAutoCommit(false)</span> and <span class='mono'>commit()</span> written by hand", "<span class='mono'>@Transactional</span> or a <span class='mono'>TransactionTemplate</span>"],
    ["Extra dependencies", "The driver only", "Spring Core, Spring JDBC, plus the driver"],
    ["Lines per query", "Roughly fifteen", "Roughly five"],
    ["Compile-time checking of the SQL", "None", "None"],
    ["Used in BasinWatch?", "<b>Yes</b>", "<b>No</b>"],
  ],
  caption="<b>Table 19.2</b> — The two approaches compared, with the project's actual choice stated."))

B19.append(core("""<p>Two conclusions follow from that table, and both are worth holding together.</p>
<p><b>JdbcTemplate is not a replacement for JDBC.</b> It is a class that calls the same
<span class='mono'>Connection</span>, <span class='mono'>PreparedStatement</span> and
<span class='mono'>ResultSet</span> interfaces you studied in Chapter 12. Everything you learned about
parameter binding, result-set iteration and transactions still applies — you have simply delegated the
resource handling.</p>
<p><b>Neither approach is wrong.</b> For an application with one database and a dozen queries, raw JDBC in
a few repository classes is perfectly reasonable and keeps the dependency list to one jar. For an
application with hundreds of queries, pooling, declarative transactions and several data sources, the
framework earns its place.</p>"""))

B19.append(exam("""<p>A very likely question is "why does Spring JdbcTemplate not eliminate the need for
JDBC?" The answer is that it is built <i>on</i> JDBC: it obtains connections from a
<span class='mono'>DataSource</span>, creates <span class='mono'>PreparedStatement</span>s, binds
parameters, iterates <span class='mono'>ResultSet</span>s and closes everything — all through the same
<span class='mono'>java.sql</span> interfaces. It removes repetition, not the underlying protocol. Saying
that plainly is usually worth full marks.</p>"""))

B19.append(summary([
  "Raw JDBC forces the same resource-handling structure into every method, with only the SQL and row mapping varying.",
  "JdbcTemplate performs that structure for you and asks only for the SQL and a RowMapper.",
  "A DataSource supplies connections; JdbcTemplate never calls DriverManager directly.",
  "DriverManagerDataSource creates a new connection per call and does not pool; it is for teaching and tests.",
  "JdbcTemplate translates SQLException into Spring's DataAccessException hierarchy.",
  "JdbcTemplate is built on the same java.sql interfaces, so it removes repetition rather than JDBC itself.",
  "BasinWatch uses raw JDBC exclusively; the JdbcTemplate material is a taught alternative, not a description of the project.",
]))

B19.append(keyterms([
  "<b>JdbcTemplate</b> — a Spring class that executes SQL and manages JDBC resources, leaving SQL and row mapping to the caller.",
  "<b>RowMapper</b> — a callback that converts one result-set row into an object.",
  "<b>DataSource</b> — an abstraction representing a source of database connections.",
  "<b>DriverManagerDataSource</b> — a simple non-pooling DataSource implementation.",
  "<b>DataAccessException</b> — Spring's unchecked exception hierarchy for data access failures.",
]))

B19.append("</div>")

HTML = "".join(P + B17 + B18 + B19)
