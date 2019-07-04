from Neuroprosthetics.filter_banks import *
from Neuroprosthetics.plot_utils import set_plot_params
from matplotlib import pyplot as plt
from scipy.signal import freqz



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
        plt.plot(center_freq,  'o-', label='{} electrodes'.format(electrodes))

    plt.legend()
    plt.ylabel('Center Frequency (Hz)')
    plt.xlabel('Electrode Number')
    if save:
        path = '../latex/tex_7/imgs/'
        plt.savefig(path + 'center_frequencies_' + name + '.eps',
                    format='eps')
    plt.show()


if __name__=='__main__':
    # # Plot for all CIs - as overview
    # electrode_counts = [3, 6, 12, 22]
    # plot_center_frequencies(electrode_counts, name='all', save=True)

    # # Plot for 22 electrode CI only
    # electrode_count = [22]
    # plot_center_frequencies(electrode_count, name='22', save=True)

    # electrode_counts = [3, 6, 12, 22]
    # fs = 48e3  # sample frequency
    # for ci in electrode_counts:
    #     filter_banks = generate_CI_filterbanks(ci, fs)
    #     plot_filter_banks(fs, filter_banks, ci)

    filter_wav_file()



