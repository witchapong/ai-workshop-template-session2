# Gate 2 — Requirements

> **Provisional.** Hand-written so the recovery path works before Task 9A
> Phase C runs. Phase C replaces this with a set captured from a real agent
> run, which is what students should recognise. Until then this is still a
> correct, usable fallback.

Every acceptance criterion below is checked by a test in
`tests/test_spectrum.py`.

| # | Requirement | Acceptance criterion (how we check it) |
|---|---|---|
| 1 | Build a signal by adding two sine waves, each with its own frequency and amplitude | `make_signal([(50.0, 1.0)], 1000, 1.0)` returns 1000 time values and 1000 signal values |
| 2 | Report which frequencies the signal contains | A 50 Hz input produces a peak at exactly 50.0 Hz |
| 3 | Report the correct amplitude for each frequency | A tone entered at amplitude 1.0 reads back as 1.0, within 0.001 |
| 4 | Handle two tones at once | 50 Hz at 1.0 and 120 Hz at 0.5 read back as 1.0 and 0.5 |
| 5 | Handle a constant offset | A DC offset of 2.0 appears at 0 Hz as 2.0, not 4.0 |
| 6 | Cover frequencies up to half the sampling rate | The frequency axis runs 0 Hz to 500 Hz at 1000 samples per second |
| 7 | Reject impossible inputs | A negative sampling rate raises an error mentioning "positive" |

**Approved by:** (your name)
**Date:**
