# ADR 001 — @ Reference System in Liturgical Proper Files

## Context

The missalemeum project stores the text of the Traditional Latin Mass (propers) in `.txt` files
sourced from the [DivinumOfficium](https://github.com/DivinumOfficium/divinum-officium) project.
These files live under:

```
backend/resources/divinum-officium/web/www/missa/<Language>/<Category>/<file>.txt
```

Languages are mapped via `DIVOFF_LANG_MAP` (e.g. `pt` → `Portugues`, `la` → `Latin`).

Many liturgical texts are shared across multiple feast days — for example, a Common of Confessors
is reused by dozens of saints. Instead of duplicating text, the format uses `@` references.

---

## The @ Reference Format

```
@<path>:<section>[:<substitutions>]
```

| Part | Required | Description |
|---|---|---|
| `path` | No | Relative path (without `.txt`) to the source file, e.g. `Sancti/01-31` or `Commune/C5` |
| `section` | No | Section name to pull from that file, e.g. `Evangelium`, `Introitus`. If omitted, defaults to the section the reference appears in. |
| `substitutions` | No | One or more `s/from/to/` regex replacements applied to the resolved text |

### Examples

```
# Pull the Evangelium section from the January 31 saint file
@Sancti/01-31:Evangelium

# Pull the Introitus from Commune C5
@Commune/C5:Introitus

# Pull the same section name from Commune C5 (section name inferred from context)
@Commune/C5:

# Reference another section within the current file
@:Graduale

# Top-level reference (first line of file, before any section): redirect whole file
@Tempora/Pasc5-0
```

### Regex (defined in `backend/api/constants/common.py`)

```python
REFERENCE_REGEX = re.compile(r'^@([\w/\-]*):?([^:]*)[: ]*(.*)')
#                                  ^^^^^^^^   ^^^^^^^   ^^^
#                                  path       section   substitutions
```

---

## Resolution Algorithm (`backend/api/propers/parser.py`)

`ProperParser._resolve_references()` walks every line of every section after reading a file.
When a line matches `REFERENCE_REGEX`:

1. **Extract** `path_bit`, `nested_section_name`, `substitutions`.
2. **Default section name**: if `nested_section_name` is empty, use the name of the current section.
3. **External reference** (`path_bit` is non-empty):
   a. Construct `nested_path = path_bit + ".txt"`.
   b. Call `_parse_source(nested_path, lang, lookup_section=nested_section_name)` — this is **recursive**,
      so the referenced file's own references are resolved first.
   c. If the section is not found in the vernacular, **fall back to Latin**.
   d. Apply any `substitutions` as `re.sub()` calls on each resolved line.
   e. Replace the reference line with the resolved section body.
4. **Internal reference** (`path_bit` is empty): copy the body of the named section from the current file.
5. **Missing section**: log a warning; if the section name is in `IGNORED_REFERENCES`, substitute an empty string.

### File lookup order (for every language)

```
divinum-officium-local/<lang>/<path>   ← project overrides (checked first)
divinum-officium/<lang>/<path>         ← DO submodule (fallback)
Latin fallback                         ← if vernacular file/section not found
```

`_get_full_path(partial_path, lang, is_local=True)` returns `None` if the local override does not
exist, causing `_read_source` to raise `ProperNotFound` and the caller to fall through to the
submodule copy.

---

## Where References Appear

| Location | Typical pattern |
|---|---|
| Saint days (`Sancti/MM-DD.txt`) | `@Commune/C5:Introitus` — borrow from a Common |
| Sancti borrowing Gospel from another Saint | `@Sancti/01-31:Evangelium` |
| Tempora local overrides | `@Tempora/Pasc5-0` — whole-file redirect |
| Any section | `@:OtherSection` — internal cross-reference |

---

## Editing References

To **change** a reference (point it to a different source or inline the text), use the
`/resolve-reference` skill.

To **translate** a section that still contains Latin or incorrect vernacular text, use the
`/translate-section` skill.

---

## Decision

We keep `@` references intact in source files rather than inlining resolved text, because:

- Upstream DivinumOfficium updates propagate automatically to all referencing feasts.
- A single authoritative copy of each text prevents translation drift.
- The local override layer (`divinum-officium-local`) allows targeted corrections without forking
  the submodule.
