import matplotlib.pyplot as plt
import numpy as np
import code.Neuroprosthetics.hodgkinHuxley as hh
from .Neuroprosthetics.plot_utils import set_plot_params


def plotTandX(voltageRange, timeconstantsArraysList, xArrayList, ylim, temp, path='../latex/tex_4/imgs/',
              fontsize=13, save=True):

    for tc in timeconstantsArraysList:
        plt.plot(voltageRange, tc, linewidth=1)

    plt.xlim(voltageRange[0], voltageRange[-10])  # set axis limits
    plt.ylim(0, ylim)

    if ylim < 1:
        y_step = 0.1
    else:
        y_step = 1

    plt.xticks(np.arange(voltageRange[0], voltageRange[-1] + .00001,
                         step=50), fontsize=fontsize)  # set tick ranges
    plt.yticks(np.arange(0, ylim + .00001, step=y_step), fontsize=fontsize)

    plt.legend([r'$\tau_m$', r'$\tau_n$', r'$\tau_h$'], fontsize=fontsize)
    plt.xlabel('V (mV)', fontsize=fontsize)
    plt.ylabel('t (ms)', fontsize=fontsize)
    plt.grid()

    plt.tight_layout()

    if save:
        plt.savefig(path + 'timeConst_at_' + str(int(temp)) + '.eps', format='eps')

    plt.show()

    plt.xlim(voltageRange[0], voltageRange[-10])
    plt.ylim(0, 1)
    for x in xArrayList:
        plt.plot(voltageRange, x, linewidth=1)

    plt.xticks(np.arange(voltageRange[0], voltageRange[-1] + .00001,
                         step=50), fontsize=fontsize)  # set tick ranges
    plt.yticks(np.arange(0, 1.00001, step=0.2), fontsize=fontsize)  # adjust ticks

    plt.legend([r'$m_{\infty}$', r'$n_{\infty}$', r'$h_{\infty}$'],
               loc='center left', fontsize=fontsize)
    plt.xlabel('V (mV)', fontsize=fontsize)
    plt.ylabel('P', fontsize=fontsize)
    plt.grid()

    plt.tight_layout()

    if save:
        plt.savefig(path + 'x_at_' + str(int(temp)) + '.eps', format='eps')

    plt.show()


def plot_istim(t, istim, max_impulse, temp, path='../latex/tex_4/imgs/', fontsize=13, save=True):
    plt.xlim(t[0], t[-1])
    plt.ylim(0, max_impulse)
    plt.plot(t, istim, linewidth=1)

    plt.xticks(np.arange(t[0], t[-1] + .00001,
                         step=20), fontsize=fontsize)  # set tick ranges
    if max_impulse <= 10:
        plt.yticks(np.arange(0, max_impulse + .00001, step=1), fontsize=fontsize)  # adjust ticks
    else:
        plt.yticks(np.arange(0, 35.00001, step=5), fontsize=fontsize)  # adjust ticks

    plt.legend(["input current"],
               loc='upper right', fontsize=fontsize)
    plt.xlabel('t (ms)', fontsize=fontsize)
    plt.ylabel(r'$i \,(\mu A)$', fontsize=fontsize)
    plt.grid()

    plt.tight_layout()

    if save:
        plt.savefig(path + 'istim_at_' + str(int(temp)) + '.eps', format='eps')

    plt.show()


def plot_membrane_potential(t, v, temp, path='../latex/tex_4/imgs/', fontsize=13, save=True):
    v_max = max(v)
    plt.xlim(t[0], t[-1])
    plt.ylim(-20, v_max + 20)  # little buffer to the top
    plt.plot(t, v, linewidth=1)

    plt.xticks(np.arange(t[0], t[-1] + .00001,
                         step=20), fontsize=fontsize)  # set tick ranges
    plt.yticks(np.arange(-20, v_max + 20, step=20), fontsize=fontsize)  # adjust ticks

    plt.legend(["membrane potential"],
               loc='upper right', fontsize=fontsize)
    plt.xlabel('t (ms)', fontsize=fontsize)
    plt.ylabel(r'$V(t) \,(mV)$', fontsize=fontsize)
    plt.grid()

    plt.tight_layout()

    if save:
        plt.savefig(path + 'membrane_pot_at_' + str(int(temp)) + '.eps',
                    format='eps')

    plt.show()


def plot_gates(t_gates, gates, start_idx, end_idx, temp, path='../latex/tex_4/imgs/', fontsize=13, save=True):

    t_gates = t_gates[start_idx:end_idx]
    plt.xlim(t_gates[0], t_gates[-1])
    plt.ylim(0, 1)  # little buffer to the top

    gates = gates[start_idx:end_idx]
    gates_unzipped = [list(result_tuple) for result_tuple in zip(*gates)]

    for gate in gates_unzipped:
        plt.plot(t_gates, gate, linewidth=1)

    plt.xticks(np.arange(t_gates[0], t_gates[-1] + .00001,
                         step=20), fontsize=fontsize)  # set tick ranges
    plt.yticks(np.arange(0, 1.000001, step=0.2), fontsize=fontsize)  # adjust ticks

    plt.legend(['m', 'n', 'h'],
               loc='upper right', fontsize=fontsize)
    plt.xlabel('t (ms)', fontsize=fontsize)
    plt.ylabel('P(t)', fontsize=fontsize)
    plt.grid()

    plt.tight_layout()
    if save:
        plt.savefig(path + 'gates_at_' + str(int(temp)) + '_from' +str(start_idx) +'.eps', format='eps')

    plt.show()


def plot_ion_currents(t, i_ions_dict, temp, fontsize=13, path='../latex/tex_4/imgs/', save=True):
    plt.xlim(t[0], t[-1])
    plt.ylim(0, 1000)  # little buffer to the top

    for current in ['iNa', 'iK']:
        plt.plot(t, [i[current] for i in i_ions_dict], linewidth=1)


    plt.xticks(np.arange(t[0], t[-1] + .00001,
                         step=20), fontsize=fontsize)  # set tick ranges
    plt.yticks(np.arange(-1000.00001, 1000.00001, step=500), fontsize=fontsize)  # adjust ticks

    plt.legend([r'$i_{Na}$', r'$i_{K}$'],
               loc='upper right', fontsize=fontsize)
    plt.xlabel('t (ms)', fontsize=fontsize)
    plt.ylabel(r'i(t)$\,(\mu A)$', fontsize=fontsize)
    plt.grid()

    plt.tight_layout()
    if save:
        plt.savefig(path + 'ion_currents_at_' + str(int(temp)) + '.eps',
                    format='eps')

    plt.show()


def plot_current_phase(v, i_ions_dict, temp, fontsize=13, path='../latex/tex_4/imgs/', save=True):
    # add arrows to clarify circular direction of i in plot later
    for current in ['iNa', 'iK', 'iL']:
        plt.plot(v, [i[current] for i in i_ions_dict], linewidth=1)

    if temp == 6.3:
        plt.xlim(-50, 150)
        plt.ylim(-1000, 1000)  # little buffer to the top
        plt.xticks(np.arange(-50, 150 + .00001,
                             step=50), fontsize=fontsize)  # set tick ranges
        plt.yticks(
            np.arange(-1000.00001, 1000.00001, step=500), fontsize=fontsize)  # adjust ticks
    else:
        plt.xlim(-20, 80)
        plt.ylim(-800, 800)  # little buffer to the top
        plt.xticks( np.arange(-20, 80 + .00001, step=50), fontsize=fontsize)  # set tick ranges
        plt.yticks(
            np.arange(-800.00001, 800.00001, step=200), fontsize=fontsize)  # adjust ticks

    plt.legend([r'$i_{Na}$', r'$i_{K}$', r'$i_{L}$'],
               loc='upper left', fontsize=fontsize)
    plt.xlabel('V (mV)', fontsize=fontsize)
    plt.ylabel(r'i(V)$\,(\mu A)$', fontsize=fontsize)
    plt.grid()

    plt.tight_layout()

    if save:
        plt.savefig(path + 'current_phases_at_' + str(int(temp)) + '.eps',
                    format='eps')

    plt.show()


if __name__ == '__main__':
    # 1. Time constants and steady state values
    # delta_v muss klein genug gewählt werden, um den
    # "perfekten" Graph zu erzeugen
    # -> es existieren nullstellen für a_m und a_n
    voltages = np.arange(-100, 101, 0.1)
    temperatures = [6.3, 28]
    ylim = [9, 0.8]

    # 2.1 and 2.2
    impulses_1 = [1, 2, 3, 4, 5]
    impulses_2 = [2, 4, 8, 16, 32]
    impulses_list = [impulses_1, impulses_2]

    set_plot_params()

    for index, t in enumerate(temperatures):
        timeConstants, steadyStateGates = hh.timeConstantsAndSteadyStateValues(
            voltages, t)

        plotTandX(voltages, timeConstants, steadyStateGates, ylim[index], t)

        v_membrane, gating_vars, ionic_currents, timevector, i_stim = hh.hh_model(
            0, 100, 0.01, t, impulses_list[index])

        plot_istim(timevector, i_stim, max(impulses_list[index]), t, save=False)
        plot_membrane_potential(timevector, v_membrane, t, save=False)
        plot_gates(timevector, gating_vars, 0, 10001, t, save=False)
        plot_ion_currents(timevector, ionic_currents, t, save=False)
        plot_current_phase(v_membrane, ionic_currents, t, save=False)

        plot_gates(timevector, gating_vars, 5300, 7500, t,
                   save=False)


