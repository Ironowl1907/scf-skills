#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Dossier standard: the YAML template is the single source of truth.

Commands
  render    Turn the YAML template into a fill-in Markdown dossier.
  validate  Check a filled dossier against the YAML template.

Examples
  uv run dossier.py render -o assets/brief-and-context.md
  uv run dossier.py render --check assets/brief-and-context.md   # drift check
  uv run dossier.py validate .ai/tasks/my-task/01-brief-and-context.md
  uv run dossier.py validate DOSSIER --json

Exit codes: 0 = ok, 1 = dossier invalid / render out of date, 2 = template or usage error.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

import yaml

DEFAULT_TEMPLATE = Path(__file__).resolve().with_name("brief-and-context.yaml")
FORMATS = {"string": "prose", "ordered_list": "ordered list",
           "bullet_list": "bullet list"}
META_TYPES = {"string", "enum"}

PLACEHOLDER_RE = re.compile(r"<([^<>\n]+)>")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
LIST_RE = re.compile(
    r"^(?P<indent>\s*)(?P<marker>[-*+]|\d+[.)])\s+(?P<text>.*)$")
NONE_RE = re.compile(r"^[_*]*(none|n/a)[_*.]*$", re.I)


# --------------------------------------------------------------------------- template model


class TemplateError(Exception):
    pass


@dataclass
class MetaField:
    name: str
    type: str
    options: list[str] = field(default_factory=list)
    default: str | None = None
    required: bool = True


@dataclass
class Block:
    """A unit of content: a section with `format`, or a subsection."""

    title: str
    format: str
    prompt: str | None = None
    item_schema: str | None = None
    required: bool = True
    pattern: re.Pattern | None = None
    example: str = ""
    placeholders: set[str] = field(default_factory=set)


@dataclass
class Section:
    id: str
    title: str
    block: Block | None
    subsections: list[Block]
    required_at: str | None = None


@dataclass
class Template:
    path: Path
    version: str
    metadata: list[MetaField]
    sections: list[Section]

    @property
    def status_field(self) -> MetaField | None:
        return next((f for f in self.metadata if f.name == "status" and f.type == "enum"), None)


def load_template(path: Path) -> Template:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise TemplateError(f"template not found: {path}") from None
    except yaml.YAMLError as e:
        raise TemplateError(f"invalid YAML in {path}: {e}") from None
    if not isinstance(raw, dict):
        raise TemplateError("template root must be a mapping")

    meta_raw = raw.get("metadata") or {}
    if not isinstance(meta_raw, dict):
        raise TemplateError("'metadata' must be a mapping")
    metadata = [_parse_meta(k, v) for k, v in meta_raw.items()]
    statuses = next((f.options for f in metadata if f.name ==
                    "status" and f.type == "enum"), [])

    sections_raw = raw.get("sections")
    if not isinstance(sections_raw, list) or not sections_raw:
        raise TemplateError("'sections' must be a non-empty list")

    sections, seen = [], set()
    for i, s in enumerate(sections_raw):
        where = f"sections[{i}]"
        if not isinstance(s, dict) or not s.get("title"):
            raise TemplateError(f"{where}: each section needs a 'title'")
        title = str(s["title"])
        subs_raw = s.get("subsections")
        if bool(subs_raw) == ("format" in s):
            raise TemplateError(
                f"{where} ({title}): define exactly one of 'format' or 'subsections'")
        if _norm(title) in seen:
            raise TemplateError(f"{where}: duplicate section title {title!r}")
        seen.add(_norm(title))

        required_at = s.get("required_at")
        if required_at is not None and required_at not in statuses:
            raise TemplateError(f"{where} ({title}): required_at {
                                required_at!r} is not a status option {statuses}")

        block = _parse_block(s, where) if "format" in s else None
        subs = [_parse_block(b, f"{where}.subsections[{j}]")
                for j, b in enumerate(subs_raw or [])]
        sub_titles = [_norm(b.title) for b in subs]
        if len(sub_titles) != len(set(sub_titles)):
            raise TemplateError(
                f"{where} ({title}): duplicate subsection titles")
        sections.append(Section(str(s.get("id") or _norm(title)),
                        title, block, subs, required_at))

    return Template(path, str(raw.get("version", "?")), metadata, sections)


def _parse_meta(name: str, spec) -> MetaField:
    if isinstance(spec, str):
        spec = {"type": spec}
    if not isinstance(spec, dict):
        raise TemplateError(
            f"metadata.{name}: expected a type name or a mapping")
    ftype = spec.get("type", "string")
    if ftype not in META_TYPES:
        raise TemplateError(f"metadata.{name}: unknown type {
                            ftype!r}; expected one of {sorted(META_TYPES)}")
    options = [str(o) for o in spec.get("options") or []]
    if ftype == "enum" and not options:
        raise TemplateError(f"metadata.{name}: enum needs 'options'")
    default = spec.get("default")
    if default is not None and ftype == "enum" and str(default) not in options:
        raise TemplateError(f"metadata.{name}: default {
                            default!r} is not in options")
    return MetaField(name, ftype, options, None if default is None else str(default), bool(spec.get("required", True)))


def _parse_block(spec, where: str) -> Block:
    if not isinstance(spec, dict) or not spec.get("title"):
        raise TemplateError(f"{where}: needs a 'title'")
    title, fmt = str(spec["title"]), spec.get("format")
    if fmt not in FORMATS:
        raise TemplateError(f"{where} ({title}): unknown format {
                            fmt!r}; expected one of {sorted(FORMATS)}")
    schema = spec.get("item_schema")
    if schema and fmt == "string":
        raise TemplateError(
            f"{where} ({title}): 'item_schema' only applies to list formats")

    prompt = spec.get("prompt")
    example = schema or f"<{(prompt or title).strip().rstrip('.').lower()}>"
    return Block(
        title=title,
        format=fmt,
        prompt=prompt,
        item_schema=schema,
        required=bool(spec.get("required", True)),
        pattern=_compile_schema(schema) if schema else None,
        example=example,
        placeholders={m.strip().casefold()
                      for m in PLACEHOLDER_RE.findall(example)},
    )


def _compile_schema(schema: str) -> re.Pattern:
    """`<x>` becomes a wildcard (`<n>` a number); dashes and whitespace are matched leniently."""
    parts, pos = [], 0
    for m in PLACEHOLDER_RE.finditer(schema):
        parts.append(_literal(schema[pos: m.start()]))
        parts.append(r"\d+" if m.group(1).strip() == "n" else r".+?")
        pos = m.end()
    parts.append(_literal(schema[pos:]))
    return re.compile("^" + "".join(parts) + "$", re.S)


def _literal(text: str) -> str:
    out = []
    for tok in re.split(r"(\s*[—–]\s*|\s+)", text):
        if not tok:
            continue
        if re.fullmatch(r"\s*[—–]\s*", tok):
            out.append(r"\s*(?:—|–|--?)\s*")
        elif tok.isspace():
            out.append(r"\s+")
        else:
            out.append(re.escape(tok))
    return "".join(out)


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().casefold()


# --------------------------------------------------------------------------- render


def render_markdown(t: Template) -> str:
    out = ["---"]
    for f in t.metadata:
        if f.type == "enum":
            out.append(f"{f.name}: {_scalar(f.default or f.options[0])}  # one of: {
                       ' | '.join(f.options)}")
        else:
            out.append(f"{f.name}: {_scalar(f'<{f.name}>')}")
    out += ["---", ""]
    out.append(
        f"<!-- Generated from {
            t.path.name} (v{t.version}); edit the YAML, not this file.\n"
        "Rules: keep every heading verbatim and in order. Replace every <placeholder>.\n"
        "Prose blocks are paragraphs; ordered lists use '1.'; bullet lists use '-'.\n"
        "Optional lists with nothing to record: a single '- None'. Comments are ignored by the validator. -->"
    )
    status = t.status_field
    for s in t.sections:
        out += ["", f"## {s.title}"]
        if s.required_at and status:
            out.append(
                f"<!-- Must be complete once status is '{s.required_at}' or later. -->")
        if s.block:
            out += _render_block(s.block)
        for b in s.subsections:
            out += ["", f"### {b.title}"] + _render_block(b)
    return "\n".join(out) + "\n"


def _render_block(b: Block) -> list[str]:
    hints = [FORMATS[b.format], "required" if b.required else "optional"]
    if b.item_schema:
        hints.append(f"each item: {b.item_schema}")
    if b.prompt and not b.item_schema:
        hints.append(b.prompt if b.format ==
                     "string" else f"one item per: {b.prompt}")
    lines = [f"<!-- {' · '.join(hints)} -->"]
    prefix = {"string": "", "ordered_list": "1. ",
              "bullet_list": "- "}[b.format]
    lines.append(prefix + b.example)
    return lines


def _scalar(value: str) -> str:
    return yaml.safe_dump(value, default_flow_style=True, width=10**6).removesuffix("\n...\n").strip()


# --------------------------------------------------------------------------- markdown parsing


@dataclass
class Heading:
    title: str
    line: int
    body: list[tuple[int, str]] = field(default_factory=list)
    children: list["Heading"] = field(default_factory=list)


@dataclass
class Item:
    line: int
    kind: str  # "ordered" | "bullet"
    text: str


@dataclass
class Content:
    paragraphs: list[tuple[int, str]]
    items: list[Item]


def split_frontmatter(text: str) -> tuple[str | None, list[str], int]:
    """Return (frontmatter, body_lines, 0-based index of the first body line)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, lines, 0
    for i in range(1, len(lines)):
        if lines[i].strip() in ("---", "..."):
            return "\n".join(lines[1:i]), lines[i + 1:], i + 1
    return None, lines, 0


def parse_headings(lines: list[str], offset: int) -> list[Heading]:
    """H2 headings with nested H3 children; everything else becomes body lines."""
    text = COMMENT_RE.sub(
        lambda m: "\n" * m.group().count("\n"), "\n".join(lines))
    sections: list[Heading] = []
    h2 = h3 = None
    in_fence = False
    for idx, line in enumerate(text.split("\n")):
        n = offset + idx + 1
        if FENCE_RE.match(line):
            in_fence = not in_fence
        m = None if in_fence else HEADING_RE.match(line)
        if m and len(m.group(1)) == 2:
            h2, h3 = Heading(m.group(2), n), None
            sections.append(h2)
        elif m and len(m.group(1)) == 3 and h2:
            h3 = Heading(m.group(2), n)
            h2.children.append(h3)
        elif m and len(m.group(1)) == 1:
            continue  # document title, ignored
        elif h3 or h2:
            (h3 or h2).body.append((n, line))
    return sections


def parse_content(body: list[tuple[int, str]]) -> Content:
    paragraphs: list[tuple[int, str]] = []
    items: list[Item] = []
    current: Item | None = None
    in_fence = prev_blank = False
    for n, line in body:
        stripped = line.strip()
        if FENCE_RE.match(line):
            in_fence = not in_fence
        if not stripped:
            prev_blank = True
            continue
        m = None if in_fence else LIST_RE.match(line)
        if m and len(m["indent"]) < 2:
            kind = "ordered" if m["marker"][0].isdigit() else "bullet"
            current = Item(n, kind, m["text"].strip())
            items.append(current)
        elif current and (line[:1].isspace() or in_fence or not prev_blank):
            if not m:  # nested list items are allowed but not part of the item text
                current.text += " " + stripped
        else:
            current = None
            paragraphs.append((n, stripped))
        prev_blank = False
    return Content(paragraphs, items)


# --------------------------------------------------------------------------- validation


@dataclass
class Issue:
    severity: str  # "error" | "warning"
    line: int | None
    where: str
    message: str


@dataclass
class Report:
    file: str
    issues: list[Issue] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)

    def error(self, line, where, msg):
        self.issues.append(Issue("error", line, where, msg))

    def warn(self, line, where, msg):
        self.issues.append(Issue("warning", line, where, msg))

    def count(self, severity: str) -> int:
        return sum(i.severity == severity for i in self.issues)

    def ok(self, strict: bool = False) -> bool:
        return self.count("error") == 0 and (not strict or self.count("warning") == 0)


def validate_dossier(dossier_path: Path, t: Template) -> Report:
    report = Report(str(dossier_path))
    try:
        text = dossier_path.read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeDecodeError) as e:
        report.error(None, "file", f"cannot read dossier: {e}")
        return report

    fm, body, offset = split_frontmatter(text)
    status = _check_metadata(fm, t, report)
    found = parse_headings(body, offset)
    matched = _match_headings(
        [s.title for s in t.sections], found, "section", "##", "document", report)

    statuses = t.status_field.options if t.status_field else []
    for s in t.sections:
        node = matched.get(_norm(s.title))
        if node is None:
            continue
        if s.required_at and status in statuses and statuses.index(status) < statuses.index(s.required_at):
            report.skipped.append(
                f"{s.title} (content checked from status '{s.required_at}')")
            _match_headings([b.title for b in s.subsections],
                            node.children, "subsection", "###", s.title, report)
            continue
        if s.block:
            if node.children:
                report.error(
                    node.children[0].line, s.title, "unexpected '###' subsection; this section has no subsections")
            _check_block(s.block, parse_content(
                node.body), s.title, node.line, report)
            continue
        if any(line.strip() for _, line in node.body):
            first = next(n for n, line in node.body if line.strip())
            report.warn(first, s.title,
                        "content before the first subsection is ignored")
        subs = _match_headings([b.title for b in s.subsections],
                               node.children, "subsection", "###", s.title, report)
        for b in s.subsections:
            if (sub := subs.get(_norm(b.title))) is not None:
                _check_block(b, parse_content(sub.body), f"{
                             s.title} › {b.title}", sub.line, report)
    return report


def _check_metadata(fm: str | None, t: Template, report: Report) -> str | None:
    if fm is None:
        report.error(
            1, "frontmatter", "missing YAML frontmatter (the file must start with '---')")
        return None
    try:
        data = yaml.safe_load(fm) or {}
    except yaml.YAMLError as e:
        report.error(1, "frontmatter", f"invalid YAML: {e}")
        return None
    if not isinstance(data, dict):
        report.error(1, "frontmatter", "frontmatter must be a mapping")
        return None

    line_of = {m.group(1): i + 2 for i, l in enumerate(fm.splitlines())
               if (m := re.match(r"^([\w-]+)\s*:", l))}
    known = {f.name for f in t.metadata}
    for f in t.metadata:
        value, line = data.get(f.name), line_of.get(f.name, 1)
        if value is None or str(value).strip() == "":
            if f.required:
                report.error(line, f"metadata.{
                             f.name}", "required field is missing or empty")
        elif f.type == "enum" and str(value) not in f.options:
            report.error(line, f"metadata.{f.name}", f"{
                         value!r} is not one of: {', '.join(f.options)}")
        elif f.type == "string" and not isinstance(value, str):
            report.error(line, f"metadata.{f.name}", f"expected a string, got {
                         type(value).__name__}")
        elif f.type == "string" and PLACEHOLDER_RE.fullmatch(value.strip()):
            report.error(line, f"metadata.{f.name}",
                         f"unfilled placeholder {value!r}")
    for key in data.keys() - known:
        report.warn(line_of.get(key, 1), f"metadata.{
                    key}", "unknown field (not in template)")
    status = data.get("status")
    return str(status) if status is not None else None


def _match_headings(expected, found, kind, hashes, where, report) -> dict[str, Heading]:
    """Map normalized expected titles to found headings; report missing/duplicate/unknown/out-of-order."""
    wanted = {_norm(e): e for e in expected}
    matched: dict[str, Heading] = {}
    for h in found:
        key = _norm(h.title)
        if key in matched:
            report.error(h.line, where, f"duplicate {
                         kind} '{hashes} {h.title}'")
        elif key in wanted:
            matched[key] = h
        else:
            close = difflib.get_close_matches(
                h.title, expected, n=1, cutoff=0.6)
            hint = f"; did you mean '{hashes} {close[0]}'?" if close else ""
            report.warn(h.line, where, f"unknown {
                        kind} '{hashes} {h.title}'{hint}")
    for title in expected:
        if _norm(title) not in matched:
            report.error(None, where, f"missing {kind} '{hashes} {title}'")

    order = [matched[_norm(e)] for e in expected if _norm(e) in matched]
    for prev, cur in zip(order, order[1:]):
        if cur.line < prev.line:
            report.error(cur.line, where, f"{kind} '{
                         cur.title}' must come after '{prev.title}'")
    return matched


def _check_block(b: Block, c: Content, where: str, heading_line: int, report: Report) -> None:
    if b.format == "string":
        if c.items:
            report.error(c.items[0].line, where,
                         "expected prose paragraphs, found a list")
        if not c.paragraphs and not c.items:
            if b.required:
                report.error(heading_line, where, "required content is empty")
            return
        for n, text in c.paragraphs:
            _check_placeholders(text, b, n, where, report)
        return

    want = "ordered" if b.format == "ordered_list" else "bullet"
    marker = "1." if want == "ordered" else "-"
    for n, _ in c.paragraphs[:1]:
        report.error(n, where, f"unexpected prose; expected a {
                     FORMATS[b.format]} (every line should start with '{marker}')")

    items = c.items
    if len(items) == 1 and NONE_RE.match(items[0].text):
        if b.required:
            report.error(
                items[0].line, where, "required list cannot be 'None'; add at least one item")
        return
    if not items:
        if b.required:
            report.error(heading_line, where, f"required {
                         FORMATS[b.format]} is empty")
        return

    for i, item in enumerate(items, 1):
        if item.kind != want:
            report.error(item.line, where, f"item {
                         i} uses the wrong list type; expected '{marker}' items")
        if _check_placeholders(item.text, b, item.line, where, report):
            continue
        if b.pattern and not b.pattern.match(item.text):
            report.error(item.line, where, f"item {
                         i} does not match schema: {b.item_schema}")


def _check_placeholders(text: str, b: Block, line: int, where: str, report: Report) -> bool:
    left = [p for p in PLACEHOLDER_RE.findall(
        text) if p.strip().casefold() in b.placeholders]
    if left:
        report.error(line, where, "unfilled placeholder " +
                     ", ".join(f"<{p}>" for p in left))
    return bool(left)


# --------------------------------------------------------------------------- CLI


def format_report(r: Report, strict: bool) -> str:
    verdict = "VALID" if r.ok(strict) else "INVALID"
    out = [f"{r.file}: {verdict} ({r.count('error')} errors, {
        r.count('warning')} warnings)"]
    for i in sorted(r.issues, key=lambda i: (i.line or 0, i.severity)):
        loc = f"{r.file}:{i.line}" if i.line else r.file
        out.append(f"{loc}: {i.severity}: [{i.where}] {i.message}")
    for s in r.skipped:
        out.append(f"note: not yet checked: {s}")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-t", "--template", type=Path, default=DEFAULT_TEMPLATE,
                        help="YAML template (default: %(default)s)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_render = sub.add_parser(
        "render", help="render the template as a fill-in Markdown dossier")
    group = p_render.add_mutually_exclusive_group()
    group.add_argument("-o", "--output", type=Path,
                       help="write to this file instead of stdout")
    group.add_argument("--check", type=Path, metavar="FILE",
                       help="exit 1 if FILE differs from a fresh render")

    p_val = sub.add_parser(
        "validate", help="validate a dossier against the template")
    p_val.add_argument("dossier", type=Path)
    p_val.add_argument("--json", action="store_true",
                       help="machine-readable output")
    p_val.add_argument("--strict", action="store_true",
                       help="treat warnings as failures")

    args = parser.parse_args(argv)
    try:
        template = load_template(args.template)
    except TemplateError as e:
        print(f"template error: {e}", file=sys.stderr)
        return 2

    if args.command == "render":
        md = render_markdown(template)
        if args.check:
            current = args.check.read_text(
                encoding="utf-8") if args.check.exists() else ""
            if current == md:
                print(f"{args.check}: up to date")
                return 0
            print(
                f"{args.check}: out of date; re-run 'render -o {args.check}'", file=sys.stderr)
            return 1
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(md, encoding="utf-8")
            print(f"wrote {args.output}")
        else:
            sys.stdout.write(md)
        return 0

    report = validate_dossier(args.dossier, template)
    if args.json:
        payload = {
            "file": report.file,
            "valid": report.ok(args.strict),
            "errors": report.count("error"),
            "warnings": report.count("warning"),
            "issues": [asdict(i) for i in report.issues],
            "not_yet_checked": report.skipped,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(format_report(report, args.strict))
    return 0 if report.ok(args.strict) else 1


if __name__ == "__main__":
    sys.exit(main())
