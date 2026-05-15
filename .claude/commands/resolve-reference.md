# Resolve or Change an @ Reference

Use this skill to change where an `@` reference points, or to inline the resolved text directly
into a liturgical proper file.

## What this skill does

Given a file path (e.g. `backend/resources/divinum-officium-local/web/www/missa/Portugues/Sancti/05-15.txt`)
and a section name (e.g. `Evangelium`), this skill will:

1. Show the current reference line in that section.
2. Show what the reference resolves to (the actual text).
3. Offer three options:
   - **Repoint** — change the `@path:section` to a different source.
   - **Inline** — replace the reference with the resolved text directly in the file.
   - **Remove** — delete the reference line entirely.

## How to invoke

```
/resolve-reference
```

Then describe what you want, for example:
- "In `Sancti/05-15.txt` Portuguese, the Evangelium reference `@Sancti/01-31:Evangelium` should point to `@Sancti/02-15:Evangelium` instead."
- "Inline the Gospel text for `@Sancti/01-31:Evangelium` in `Portugues/Sancti/05-15.txt`."

## Steps Claude will follow

1. **Locate the file** — determine if the edit should go in `divinum-officium-local` (preferred for
   project-specific overrides) or `divinum-officium` (the submodule, avoid editing directly).

   Local override path pattern:
   ```
   backend/resources/divinum-officium-local/web/www/missa/<Language>/<Category>/<file>.txt
   ```

   If the local override file does not exist yet, create it by copying only the relevant section
   from the submodule file.

2. **Read the file** to confirm the exact reference line.

3. **Resolve the reference** by reading the target file and extracting the target section.

4. **Apply the change**:
   - Repoint: edit the `@path:section` string.
   - Inline: replace the `@...` line with the resolved section body lines.
   - Remove: delete the line.

5. **Verify** the edit looks correct, then commit to branch `claude/add-liturgical-content-q5WkH`.

## Reference format reminder

```
@<path>:<section>[:<substitutions>]
```

Examples:
```
@Sancti/01-31:Evangelium
@Commune/C5:Introitus
@:Graduale
```

See `docs/adr/001-at-reference-system.md` for full documentation.

## Notes

- Always prefer editing files in `divinum-officium-local`, not the submodule.
- When inlining, preserve scripture citation lines (lines starting with `*`) above the resolved body.
- If the reference has substitutions (`s/from/to/`), apply them manually when inlining.
