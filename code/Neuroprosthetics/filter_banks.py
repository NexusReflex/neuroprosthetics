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


def generate_CI_filterbanks(num_electrodes, fs, order=2):
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
                                 border_frequencies[electrode + 1], order=order))
    return filter_banks


def play_back_sound(sound_array, fs):
    # normalise the data to between -1 and 1. Else it will be very noisy when played
    data_array = sound_array / np.max(np.abs(sound_array))
    print('Starting playback...')
    sd.play(data_array, fs)
    print('...stopping playback.')


def play_back_generated_audios(path_for_filtered_audiofiles, sound_name):
    while True:
        print(
            "Enter a number between 0-11 corresponding to the .wav audio file you want to listen to.\n Enter :wq to exit:\n")
        var = input()
        if var == ':wq':
            break
        elif var == '':
            continue
        elif 0 <= int(var) <= 11:
            print("You entered: " + var)
            filepath = path_for_filtered_audiofiles + '/sound_{}_{}.wav'.format(
                sound_name, var)
            with open(filepath, 'rb') as audiofile:
                fs, data = wavfile.read(audiofile)
                data_array = np.array(data)
            play_back_sound(data_array, fs)
        else:
            print('No file with name /sound_{}.wav exists. Try again.'.format(
                var))
            continue


def butter_bandpass_filter(data, b, a):
    y = signal.lfilter(b, a, data)
    return y


def filter_wav_file(audio_file_name, num_electrodes, order=2, save=False, play_back=True, show_plot=True):
    '''
        Filters a given audiosignal with the given filterbanks.

        Args:
            audio_file_path: path to file, (str)

        Returns:
            f: filtered signal
    '''

    audio_file_path = '../data/exercise_7/{}.wav'.format(audio_file_name)

    with open(audio_file_path, 'rb') as audiofile:
        sample_rate, data = wavfile.read(audiofile)
        data = np.array(data)
        print("Sample rate is {} Hz. Data length is {}.".format(sample_rate,
                                                                len(data)))

    # Play back the audiofile
    if play_back:
        play_back_sound(data, sample_rate)

    # Plot the time signal of the initial audio file
    set_plot_params([10, 6], fontsize=14, spines=True)
    timearray = np.arange(0, data.shape[0], 1) / sample_rate
    plt.figure()
    plt.plot(timearray, data)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid()
    if save:
        plt.savefig('../latex/tex_7/imgs/{}_fft.eps'.format(audio_file_name),
                    format='eps')
    if show_plot:
        plt.show()

    # Plot the FFT of the initial audio file
    set_plot_params([10, 6], fontsize=14, spines=True)
    n = data.size
    fft = np.abs(np.fft.rfft(data) / n)
    freq = np.fft.rfftfreq(n, 1 / sample_rate)
    fft[1:] = fft[1:] * 2
    fft /= np.max(fft)
    plt.figure()
    plt.plot(freq, fft)
    plt.semilogx()
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Normalized Amplitude')

    if save:
        plt.savefig('../latex/tex_7/imgs/{}_fft.eps'.format(audio_file_name), format='eps')
    if show_plot:
        plt.show()

    # Create the filter-banks and filter the signal
    filter_banks = generate_CI_filterbanks(num_electrodes, sample_rate, order=order)
    filtered = []
    for f in filter_banks:
        filtered_signal = butter_bandpass_filter(data, *f)
        filtered.append(filtered_signal)

    return filtered, sample_rate


def plot_fft(signal, Fs, title=None, newFig=True, labels=True, save=False, name=None, normalize=True):
    n = signal.size
    spectrum = np.abs(np.fft.rfft(signal) / n)
    freq = np.fft.rfftfreq(n, 1 / Fs)
    spectrum[1:] = spectrum[1:] * 2
    indices = freq > 100

    if newFig:
        plt.figure()

    if normalize:
        spectrum /= np.max(spectrum)
    else:
        plt.ylim(0, 50)
        plt.yticks(np.arange(0, 50.00001, step=10))
    plt.semilogx()
    plt.plot(freq[indices], spectrum[indices])
    if labels:
        if not normalize:
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Magnitude')
        else:
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Norm. Magnitude')
    plt.title(title)
    if save:
        plt.savefig('../latex/tex_7/imgs/filtered_{}_fft.eps'.format(name),
                    format='eps')


def sum_channels(audio_name, num_electrodes, play_back=False):
    filtered, rate = filter_wav_file(audio_name, num_electrodes,
                                     play_back=play_back)
    # sum channels -> play back
    summed = np.sum(filtered, axis=0)
    return summed, rate
