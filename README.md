# SCF skills

## Design choices
See [CONVENTIONS.md](CONVENTIONS.md)


## Attribution
*Grilling protocol adapted from Matt Pocock's `grilling` skill (github.com/mattpocock/skills).*


## Dossier Templates

A dossier is a Markdown document with a fixed structure: YAML-style front matter followed by numbered `##` sections. The structure is defined by a **JSON template**, which is the single source of truth for two tools:

| Tool | What it does |
|---|---|
| `dossier-renderer` | Reads a template and prints an empty Markdown skeleton with placeholders and hint comments. |
| `dossier-validator` | Checks a filled Markdown dossier against the same template and reports errors with line numbers. |

Because both tools read the same template, adding a new kind of dossier means writing **one JSON file**. No code changes are needed.

```sh
dossier-renderer my-template.json > dossier.md     # 1. generate the skeleton
vim dossier.md                                 # 2. fill it in
dossier-validator dossier.md my-template.json      # 3. check it (exit 0 = VALID, 1 = INVALID, 2 = usage)
```

Both tools need Python 3.8+ and only the standard library. Both currently **require** the template path as an argument (see [Known quirks](#known-quirks)).

---

### Template anatomy

```json
{
  "version": "1.0",
  "metadata": { ... },
  "sections": [ ... ]
}
```

| Key | Required | Notes |
|---|---|---|
| `version` | no | Informational only; neither tool reads it. |
| `metadata` | yes | Front-matter keys, in output order. Use `{}` if you need none. |
| `sections` | yes | Ordered list of `##` sections. |

#### Metadata

Each key in `metadata` becomes a front-matter line. **Every metadata key is required**: there is no optional metadata. The value may be a plain string or an object.

| Spec | Rendered as | Validated as |
|---|---|---|
| `"string"` (any string) | `key: <key>` | Non-empty and not a bare `<placeholder>`. |
| `{ "options": [...], "default": "..." }` | `key: <default>  # one of: a \| b` | Must be exactly one of `options`. Without `default`, the first option is used. |
| `{ "schema": "..." }` | `key: <key>` | Must match the [schema](#schema-mini-language). |

`type` and `prompt` inside a metadata object are documentation only; neither tool reads them (the renderer does not show the metadata `prompt`).

When reading front matter, the validator strips surrounding quotes and drops anything after ` #` (space-hash), which is how the `# one of:` hint is ignored.

#### Sections and subsections

A section is one of two shapes:

```jsonc
// A section that is itself a block
{ "title": "5. Decision Log", "format": "bullet_list", ... }

// A section that groups subsections (each subsection is a block)
{ "title": "1. Task Brief", "subsections": [
    { "title": "Problem Statement", "format": "string", ... },
    { "title": "Acceptance Criteria", "format": "ordered_list", ... }
] }
```

Section titles become `## <title>` and subsection titles become `### <title>`. The validator matches headings **by exact text**, so any numbering you put in the title (`"1. Scope"`) becomes part of the heading the author must write. Headings must appear in template order.

#### Blocks

A block is anything with a `format`. These keys apply to all blocks:

| Key | Meaning |
|---|---|
| `format` | `string`, `ordered_list`, `bullet_list`, or `entries`. |
| `required` | Defaults to `true`. With `false`, the content may be empty or `None`, but **the heading itself must still be present**. |
| `prompt` | Text shown as the placeholder: rendered as `<prompt>` in lowercase, with a trailing period removed. Falls back to the block title. |
| `item_schema` | For lists only. A [schema](#schema-mini-language) each item must match. When present, it is shown instead of `prompt`. |

##### `string`

Free prose. Any list item under the heading is an error. A required block with no prose is an error.

##### `ordered_list` and `bullet_list`

Every top-level line must be a list item: `1.` or `1)` for ordered lists, `-`, `*` or `+` for bullet lists. Prose lines are an error, and using the wrong marker is an error. The numbers in an ordered list are not checked.

Items whose whole text is `None` or `N/A` (case-insensitive, optionally wrapped in `_` / `*`, trailing period allowed) are ignored. A required list that only contains such items fails. To mark an optional list as empty, write the item **as a list item** (`- None` or `1. N/A`), not as a bare line.

Indented lines are ignored entirely, so authors can add nested sub-bullets or continuation lines without breaking validation. The schema only applies to top-level items.

##### `entries`

A repeatable group of `###` headings, each carrying a fixed set of `- **Field**: value` lines. Use it for numbered records such as impacts, obligations, or test cases.

| Key | Meaning |
|---|---|
| `heading_schema` | [Schema](#schema-mini-language) every entry heading must match, e.g. `"I<n> — <title>"`. |
| `fields` | Ordered list of field specs (below). |
| `required` | With `true` (the default), at least one entry must exist. |

Each field spec:

| Key | Meaning |
|---|---|
| `name` | Field label, written as `- **<name>**: value`. |
| `prompt` | Placeholder text if there is no `options`/`schema`. Unlike block prompts, it is **not** lowercased. |
| `options` | Value must equal one of these exactly (case-sensitive). |
| `schema` | A schema string, or a **list** of alternative schemas. The value must match at least one. |

Every field is required in every entry; there is no per-field `required`. Field values must be on a single line. Extra, unknown fields are ignored. If a field has both `options` and `schema`, only `options` is checked.

> **`entries` is only valid as a section-level format**, never inside `subsections`. Entries are `###` headings, and subsections are `###` headings too, so the two would collide. Every `###` under an entries section is treated as an entry.

---

### Schema mini-language

`item_schema`, `heading_schema`, field `schema` and metadata `schema` all use the same syntax. A schema is literal text mixed with `<...>` tokens. The entire value must match: it is anchored at both ends.

| Token | Matches | Example |
|---|---|---|
| `<n>` | One or more digits | `Q<n>` matches `Q12` |
| `<a \| b \| c>` | Exactly one of the listed alternatives (separator is space-pipe-space) | `<origin \| upstream \| downstream>` |
| `<anything else>` | Any non-empty text | `<rationale>` |
| Literal text | Itself, verbatim (including backticks, `**`, parentheses) | `(Settled in: Q<n>)` |

The em dash `—` in a schema also accepts an en dash `–` or a hyphen `-`, so `T<n> — <title>` accepts `T2 – Title` and `T2 - Title`.

The text inside a free-text token is only a hint for the author. `<impact ids, e.g. I1, I2>` accepts any non-empty text; the format of the ids is not enforced. If you need structure, put it in the literal part of the schema.

Tokens cannot nest, and a `<` or `>` inside a token is not supported.

### How "unfilled" is detected

The renderer writes placeholders such as `<what is being tested and why>`. The validator treats a value as unfilled when it still contains a `<...>` whose text (case-insensitive) is one of the placeholder names from that block's `item_schema`/`prompt`, or from that field's example. In practice, this has three consequences:

1. Keep `prompt` text free of `<`, `>` and line breaks, because the whole prompt becomes a placeholder name.
2. Placeholders left in an **optional** block are still errors. The author must fill the block or replace the placeholder with `None`.
3. Real content that happens to contain angle brackets (`List<T>`, `<div>`) is fine as long as the text inside does not match a placeholder name. However, see the schema quirk under [Known quirks](#known-quirks).

HTML comments (`<!-- ... -->`), including the renderer's hints, are stripped before validation and can be left in place.

---

## Creating a new template: walkthrough

This example builds a test plan template that uses every feature.

### 1. Sketch the target document

Write by hand the Markdown you want authors to produce. Decide which parts are prose, which are lists, and which are repeatable records with fixed fields. Decide which parts may be empty.

### 2. Write the template

`test-plan.json`:

```json
{
  "version": "1.0",
  "metadata": {
    "task_name": "string",
    "ticket": { "type": "string", "schema": "<PROJ | OPS>-<n>" },
    "status": { "type": "enum", "options": ["Draft", "Reviewed", "Approved"], "default": "Draft" }
  },
  "sections": [
    {
      "title": "1. Scope",
      "subsections": [
        { "title": "Summary", "format": "string", "prompt": "What is being tested and why." },
        { "title": "Components", "format": "bullet_list", "item_schema": "`<path or module>` — <what changes>" },
        { "title": "Not Tested", "format": "bullet_list", "prompt": "Item", "required": false }
      ]
    },
    {
      "title": "2. Test Cases",
      "format": "entries",
      "heading_schema": "T<n> — <title>",
      "fields": [
        { "name": "Level", "options": ["Unit", "Integration", "E2E"] },
        { "name": "Steps", "prompt": "Short description of the steps" },
        { "name": "Expected", "prompt": "Observable result" },
        { "name": "Covers", "schema": "<acceptance criteria ids, e.g. AC1, AC2>" }
      ]
    },
    {
      "title": "3. Run Order",
      "format": "ordered_list",
      "item_schema": "T<n> — <reason>",
      "required": false
    }
  ]
}
```
