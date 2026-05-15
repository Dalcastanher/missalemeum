# Translate a Liturgical Section

Use this skill when a section in a vernacular (Portuguese) proper file contains Latin text,
a missing translation, or an incorrect/outdated translation.

## What this skill does

Given a file and section, this skill will:

1. Show the current text (Latin or wrong vernacular).
2. Produce a faithful liturgical translation into the target language.
3. Write the corrected text into the appropriate file in `divinum-officium-local`.

## How to invoke

```
/translate-section
```

Then describe what you want, for example:
- "The Gradual in `Portugues/Sancti/05-15.txt` still has Latin text, translate it to Portuguese."
- "The Oratio in `Portugues/Tempora/Adv1-0.txt` is wrong, here is the correct text: …"

## Translation guidelines

These are traditional liturgical texts (Tridentine Rite / 1962 Missal). Apply these rules:

| Rule | Detail |
|---|---|
| **Register** | Formal, archaic Portuguese (vós/Vós address, not você). Use forms like "concedei", "dai-nos", "fazei". |
| **God address** | Always capitalise pronouns referring to God: Vós, Vos, Vosso, Ele, Lhe. |
| **Scripture citations** | Preserve book/chapter/verse markers (lines starting with `*`) verbatim; only translate the text lines. |
| **Section headers** | Do not translate `[SectionName]` headers — they are identifiers, not display text. |
| **Diacritics** | Use Portuguese diacritics (ã, ç, é, ê, etc.) correctly. Do not carry over Latin diacritics (æ, œ, ú in Latin words). |
| **Alleluia** | Always rendered as "Aleluia" in Portuguese (not "Alleuia" or "Aleluia"). |
| **Versicle markers** | Keep `V.` and `R.` prefixes; they become `℣.` and `℟.` at render time. |
| **Cross marker** | `++` in source becomes `☩` at render — do not change `++` in the source file. |

## Steps Claude will follow

1. **Identify the file** — determine whether to edit in `divinum-officium-local` or if a local
   override file needs to be created.

   Local override path pattern:
   ```
   backend/resources/divinum-officium-local/web/www/missa/<Language>/<Category>/<file>.txt
   ```

2. **Read the Latin source** from the submodule for reference:
   ```
   backend/resources/divinum-officium/web/www/missa/Latin/<Category>/<file>.txt
   ```

3. **Read the existing vernacular file** (if present) to understand what is already translated.

4. **Translate** — produce the Portuguese text following the guidelines above.
   - Cross-check against the Latin original line by line.
   - Flag any passages that are theologically nuanced and explain the translation choice.

5. **Write the translation** into the correct section of the local override file.

6. **Verify** the result, then commit to branch `claude/add-liturgical-content-q5WkH`.

## Common section names and their Portuguese labels

| Section ID | Portuguese label |
|---|---|
| `Introitus` | Introito |
| `Graduale` | Gradual |
| `Tractus` | Trato |
| `Evangelium` | Evangelho |
| `Lectio` | Epístola |
| `Offertorium` | Ofertório |
| `Communio` | Comunhão |
| `Oratio` | Colecta |
| `Secreta` | Secreta |
| `Postcommunio` | Pós-Comunhão |

## Notes

- Never edit files inside `divinum-officium/` (the submodule) directly.
- If the Portuguese file already exists in `divinum-officium-local`, merge changes into it.
- If only a single section needs overriding, create a minimal local file with only that section
  plus a `[Comment]` block referencing the original.
- After writing, confirm the section body does not start with `@` (that would be a reference, not
  translated text).
