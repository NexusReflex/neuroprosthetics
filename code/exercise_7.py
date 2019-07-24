from Neuroprosthetics.filter_banks import *
from Neuroprosthetics.plot_utils import set_plot_params
from matplotlib import pyplot as plt
from scipy.signal import freqz, spectrogram
from scipy.io.wavfile import write
import os


def plot_filter_banks(f_s, filter_banks, num_electrodes, save=False):
    set_plot_params([10, 6], fontsize=14)
    plt.semilogx()
    for i, f in enumerate(filter_banks):
        w,h = freqz(*f, worN=6000)
        freq = (f_s * 0.5 / np.pi) * w
        h = 20 * np.log10(np.abs(h))
        plt.plot(freq, h)

    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (dB)")
    plt.yticks([0, -3, -20, -40, -60, -80])
    plt.ylim(-80, 6)
    plt.grid()
    if save:
        path = '../latex/tex_7/imgs/'
        plt.savefig(path + 'ci_with_' + str(num_electrodes) + '_electrodes.eps',
                    format='eps')
    plt.show()


def plot_center_frequencies(num_electrodes_per_CI, save=False, name=None):
    set_plot_params([10, 5], fontsize=14)
    for electrodes in num_electrodes_per_CI:
        center_freq = find_border_frequencies(electrodes)
        print('for ' + str(electrodes) + ": " + str(center_freq) )
        plt.rcParams['legend.fontsize'] = 'large'
        plt.plot(center_freq,  '*-', label='{} electrodes'.format(electrodes))
        plt.legend()

    plt.grid()
    plt.ylabel('Center Frequency (Hz)')
    plt.xlabel('Electrode Number')
    if save:
        path = '../latex/tex_7/imgs/'
        plt.savefig(path + 'center_frequencies_' + name + '.eps',
                    format='eps')
    plt.show()

def plot_wav_results(audio_name, filtered_path, num_electrodes=12, saveImg=False, saveAudio=False):
    '''
    Applies the band-pass filter bank of a 12 electrode CI to the input audio signal.

    :param audio_name: name of audiofile (str)
    :param filtered_path: path to filtered subfiles (str)
    :param num_electrodes: number of electrodes of CI
    :param saveImg: (bool)
    :param saveAudio: (bool)
    :return: list of filtered signals, sample rate
    '''
    filtered, Fs = filter_wav_file(audio_name, num_electrodes, save=True)

    set_plot_params([13, 8], fontsize=11)

    plt.figure()
    plt.subplots_adjust(hspace=0.7, wspace=0.5)
    for i in range(0, 12):
        filtered_signal = filtered[i]
        if saveAudio:
            filename = '{}/sound_{}_{}.wav'.format(filtered_path, audio_name, i)
            if not os.path.exists(filename):
                write(filename, Fs, filtered_signal)
            else:
                print('File at {} already exists.'.format(filename))

        set_plot_params([10,8], fontsize=11, spines=True)
        plt.subplot(4, 3, i+1)
        timearray = np.arange(0, filtered_signal.shape[0], 1) / Fs
        # set axis limits
        plt.xlim(0, 2.5)
        plt.xticks(np.arange(0, 2.50001, step=1), fontsize=11)
        plt.ylim(-650, 650)
        plt.yticks(np.arange(-600, 600.00001, step=300), fontsize=11)
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.title('Filter {}'.format(i+1))
        plt.grid()
        plt.plot(timearray, filtered_signal, linewidth=0.4)

    if saveImg:
        plt.savefig('../latex/tex_7/imgs/wav_results.eps', format='eps')
    plt.show()

    #FFT plots
    set_plot_params([13, 8], fontsize=11)
    plt.figure()
    plt.subplots_adjust(hspace=0.7, wspace=0.5)
    for i in range(0, 12):
        filtered_signal = filtered[i]
        set_plot_params([10, 8], fontsize=11, spines=True)
        plt.subplot(4, 3, i + 1)
        plot_fft(filtered_signal, Fs, 'Filter {}'.format(i + 1), newFig=False, labels=True, normalize=False)

    if saveImg:
        plt.savefig('../latex/tex_7/imgs/wav_results_fft.eps', format='eps')
    plt.show()


def plot_summed_channels(audio_name, num_electrodes=12, saveImg=False):

    summed, rate = sum_channels(audio_name, num_electrodes=12, play_back=False)
    print(
        "Play back summed signal? (y/n)")
    var = input()
    if var == 'y':
        play_back_sound(summed, rate)
    elif var == 'n':
        print('continuing...')

    # Plot the time signal of the initial audio file
    plt.figure()
    set_plot_params([10, 6], fontsize=14, spines=True)
    timearray = np.arange(0, summed.shape[0], 1) / rate
    plt.plot(timearray, summed, linewidth=1)
    plt.xlim(0, 2.5)
    plt.xticks(np.arange(0, 2.50001, step=0.5))
    plt.ylim(-1550, 1550)
    plt.yticks(np.arange(-1500, 1500.00001, step=500))
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid()

    if saveImg:
        plt.savefig('../latex/tex_7/imgs/summed_{}_CI.eps'.format(num_electrodes), format='eps')
    plt.show()


def plot_spectogram(signal, fs, f_max=10e3, title=None, time_window=10e-3, overlap=5e-3, name=None, save=False, exercise_num=7):
    f, t, Sxx = spectrogram(signal, fs, nperseg=int(time_window * fs),
                            noverlap=int(overlap * fs),
                            return_onesided=True,
                            mode='magnitude')
    indices = f < f_max
    plt.figure()
    plt.pcolormesh(t, f[indices], Sxx[indices, :], cmap='nipy_spectral')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [s]')
    if title is not None:
        plt.title(title)

    if save:
        plt.savefig(
            '../latex/tex_{}/imgs/spectogram_{}_CI.eps'.format(exercise_num, name),
            format='eps')


if __name__=='__main__':
    saveAudio = False
    saveImg = False
    # Plot for all CIs as overview
    CI_all = [3, 6, 12, 22]
    # # Filter an audio signal and plot the results (time-signal)
    path_for_filtered_audiofiles = '../data/exercise_7'
    original_audiofile_name = 'sorekara'

    # plot_center_frequencies(CI_all, name='all', save=saveImg)
    #
    # # Plot for 22 electrode CI only
    # plot_center_frequencies([CI_all[3]], name='22', save=saveImg)
    #
    # # Plot filter-banks for all CI types
    # fs = 48e3  # sample frequency
    # for ci_type in CI_all:
    #     filter_banks = generate_CI_filterbanks(ci_type, fs)
    #     plot_filter_banks(fs, filter_banks, ci_type, save=saveImg)


    plot_wav_results(original_audiofile_name, path_for_filtered_audiofiles, saveAudio=saveAudio, saveImg=saveImg)

    # Play back prompted audio files
    play_back_generated_audios(path_for_filtered_audiofiles, original_audiofile_name)

    # Plot summed channels of a 12 electrode CI
    plot_summed_channels(original_audiofile_name, saveImg=saveImg)

    # Plot spectra and spectrograms for all CI types
    for i, ci_type in enumerate(CI_all):
        summed, fs = sum_channels(original_audiofile_name, ci_type, play_back=False)
        if saveAudio:
            filename = '{}/sound_filtered_{}_{}.wav'.format(path_for_filtered_audiofiles, original_audiofile_name, ci_type)
            if not os.path.exists(filename):
                write(filename, fs, summed)
            else:
                print('File at {} already exists.'.format(filename))

        set_plot_params([10, 8], fontsize=20, spines=True)
        plot_fft(summed, fs, save=saveImg, name=ci_type)
        plot_spectogram(summed, fs, 10e3, name=ci_type, save=saveImg)

    plt.show()



