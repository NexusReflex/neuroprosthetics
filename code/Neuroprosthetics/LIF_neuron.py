import numpy as np
import matplotlib.pyplot as plt

def rectifiedSignalGenerator(amplitude, stepsize, frequency, duration):
    samples = duration/stepsize

    output_time_array = np.linspace(0, duration, samples+1)

    w = 2 * np.pi * frequency
    signal_current = np.abs(amplitude * np.sin(w * output_time_array))

    plotRectSignal(str(amplitude) + 'muA_rectSign.eps', output_time_array, signal_current)
    return signal_current


def lif(i_input_amplitude, i_const=True, freq=50):
    v_n_list = []
    times = []
    C_m = 0.000001
    g_leak = 0.0001
    v_rest = -0.06
    v_thr = -0.02
    v_spike = 0.02

    duration = 0.05
    stepsize = 0.000025

    v_n = v_rest  # initial cell membrane voltage == resting voltage
    if i_const == False:
        i_input = rectifiedSignalGenerator(i_input_amplitude, stepsize, freq, duration)
    else:
        i_input = i_input_amplitude

    index = 0
    for t_n in np.arange(0, duration, stepsize):
        v_n_list.append(v_n)
        if v_n < v_thr and i_const == True:
            v_n_plus_1 = v_n + (stepsize/C_m) * (-g_leak*(v_n - v_rest) + i_input)
        elif v_n < v_thr and i_const == False:
            v_n_plus_1 = v_n + (stepsize/C_m) * (-g_leak*(v_n - v_rest) + i_input[index])
        elif v_thr <= v_n < v_spike:
            v_n_plus_1 = v_spike
        elif v_spike <= v_n:
            v_n_plus_1 = v_rest

        index += 1
        times.append(t_n)
        v_n = v_n_plus_1

    return v_n_list, times


def plotRectSignal(filename, timearray, signalarray, fontsize=13, save=False):
    times = [time * 1000 for time in timearray]  # s to ms
    signals = [signal * 1000000 for signal in signalarray]  # to dislay as muA

    plt.rcParams['figure.figsize'] = [8, 4]  # *\textwidth in LaTeX
    plt.rcParams['axes.spines.right'] = True
    plt.rcParams['axes.spines.top'] = True

    ax = plt.axes()
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')
    ax.tick_params(axis='both', which='major', pad=10, labelsize=fontsize,
                   direction='in')  # set tick properties

    signal_max = max(signals)
    plt.xlim(0, 50)  # set axis limits
    plt.ylim(0, signal_max)
    plt.xticks(np.arange(0, 50.00001, step=5))  # set tick ranges
    if signal_max < 15:
        plt.yticks(np.arange(0, max(signals) + .00001, step=2))
    else:
        plt.yticks(np.arange(0, max(signals) + .00001, step=5))

    plt.plot(times, signals, linewidth=1)

    plt.xlabel('t (ms)', fontsize=fontsize)
    plt.ylabel(u'I (\u03bcA)', fontsize=fontsize)
    plt.tight_layout()

    if save:
        path = '../latex/tex_3/imgs/'
        plt.savefig(path + filename, format='eps')

    plt.show()


def plotLif(filename, voltages_list, timesteps, fontsize=25, save=False):
    times = [time * 1000 for time in timesteps]  # s to ms
    voltages = [voltage * 1000 for voltage in voltages_list]  # V to mV

    plt.rcParams['figure.figsize'] = [10, 10]  # bit more than 0.5*\textwidth in LaTeX
    plt.rcParams['axes.spines.right'] = True
    plt.rcParams['axes.spines.top'] = True

    ax = plt.axes()
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')
    ax.tick_params(axis='both', which='major', pad=10, labelsize=fontsize,
                   direction='in')  # set tick properties

    plt.xlim(0, 50)  # set axis limits
    plt.ylim(-60, 20)
    plt.xticks(np.arange(0, 50.00001, step=10))  # set tick ranges
    plt.yticks(np.arange(-60, 20.00001, step=10))

    plt.plot(times, voltages, linewidth=1.3)

    plt.xlabel('t (ms)', fontsize=fontsize)
    plt.ylabel('V (mV)', fontsize=fontsize)

    plt.tight_layout()

    if save:
        path = '../latex/tex_3/imgs/'
        plt.savefig(path + filename, format='eps')

    plt.show()
