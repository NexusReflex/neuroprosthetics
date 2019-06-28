import numpy as np
import matplotlib.pyplot as plt
from Neuroprosthetics.potential_fields import calculate_point_source_potential_field, calculate_external_potential
from Neuroprosthetics.plot_utils import set_plot_params
from Neuroprosthetics.current_with_pulse import mono_phasic_current_pulse, bi_phasic_current_pulse
from Neuroprosthetics.multicompartment_model import hh_multi_compartment


def plot_potential_field(center, size, distance, rho, current, save=False):
    path = '../latex/tex_6/imgs/'
    potential_field = calculate_point_source_potential_field(center, size, rho,
                                                             current,
                                                             distance)

    fig = plt.figure()
    ax = fig.gca()
    im = ax.imshow(potential_field, origin='lower', aspect='auto',
                   cmap='rainbow')
    ax.set_xlabel(r'x $(\mu m)$')
    ax.set_ylabel(r'y $(\mu m)$')

    cb = fig.colorbar(im)
    cb.set_label("V (V)")

    plt.xlim(0, 50)
    plt.ylim(0, 50)
    plt.xticks(np.arange(0, 50.00001, step=10))  # set tick ranges
    plt.yticks(np.arange(0, 50.00001, step=5))
    fig.tight_layout()

    if save:
        plt.savefig(path + 'potentialfield' + '.eps',
                    format='eps')
    plt.show()


def plot_external_potential(rho, currents, save=False):
    path = '../latex/tex_6/imgs/'
    counter = 0
    step = 0.5
    for i_val in currents:
        if i_val > 0:
            plt.xlim(0, 50)
            plt.ylim(8, 24)
            plt.xticks(np.arange(0, 50.00001, step=10))  # set tick ranges
            plt.yticks(np.arange(8, 24.00001, step=2))
        else:
            plt.xlim(0, 50)
            plt.ylim(-24, -8)
            plt.xticks(np.arange(0, 50.00001, step=10))  # set tick ranges
            plt.yticks(np.arange(-24, -7.99999, step=2))

        external_potential, e_field, activation, x_position = calculate_external_potential(
            rho,
            i_val, resolution=step*1e-6)

        x_position *= 1e6
        plt.plot(x_position, external_potential)
        plt.xlabel(r'x $(\mu m)$')
        plt.ylabel('V (V)')
        plt.grid()
        plt.tight_layout()
        if save:
            plt.savefig(path + 'external_potential_' + str(counter) + '.eps',
                        format='eps')
        plt.show()

        plt.xlim(0, 50)
        plt.ylim(-2e6, 2e6)
        plt.xticks(np.arange(0, 50.00001, step=10))  # set tick ranges
        plt.yticks(np.arange(-2e6, 2.00001e6, step=0.5e6))

        plt.plot(x_position, e_field/(step**2*1e-6)) # account for resolution of V/0.5e-6m -> back to v/m
        plt.ticklabel_format(axis='y', style='sci', scilimits=(6, 6))
        plt.xlabel(r'x $(\mu m)$')
        plt.ylabel('E (V/m)')
        plt.grid()
        plt.tight_layout()
        if save:
            plt.savefig(path + 'e_field_' + str(counter) + '.eps',
                        format='eps')
        plt.show()

        if i_val > 0:
            plt.xlim(0, 50)
            plt.ylim(-10e11, 2e11)
            plt.xticks(np.arange(0, 50.00001, step=10))  # set tick ranges
            plt.yticks(np.arange(-10e11, 2.000001e11, step=2e11))
        else:
            plt.xlim(0, 50)
            plt.ylim(-2e11, 10e11)
            plt.xticks(np.arange(0, 50.00001, step=10))  # set tick ranges
            plt.yticks(np.arange(-2e11, 10.00001e11, step=2e11))

        plt.plot(x_position, activation/((step**2*1e-6)**2))
        plt.ticklabel_format(axis='y', style='sci',scilimits=(11,11))
        plt.xlabel(r'x $(\mu m)$')
        plt.ylabel(r'A $(V/m^2)$')
        plt.grid()
        plt.tight_layout()
        if save:
            plt.savefig(path + 'activation_' + str(counter) + '.eps',
                        format='eps')
        plt.show()
        counter += 1


def plot_neuron_model(pulse_amplitude, rho, current_function, end_time, l_compartment=0.5e-4, l_axon=50e-6, name=None, save=False):
    def get_external_potential(t):
        potential_field, _, activation, x_pos = calculate_external_potential(rho,
                                                                    current_function(
                                                                        t,
                                                                        pulse_amplitude), resolution=l_axon/100)
        return potential_field, activation, x_pos

    membrane_voltage, time_array = hh_multi_compartment(end_time, 0.001, N=101,
                                                        v_e=lambda t: get_external_potential(t)[0],
                                                        rho_axon=0.01,
                                                        r_axon=1.5e-4,
                                                        T=6.3,
                                                        d_l=l_compartment)

    fig = plt.figure()
    ax = fig.gca()
    plt.xlim(0, 30)
    plt.ylim(0, 100)
    plt.xticks(np.arange(0, 30.00001, step=5))  # set tick ranges
    plt.yticks(np.arange(0, 100.00001, step=20))

    l_compartment*=1e-2 # from cm-4 to m^-6
    _, _, x_position = get_external_potential(0)
    im = ax.imshow(membrane_voltage.T,
                   aspect='auto',
                   cmap='jet',
                   origin='lower',
                   interpolation='none',
                   extent=(time_array[0], time_array[-1], x_position[0]/l_compartment,
                            x_position[-1]/l_compartment))
    ax.set_xlabel('Time [ms]')
    ax.set_ylabel('Compartment Number')
    cb = fig.colorbar(im)
    cb.set_label('Potential [mV]')
    if save:
        path = '../latex/tex_6/imgs/'
        plt.savefig(path + 'model_' + name + '.eps',
                    format='eps')
    plt.show()


if __name__ == '__main__':
    slice_size = [50e-6, 50e-6]  # mu*m x,y
    center_point = [25e-6, 25e-6]
    distance = 10e-6  # mu*m
    rho_medium = 300e-2  # Ohm*m
    i = 1e-3  # mA
    i_2 = [1e-3, -1e-3]
    
    set_plot_params(size=[10, 8], fontsize=15, ticksize=5, tickwidth=2)
    plot_potential_field(center_point, slice_size, distance, rho_medium, i)

    set_plot_params(fontsize=13, ticksize=3.5, tickwidth=0.8)
    plot_external_potential(rho_medium, i_2, save=False)

    set_plot_params(size=[10, 5], fontsize=13, ticksize=3.5, tickwidth=0.8)
    plot_neuron_model(-.25, rho_medium, mono_phasic_current_pulse, 30,
                      name='monophasic_m025', save=False)
    plot_neuron_model(-1, rho_medium, mono_phasic_current_pulse, 30,
                      name='monophasic_m1', save=False)
    plot_neuron_model(0.5, rho_medium, bi_phasic_current_pulse, 30,
                      name='biphasic_05', save=False)
    plot_neuron_model(2, rho_medium, bi_phasic_current_pulse, 30,
                      name='biphasic_2', save=False)
    plot_neuron_model(.25, rho_medium, mono_phasic_current_pulse, 30,
                      name='monophasic_025', save=False)
    plot_neuron_model(5, rho_medium, mono_phasic_current_pulse, 30,
                      name='monophasic_5', save=False)