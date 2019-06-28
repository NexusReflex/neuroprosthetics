from Neuroprosthetics.multicompartment_model import hh_multi_compartment, calc_input_current
from Neuroprosthetics.plot_utils import set_plot_params
import matplotlib.pyplot as plt
import numpy as np


def plot_model(v, N, stimulated_compartments, path='../latex/tex_5/imgs/',
               save=False):
    f = plt.figure()
    ax = f.gca()
    im = ax.imshow(v.T,
                   aspect='auto',
                   origin='lower',
                   cmap='jet',
                   interpolation='none',
                   norm=None,
                   extent=(0, 100, 0, N))
    ax.set_xlabel('t (ms)')
    ax.set_ylabel('Compartment Number')

    cb = f.colorbar(im)
    cb.set_label("V (mV)")

    f.tight_layout()

    if save:
        plt.savefig(path + 'compartment_model' + ''.join(
            str(x) for x in stimulated_compartments) + '.eps',
                    format='eps')
    plt.show()


def create_multi_compartment_model(stimulated_compartments, save_plots=False):
    N = 100
    V_0 = np.zeros(N)
    dt = 25 * 10 ** -3  # ms
    duration = 100  # ms

    def i_stim(t):
        return calc_input_current(t, N, indices=stimulated_compartments)

    v, _ = hh_multi_compartment(duration, dt, i_stim, N, V_0=V_0)
    plot_model(v, N, stimulated_compartments, save=save_plots)


def plot_different_Ra_Cm_settings(stim_comp=[0],path='../latex/tex_5/imgs/', save=False):
    N = 100
    V_0 = np.zeros(N)
    dt = 25 * 10 ** -3  # ms
    duration = 100  # ms

    R_a = [0.5, 1, 5]
    C_m = [0.5, 1, 1.5]

    def i_stim(t):
        return calc_input_current(t, N, indices=stim_comp)

    f, axes = plt.subplots(len(C_m), len(R_a))
    for i in range(len(C_m)):
        for j in range(len(R_a)):
            v, _ = hh_multi_compartment(duration, dt, i_stim, N, V_0=V_0,
                                     R_a=R_a[j], Cm=C_m[i])
            im = axes[i, j].imshow(v.T,
                                   cmap='jet',
                                   aspect='auto',
                                   origin='lower',
                                   interpolation='none',
                                   extent=(0, 100, 0, N))
            axes[i, j].grid()
            axes[i, j].get_xaxis().set_ticks([])
            axes[i, j].get_yaxis().set_ticks([])

            if i == len(C_m) - 1:
                axes[i, j].set_xlabel(r'$R_a = {}$'.format(R_a[j]))
            if j == 0:
                axes[i, j].set_ylabel(r'$C_m = {}$'.format(C_m[i]))

            print((len(C_m) * i + j + 1) / (len(R_a) * len(C_m)))

    cb = f.colorbar(im)
    cb.set_label("V (mV)")

    f.tight_layout()

    if save:
        plt.savefig(path + 'different_settings_Ra_Cm' + '.eps',
                    format='eps')
    plt.show()


if __name__ == '__main__':

    set_plot_params([10, 5], fontsize=13)

    stimulated_compartments_list = [[0], [20, 80]]

    for stimulated_compartments in stimulated_compartments_list:
        create_multi_compartment_model(stimulated_compartments)

    plot_different_Ra_Cm_settings()
