# Update protocol

The value of this tracker is that it is current and that its uncertainty is honest.
Both degrade quickly without a routine. This is the routine.

---

## Cadence

| Trigger | Action | Turnaround |
|---|---|---|
| **A bill is signed** | Add or move the jurisdiction; set `effective`; mark unverified fields | 48 hours |
| **A law takes effect** | Re-verify every field against the enrolled statute, not the bill as introduced | Same week |
| **An annual report drops** | Update `utilization` verbatim, with the year and the denominator | 1 week |
| **A court rules** | Update the affected fields and note the decision in `note` | 1 week |
| **Routine sweep** | Walk every `not verified` field and every legislative session status | Monthly — set `meta.nextReviewDue` |

Legislative sessions cluster. January through May is the heavy period for US state
bills; check the pipeline weekly in those months.

---

## The rules

**1. Primary sources or nothing.**
Enrolled statute text, health department annual reports, review commission publications,
court decisions, official forms. Advocacy summaries and news reporting are leads, not
sources — and both frequently describe *the bill as introduced* rather than *the law as
enacted*.

> A worked example of why this matters. New Mexico's introduced HB 47 had 13 sections;
> the enacted Act has 8. The death-certificate provision, the insurance provision, the
> civil-immunity language and the guardianship protection were **all dropped before
> enactment**. Most public summaries of the New Mexico law describe provisions that
> are not in it.

**2. `not verified` is a valid, respectable value.**
Never estimate. Never infer from a neighbouring state. Never carry a figure forward from
a secondary summary and present it as primary. A labelled gap is useful; a confident
error is worse than silence and destroys the credibility of every field around it.

**3. Give every number a year and a denominator.**
"5.1% of deaths" is meaningless without knowing which deaths, counted by whom, in which
year. Swiss resident counts and organisation-based counts differ by roughly 14% because
one excludes non-residents — **they must never be added or reconciled.**

**4. Mark derived figures as derived.**
If you computed it, say so. Queensland's cumulative total is arithmetic from a table,
not a published statistic. Label it.

**5. Preserve conflicts; do not resolve them silently.**
When two official sources disagree, record both and say which is more authoritative and
why. New Mexico's own annual report gives an effective date that contradicts the
statutory record. Both belong in the file.

**6. Quote statutory language for anything consequential.**
Waiting periods, prescriber definitions, conscience duties and immunity provisions turn
on exact wording. Paraphrase loses the thing that matters.

**7. Log every change.**
Append to `meta.changelog` with the date and what changed. Bump `meta.version`
(minor for new content, patch for corrections). Update `meta.lastUpdated`.

---

## Adding a US jurisdiction

Add an object to `usAuthorizing`. Required fields:

| Field | Notes |
|---|---|
| `jurisdiction`, `abbr` | Full name and postal abbreviation |
| `authorized`, `effective` | Year signed; ISO date it becomes operative. **These differ, often by a year.** |
| `statute`, `citation` | Popular name and code citation |
| `mechanism` | `statute`, `ballot initiative`, or `court` |
| `prescribers` | Exact scope. If APPs may prescribe, state any physician-attestation requirement — New Mexico authorises APRNs and PAs *and* requires an MD/DO in every case. |
| `prognosis` | Currently 6 months in every US jurisdiction |
| `waitingPeriod` | Duration, **what starts the clock**, and the waiver conditions. A dispensing restriction is not a deliberation period. |
| `residency` | Required or not; note any documentation or physical-presence rule |
| `telehealth` | Permitted, prohibited, or silent. Note that the federal Ryan Haight Act constrains remote controlled-substance prescribing regardless of state law. |
| `mentalHealth` | Routine-if-questioned, or mandatory for every patient |
| `selfAdminOnly` | `true` everywhere in the US so far |
| `civilImmunity` | Do not assume. New Mexico has criminal and licensure immunity and **no civil immunity at all.** |
| `utilization` | Latest published figures with year and source |
| `notes` | Anything operationally consequential |
| `sources` | Array of primary-source URLs |

Then remove the state from `usProhibitionBasis` and from `usPipeline2026`.

## Adding an international regime

Add to `international`. Beyond the parallel fields, always capture:
`modality` (clinician administration or self-administration only — the single largest
driver of utilization), `oversight` (prospective or retrospective), `funding` (who pays,
and whether the clinician is paid at all), and `commercial` (whether provision for
profit is barred, and by what mechanism — statute, criminal-law element, or payment
structure).

---

## Before you commit

```bash
python3 scripts/validate.py
python3 -m http.server   # then eyeball http://localhost:8000
```

Check that new tags render, that long `utilization` strings do not break the layout, and
that the page still works in both light and dark mode.

---

## What not to add

- Editorial framing. State what the law says and what the data shows.
- Estimates dressed as data.
- Provider names, patient details, or anything identifying. Several jurisdictions make
  this information statutorily confidential — New Mexico's reporting is exempt from
  public-records disclosure by statute — and it is not ours to publish regardless.
