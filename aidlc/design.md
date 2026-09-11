# Gate 3 — Design

> **Provisional** — see the note in `requirements.md`.

## What data do we store?

Nothing is stored. The app computes from the inputs on screen every time.

| Value | Meaning | Example |
|---|---|---|
| frequency_hz | how fast a tone oscillates | 50.0 |
| amplitude | how tall that tone is | 1.0 |
| fs | sampling rate, samples per second | 1000 |

## What are the screens?

| Page file | What the user does here |
|---|---|
| `pages/2_Spectrum_Analyzer.py` | Sets two tones and a sampling rate, and reads the two charts |

## How does data move?

The user types two frequencies, two amplitudes and a sampling rate.
`make_signal` adds the two sine waves into one array of samples, and `spectrum`
converts that array into a list of frequencies with the strength of each.
The page draws the samples against time, then the strengths against frequency.

**Approved by:**
**Date:**
