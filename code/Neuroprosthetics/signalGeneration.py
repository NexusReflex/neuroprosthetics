import numpy as np
import matplotlib.pyplot as plt


def signalGenerator(amplitudesArray, frequenciesArray, offsetValue,
                    durationValue, sampleRateValue):
    """
        Generates Signal composed of overlying frequencies.
    """
    t = 1 / sampleRateValue
    output_time_array = np.arange(0, durationValue, t)
    summation = np.zeros((len(output_time_array), 1))
    index = 0

    for t in np.nditer(output_time_array.T):
        summation[index] = np.sum(np.multiply(amplitudesArray, np.sin(
            2 * np.pi * np.multiply(frequenciesArray, t))))
        index += 1

    output_signal_array = offsetValue + summation
    return output_signal_array, output_time_array


def plotSignal(x_data, y_data, xaxis_min, xaxis_max, yaxis_min, yaxis_max,
               x_ticks_step=0.01, y_ticks_step=2, fontsize=13, name='name'):
    """
        Plots the generated signal.
    """
    plt.style.use('seaborn-whitegrid')
    plt.rcParams['figure.figsize'] = [8, 4]
    ax = plt.axes()

    ax.tick_params(axis='both', which='major', pad=10, labelsize=fontsize)

    plt.xlim(xaxis_min, xaxis_max)
    plt.ylim(yaxis_min, yaxis_max)

    plt.plot(x_data, y_data, linewidth=0.7)

    plt.xticks(np.arange(xaxis_min, xaxis_max + 0.01, x_ticks_step))
    plt.yticks(np.arange(yaxis_min, yaxis_max + 1, y_ticks_step))

    plt.xlabel('Time (s)', fontsize=fontsize)
    plt.ylabel('Amplitude', fontsize=fontsize)
    plt.tight_layout()

    # uncommet following two lines to save plot
    #path = '../latex/tex_1/imgs/'
    #plt.savefig(path + name + '.eps', format='eps')

    plt.show()
    return 0


def plotFFT(fft_signal_vector, frequencies_vector, xlims, ylims, name, fontsize=13, save=False):
    """
        Plots the Single-Sided Amplitude Spectrum of the fft_signal_vector.
    """
    plt.style.use('seaborn-whitegrid')
    plt.rcParams['figure.figsize']= [8, 4]

    ax = plt.axes()
    ax.tick_params(axis='both', which='major', pad=10, labelsize=fontsize)
    plt.xticks(np.arange(0, xlims[1] + .01, step=1))

    plt.xlim(xlims[0], xlims[1])
    plt.ylim(ylims[0], ylims[1])
    plt.xlabel('Frequency (kHz)', fontsize=fontsize)
    plt.ylabel('Amplitude', fontsize=fontsize)
    plt.plot(frequencies_vector, fft_signal_vector, marker='o', clip_on=False,
             zorder=3)
    plt.tight_layout()

    if save:
        path = '../latex/tex_1/imgs/'
        plt.savefig(path + name + '.eps', format='eps')

    plt.show()


def calcSingleSidedAmplitudeSpectrum(input_signal_array, sampleRate):
    """
     Calculates a Single-Sided Amplitude Spectrum of the inputsignal.
     """
    N = len(input_signal_array)
    Y = np.fft.fft(input_signal_array, axis=0)[
        0:int(N / 2)] / N  # np.fft function
    Y[1:] = 2 * Y[1:]  # take single sided spectrum only
    fsig = np.abs(Y)  # get rid of imaginary part
    freq = sampleRate * np.arange((N / 2)) / N  # frequency vector
    freq /= 1000  # / 1000 for kHz)
    if sampleRate == 10000:
        plotFFT(fsig, freq, [freq[0], 5], [fsig.min(), fsig.max() + 0.2], '10kHz_samplefreq')
    elif sampleRate == 100000:
        plotFFT(fsig[:10000], freq[:10000], [freq[0], 10], [fsig.min(),
                                                             fsig.max() + 0.2], '100kHz_samplefreq')
    else:
        plotFFT(fsig, freq, [freq[0], 10], [fsig.min(), fsig.max() + 0.2], '20kHz_samplefreq')

