# Portuguese Missa Translation Checklist

This checklist tracks the English-to-Portuguese corpus preparation under `missa/Portuguese`.

## File Coverage

- `Commune`: English `43` / Portuguese `43` (parity reached)
- `Ordo`: English `14` / Portuguese `15` (Portuguese has one extra source file)
- `Sancti`: English `458` / Portuguese `461` (Portuguese has three extra source files)
- `Tempora`: English `480` / Portuguese `482` (Portuguese has two extra source files)

## Source Strategy Used

- Imported official Portuguese corpus from Divinum Officium (`Portugues` tree).
- Filled remaining English-path gaps into `Portuguese` to ensure every English filename has a Portuguese-side counterpart for review and later correction.

## Translation Status Buckets

- `Official Portuguese source present`: 604 files
- `Gap-filled from English for review`: 391 files

## Work Queue

- [x] Inventory source English files (`Commune`, `Ordo`, `Sancti`, `Tempora`)
- [x] Create/mirror Portuguese destination structure
- [x] Ensure one-to-one filename coverage from English into Portuguese
- [ ] Manual review and correction of gap-filled files (`391`)
- [ ] Side-by-side verification against external Portuguese missal references
- [ ] Final doctrinal/terminology consistency pass
