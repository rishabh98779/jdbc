# AGENTS.md — Java Concepts Integrated Visual Notes

## What this project is
One unified Java teaching book (`Java_Concepts_Integrated_Visual_Notes`) covering
Java I/O, streams, serialization, threads, JDBC/SQLite, Swing, Maven, XML/XSD,
annotations and Spring JdbcTemplate, taught as one connected system around the
**BasinWatch** case study (github.com/Rishu07368/basinwatch).

## Build
```bash
python3 build.py          # HTML + PDF + DOCX  (full build)
python3 build.py html     # fast iteration
python3 build.py pdf
python3 build.py docx
python3 qa_pages.py       # layout QA: blank pages, overflow, full-bleed detection
python3 qa_diagrams.py    # diagram QA: clipped/overflowing text runs
```
Outputs land in `out/`.

## Layout
- `content/` — one module per part: `front`, `part1`…`part6`, `revision`.
  Each exports `HTML`. Shared helpers come from `content/__init__.py`
  (`defbox`, `core`, `figure`, `table`, `mistake`, `exam`, `chapter`, `qa`, `exercise`).
- `book.css` — print stylesheet (dark navy cover, teal accent).
- `diagramkit.py` — the diagram Canvas API (boxes, arrows, tables, notes).
- `diagrams_a.py` / `diagrams_b.py` / `diagrams_c.py` — 29 diagrams, each a
  `dNN_*()` function listed in the module's `ALL`. Run `ALL` to regenerate PNG/SVG
  into `assets/png` and `assets/svg`.

## Conventions that matter
- **Diagram numbering is sequential by book order.** If you add, remove or move a
  `figure()` call, renumber *both* the `figure(name, "N", …)` argument and the baked-in
  `"Diagram N — …"` title inside the matching generator function, or the printed
  number and the caption will disagree.
- Source-labelling discipline: every claim is marked `FROM THE LECTURE NOTES`,
  `CONCEPT EXPLAINED FURTHER`, `BASINWATCH IN PRACTICE`,
  `RELATED TECHNIQUE — NOT USED IN BASINWATCH`, `IMPORTANT DISTINCTION`,
  `COMMON MISTAKE`, `EXAM TIP`, `TECHNICAL CLARIFICATION`.
  Never present supplementary material as lecture content, and never claim the
  project uses Spring — it uses raw JDBC.
- TOC page numbers use CSS `target-counter(attr(href), page)`; the counter must sit
  on an `<a>` that carries the `href` (`.pg a::after`), not on the bare span.
- The DOCX converter encodes bold/italic/code as control chars `\x01`–`\x05`.
  Always run text through `_plain()` before passing it to a python-docx API that
  writes raw strings (headings, list items, table cells), or Word rejects the file.
