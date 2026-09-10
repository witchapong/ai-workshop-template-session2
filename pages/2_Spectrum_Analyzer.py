"""Lab 1 reference solution: a two-tone spectrum analyser."""

import matplotlib.pyplot as plt
import streamlit as st

from core.spectrum import make_signal, peak_frequency, spectrum

st.title("Spectrum Analyser")
st.caption("Build a signal from two sine waves and see what it is made of.")

fs = st.select_slider("Sampling rate (samples per second)", [500, 1000, 2000, 4000], 1000)

left, right = st.columns(2)
freq_a = left.number_input("Tone A frequency (Hz)", 1.0, float(fs) / 2, 50.0, step=1.0)
amp_a = left.number_input("Tone A amplitude", 0.0, 5.0, 1.0, step=0.1)
freq_b = right.number_input("Tone B frequency (Hz)", 1.0, float(fs) / 2, 120.0, step=1.0)
amp_b = right.number_input("Tone B amplitude", 0.0, 5.0, 0.5, step=0.1)

times, signal = make_signal([(freq_a, amp_a), (freq_b, amp_b)], fs, duration=1.0)
freqs, magnitudes = spectrum(signal, fs)

st.metric("Strongest frequency", f"{peak_frequency(freqs, magnitudes):,.1f} Hz")

figure, (top, bottom) = plt.subplots(2, 1, figsize=(7, 6))
top.plot(times[:200], signal[:200], linewidth=1)
top.set_xlabel("Time (seconds)")
top.set_ylabel("Amplitude")
top.set_title("The signal (first 200 samples)")
top.grid(alpha=0.3)

bottom.stem(freqs, magnitudes, markerfmt=" ", basefmt=" ")
bottom.set_xlim(0, min(fs / 2, max(freq_a, freq_b) * 2))
bottom.set_xlabel("Frequency (Hz)")
bottom.set_ylabel("Amplitude")
bottom.set_title("What it is made of")
bottom.grid(alpha=0.3)

figure.tight_layout()
st.pyplot(figure)

st.info(
    f"Check it yourself: tone A is {amp_a} at {freq_a:.0f} Hz. "
    "The spike should reach that height. If it does not, the scaling is wrong."
)
