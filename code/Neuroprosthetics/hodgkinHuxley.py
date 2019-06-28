import numpy as np


def get_k(T):
    return 3 ** (0.1 * (T - 6.3))


def timeConstantsAndSteadyStateValues(voltageRange, tempValue):
    k = get_k(tempValue)
    T_m = []
    T_n = []
    T_h = []
    m_inf_list = []
    n_inf_list = []
    h_inf_list = []

    for v in voltageRange:

        tau_m, tau_n, tau_h = tau(v, k)
        T_m.append(tau_m)
        T_n.append(tau_n)
        T_h.append(tau_h)

        m, n, h = gates_inf(v)
        m_inf_list.append(m)
        n_inf_list.append(n)
        h_inf_list.append(h)
    return [T_m, T_n, T_h], [m_inf_list, n_inf_list, h_inf_list]


def input_current(t, amplitudes):
    duration = int(np.floor(t / 15))
    if np.floor(t / 5) % 3 == 0:
        if duration < len(amplitudes):
            return amplitudes[duration]
    return 0


def tau(v, k):
    a_m, a_n, a_h = alphas(v)
    b_m, b_n, b_h = betas(v)
    tau_m = (k * (a_m + b_m)) ** (-1)
    tau_n = (k * (a_n + b_n)) ** (-1)
    tau_h = (k * (a_h + b_h)) ** (-1)
    return tau_m, tau_n, tau_h


def alphas(v):
    a_m = (2.5 - (0.1 * v)) / (np.exp(2.5 - (0.1 * v)) - 1)
    a_n = (0.1 - 0.01 * v) / (np.exp(1 - (0.1 * v)) - 1)
    a_h = 0.07 * np.exp(-v / 20)
    return a_m, a_n, a_h


def betas(v):
    b_m = 4 * np.exp(-v / 18)
    b_n = 0.125 * np.exp(-v / 80)
    b_h = 1 / (np.exp(3 - (0.1 * v)) + 1)
    return b_m, b_n, b_h


def gates_inf(vn):
    a_m, a_n, a_h = alphas(vn)
    b_m, b_n, b_h = betas(vn)
    m_inf = (a_m / (a_m + b_m))
    n_inf = (a_n / (a_n + b_n))
    h_inf = (a_h / (a_h + b_h))
    return m_inf, n_inf, h_inf


def hh_expoEuler(dt, old_gates, voltage, k):
    new_gates = [0, 0, 0]
    a_x = list(alphas(voltage))
    b_x = list(betas(voltage))
    for i, gate in enumerate(old_gates):
        A = -(a_x[i] + b_x[i]) * k
        B = a_x[i] * k
        new_gates[i] = gate * np.exp(A * dt) + (B / A) * (np.exp(A * dt) - 1)
    return new_gates


def hh_current(dt, V, last_gates, k, currents_dict=None):
    gNa = 120
    gK = 36
    gL = 0.3
    vNa = 115
    vK = -12
    vL = 10.6

    new_gates = hh_expoEuler(dt, last_gates, V, k)
    iNa = gNa * (new_gates[0] ** 3) * new_gates[2] * (V - vNa)
    iK = gK * (new_gates[1] ** 4) * (V - vK)
    iL = gL * (V - vL)

    if currents_dict is not None:
        currents_dict['iNa'] = iNa
        currents_dict['iK'] = iK
        currents_dict['iL'] = iL

    sum_i_ion = iNa + iK + iL
    return sum_i_ion, new_gates


def forwardEulerVoltage(dvdt, v_n, t_n, dt):
    return v_n + dvdt(v_n, t_n) * dt


def hh_model(starttime, endtime, dt, temp, impulses, v_n=0):
    k = get_k(temp)
    c_m = 1
    timevector = np.arange(starttime, endtime + dt, dt)
    m_init, n_init, h_init = gates_inf(v_n)
    init_gates = [m_init, n_init, h_init]
    v_membrane = []
    i_stim_list = []
    last_gates = init_gates
    gates_list = []
    ion_currents = list()

    for index, t in enumerate(timevector):
        currents_dict = dict()
        gates_list.append(last_gates)
        v_membrane.append(v_n)
        i_stim = input_current(t, impulses)
        i_ion, gates_n = hh_current(dt, v_n, last_gates, k, currents_dict=currents_dict)

        i_total = -i_ion + i_stim
        dVdt = lambda V, i: 1. / c_m * i
        v_n_1 = forwardEulerVoltage(dVdt, v_n, i_total, dt)
        v_n = v_n_1

        i_stim_list.append(i_stim)
        last_gates = gates_n
        ion_currents.append(currents_dict)

    return v_membrane, gates_list, ion_currents, timevector, i_stim_list


