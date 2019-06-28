import numpy as np


def mono_phasic_current_pulse(t, pulse_amplitude, pulse_duration=1,
                              pulse_position=5):
    if pulse_position <= t < pulse_position + pulse_duration:
        return pulse_amplitude
    else:
        return .0


def bi_phasic_current_pulse(t, pulse_amplitude, pulse_duration=1,
                            pulse_position=5):

    if pulse_position <= t < pulse_position + pulse_duration:
        return -pulse_amplitude
    elif pulse_position + pulse_duration <= t < pulse_position + 2 * pulse_duration:
        return pulse_amplitude
    else:
        return .0
