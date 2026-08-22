# physicianaidindlying

**A continuously updated policy reference on physician aid in dying.**

All 51 US jurisdictions, 22 international regimes, and — the part that is usually
missing from legislative debate — what each policy lever actually does to access once
a law is on the books.

**Live site:** https://clinical-trials.github.io/physicianaidindlying/

---

## Who this is for

Legislators and legislative staff, health department policy teams, clinicians deciding
whether to participate, hospice and health system administrators writing institutional
policy, and journalists.

It is a reference, not an argument. Where the evidence cuts against a common talking
point — in either direction — it says so.

---

## Why it exists

Fourteen US jurisdictions now authorize medical aid in dying, covering roughly a third
of Americans. Three of them arrived in the last fourteen months. Every state debating a
bill asks the same questions, and the answers exist — in Dutch review committee reports,
Australian board annual reports, Oregon's twenty-eight-year data series, Canadian
practitioner data — but they are scattered across a dozen languages and government
websites, and they rarely reach a committee hearing.

Three findings shape everything here:

1. **Supply, not demand, is the binding constraint.** New Mexico has the most permissive
   prescriber statute in the country and fielded **26 prescribers** statewide in 2025.
   In Canada, **89 practitioners delivered 64%** of all cases in 2023. In New South Wales,
   **45.7% of authorised practitioners supported zero patients.**

2. **Volume is set by friction and workforce, not by the breadth of the right.** Germany
   has the broadest right in Europe and no regulatory framework at all. Austria has
   comparable eligibility, a 12-week waiting period, and roughly **one tenth** the
   per-capita uptake of Switzerland. Italy has a constitutional right, a public
   gatekeeper, no implementing statute, and **15 deaths in seven years**.

3. **A third of people who obtain the medication never take it.** Oregon 33% cumulative,
   Queensland 36.4%, Austria roughly a third of declarations, and 220 documented German
   green-lights declined in a single year. Four jurisdictions, four regulatory designs,
   one consistent finding. The option itself does work the act never does.

---

## How it is built

```
physicianaidindlying/
├── index.html          # the tracker — reads data at runtime, no build step
├── data/
│   └── policy.json     # SINGLE SOURCE OF TRUTH — this is the file you edit
├── scripts/
│   └── validate.py     # schema and freshness check
├── UPDATING.md         # the update protocol
└── README.md
```

**Data is separated from presentation on purpose.** Updating a waiting period or adding
a newly enacted state is a one-field edit to `data/policy.json` and a pull request.
Nobody has to touch HTML, and there is no build step, no framework, and no dependency
to keep current.

### Run it locally

```bash
python3 -m http.server
```

Then open <http://localhost:8000>. The page fetches `data/policy.json` at runtime, so it
must be served over HTTP rather than opened from the filesystem.

### Validate before committing

```bash
python3 scripts/validate.py
```

---

## Evidentiary standard

- Every field is sourced to a primary document where one could be obtained — enrolled
  statutes, health department annual reports, review commission publications, court
  decisions.
- **Fields that could not be verified read `not verified`.** They are never estimated,
  inferred, or filled from a secondary summary presented as primary.
- Where sources conflict, both figures appear with their denominators. Swiss resident
  and organisation-based counts, for example, measure different populations and must
  never be merged.
- Derived figures are labelled as arithmetic, not as published statistics.

**This is not legal advice.** Public compilations of assisted-dying law are frequently
out of date and contradict one another. Verify against primary statute with licensed
counsel in the relevant jurisdiction before relying on anything here.

---

## Contributing

Corrections are the most valuable contribution, particularly from people who work inside
these systems.

1. Edit `data/policy.json`.
2. Run `python3 scripts/validate.py`.
3. Open a pull request citing the primary source for the change.

See [UPDATING.md](UPDATING.md) for the field-by-field protocol and the review cadence.

Known gaps are tracked as issues and are labelled `not verified` in the data itself
rather than hidden. Current priorities: clause-level verification of Washington,
Vermont, Maine, New Jersey and DC; Canada's Track 2 and mental-illness track status;
Quebec's advance-request regime; Victoria, Western Australia, South Australia, Tasmania,
ACT and NT; Spain, Portugal and Ireland.

---

## Status

**v0.1.0 — first draft.** Structure and evidentiary standard are settled; coverage is
uneven and labelled as such.

## License

Data and text: CC BY 4.0. Code: MIT.
