from Neuroprosthetics.filter_banks import *
from scipy.signal import hilbert, chirp

# generate randomn noise
def noise_generator(num_channels, gain=1, signal_duration=1, fs=44.1e3, order=4):
    bandpassed_noise_channels = []
    samples = int(signal_duration*fs)
    noise = np.random.normal(loc=0.0, scale=1.0, size=samples)*gain
    noise_filters = generate_CI_filterbanks(num_channels, fs, order=order)

    for i, f in enumerate(noise_filters):
        bandpassed_noise_channels.append(butter_bandpass_filter(noise, *f))
    return np.array(bandpassed_noise_channels)


def extract_envelopes(channels, fs=44.1e3, low_pass=True, cutoff=30):

    analytic_signal = hilbert(channels)
    raw_envelopes = np.abs(analytic_signal)

    if low_pass:
        lowpass_filter = signal.dlti(*signal.tf2ss(
            *signal.butter(2, cutoff / (.5 * fs), btype='lowpass')))
        envelopes = np.zeros_like(raw_envelopes)
        for i, channel in enumerate(raw_envelopes):
            t, y, _ = signal.dlsim(lowpass_filter, channel)
            envelopes[i, :] = np.squeeze(y)
    else:
        envelopes = raw_envelopes

    mins = np.min(envelopes, axis=1)
    maxs = np.max(envelopes, axis=1)
    diffs = maxs - mins

    return (envelopes - mins[:, np.newaxis]) / diffs[:, np.newaxis]

def compress_envelopes(env, c=500, lower_clip=0.2):

    env_comp = np.log10(1+c*env)/np.log10(c+1)

    # clip array
    env_comp[env_comp > 1] = 1
    env_comp[env_comp < lower_clip] = 0

    return env_comp


def vocoder(env_compressed, noise, audio_signal):
    vocoder_channels = env_compressed * noise
    summed_channels = np.sum(vocoder_channels, axis=0)
    summed_channels *= .5*np.max(audio_signal)/np.max(summed_channels)

    return vocoder_channels, summed_channels
