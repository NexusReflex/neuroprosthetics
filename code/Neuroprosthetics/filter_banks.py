import numpy as np
from scipy import signal
from scipy.io import wavfile
from matplotlib import pyplot as plt
import sounddevice as sd
from Neuroprosthetics.plot_utils import set_plot_params


def find_border_frequencies(num_electrodes, min_freq=100, max_freq=8000):
    # bounds are given as exponents to a base, which defaults to 10.0
    return np.logspace(np.log10(min_freq), np.log10(max_freq),
                       num=num_electrodes + 1)


def butterworth_bandpass(f_s, lowcut, highcut, order=2):
    '''
    Create butterworth band-pass filters.

    Args:
        lowcut: border frequency of electrode i
        highcut: border frequency of electrode i+1
        fs: sample frequency

    Returns:
        butter: filter params (b, a)
    '''

    nyq = f_s / 2  # nyquist needs to be at lest 2 x Bandwidth of interest
    low = lowcut / nyq
    high = highcut / nyq

    # design filter
    butter = signal.butter(order, [low, high], btype='band')
    return butter


def generate_CI_filterbanks(num_electrodes, fs):
    '''
        Generates filterbank for CI with [num_electrodes] electrodes.

        Args:
            num_electrodes: number of CI electrodes
            fs:sample frequency

        Returns:
            f: filterbank for each electrode
    '''
    filter_banks = []
    border_frequencies = find_border_frequencies(num_electrodes)
    for electrode in range(num_electrodes):
        filter_banks.append(
            butterworth_bandpass(fs, border_frequencies[electrode],
                                 border_frequencies[electrode + 1]))
    return filter_banks


def play_back_sound(sound_array, fs):
    # normalise the data to between -1 and 1. Else it will be very noisy when played
    data_array = sound_array / np.max(np.abs(sound_array))
    print('Starting playback...')
    sd.play(data_array, fs)
    print('...stopping playback.')

def butter_bandpass_filter(data, b, a):
    y = signal.lfilter(b, a, data)
    return y

def filter_wav_file(save=False):
    '''
        Filters a given audiosignal with the given filterbanks.

        Args:
            audio_file_path: path to file, (str)

        Returns:
            f: filtered signal
    '''

    audio_file_path = '../data/exercise_7/sorekara.wav'
    with open(audio_file_path, 'rb') as audiofile:
        sample_rate, data = wavfile.read(audiofile)
        data_array = np.array(data)
        print("Sample rate is {} Hz. Data length is {}.".format(sample_rate, len(data)))

    # Play back the audiofile
    play_back_sound(data_array, sample_rate)

    # Plot the time signal of the initial audio file
    set_plot_params([10,6], fontsize=14, spines=True)
    timearray = np.arange(0, data.shape[0], 1)/sample_rate
    plt.plot(timearray, data, linewidth=1)
    plt.xlim(0, 2.5)
    plt.xticks(np.arange(0, 2.50001, step=0.5))
    plt.ylim(-1550, 1550)
    plt.yticks(np.arange(-1500, 1500.00001, step=500))
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid()

    if save:
        plt.savefig('../latex/tex_7/imgs/sorekara.eps', format='eps')

    filter_banks = generate_CI_filterbanks(12, sample_rate)
    filtered = []
    for f in filter_banks:
        filtered_signal = butter_bandpass_filter(data_array, *f)
        filtered.append(filtered_signal)

    return filtered, sample_rate
