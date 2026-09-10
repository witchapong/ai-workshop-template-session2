import numpy as np
import pytest

from core.spectrum import make_signal, peak_frequency, spectrum

FS = 1000.0
DURATION = 1.0


def test_a_50_hz_sine_peaks_at_50_hz():
    _, signal = make_signal([(50.0, 1.0)], FS, DURATION)
    freqs, magnitudes = spectrum(signal, FS)
    assert peak_frequency(freqs, magnitudes) == pytest.approx(50.0)


def test_a_one_volt_sine_shows_an_amplitude_of_one():
    _, signal = make_signal([(50.0, 1.0)], FS, DURATION)
    freqs, magnitudes = spectrum(signal, FS)
    assert magnitudes[np.argmax(magnitudes)] == pytest.approx(1.0, abs=0.001)


def test_two_tones_each_show_their_own_amplitude():
    _, signal = make_signal([(50.0, 1.0), (120.0, 0.5)], FS, DURATION)
    freqs, magnitudes = spectrum(signal, FS)
    assert magnitudes[freqs == 50.0][0] == pytest.approx(1.0, abs=0.001)
    assert magnitudes[freqs == 120.0][0] == pytest.approx(0.5, abs=0.001)


def test_a_constant_offset_appears_at_zero_hz():
    _, signal = make_signal([(50.0, 1.0)], FS, DURATION)
    freqs, magnitudes = spectrum(signal + 2.0, FS)
    assert magnitudes[0] == pytest.approx(2.0, abs=0.001)


def test_the_frequency_axis_stops_at_half_the_sampling_rate():
    _, signal = make_signal([(50.0, 1.0)], FS, DURATION)
    freqs, _ = spectrum(signal, FS)
    assert freqs[0] == 0.0
    assert freqs[-1] == pytest.approx(FS / 2)


def test_one_second_of_signal_gives_one_hertz_resolution():
    _, signal = make_signal([(50.0, 1.0)], FS, DURATION)
    freqs, _ = spectrum(signal, FS)
    assert freqs[1] - freqs[0] == pytest.approx(1.0)


def test_a_negative_sampling_rate_is_rejected():
    with pytest.raises(ValueError, match="positive"):
        make_signal([(50.0, 1.0)], -1000.0, 1.0)
