import numpy as np
from .hodgkinHuxley import hh_current, gates_inf, get_k


def create_connection_matrix(n):
    c = -2 * np.eye(n)
    c += np.eye(n, k=1)
    c += np.eye(n, k=-1)
    c[0, 0] += 1
    c[-1, -1] += 1
    return c


def calc_input_current(t, N, amplitude=10, duration=5, indices=None):
    if indices is None:
        indices = [0]
    i = np.zeros(N)
    if t < duration:
        i[np.array(indices)] = 1
    return amplitude * i


def hh_multi_compartment(t_stop, dt, i_external=None, N=100, t_start=0, V_0=None,
                         T=6.3, R_a=None, Cm=None, v_e=None, rho_axon=0.1, r_axon=2e-4, d_l=1e-4):

    k = get_k(T)
    timearray = np.arange(t_start, t_stop, dt)

    C = create_connection_matrix(N)
    vector_dim = C.shape[0]

    if V_0 is None:
        V_0 = np.zeros(vector_dim)

    gates_vector = np.array([gates_inf(v_i) for v_i in V_0])
    currents = list()
    V = list()

    if R_a is None:
        R_a = rho_axon * d_l / (np.pi * r_axon ** 2)

    if Cm is None:
        Cm = 1

    V_n = V_0
    i_ion = np.zeros(vector_dim)

    for i, tn in enumerate(timearray):
        currents_dict = dict()
        if i_external is not None:
            i_stim = i_external(tn)
        else:
            i_stim = 0

        for i, gates in enumerate(gates_vector):
            i_ion_i, gates_i = hh_current(dt, V_n[i], gates, k, currents_dict=currents_dict)
            i_ion[i] = i_ion_i
            gates_vector[i]= gates_i

        i_tot = i_stim - i_ion

        # # Prepare linear system
        tau = Cm * R_a
        A = np.eye(C.shape[0]) - dt / tau * C
        b = V_n + dt / Cm * i_tot
        if v_e is not None:
            potential = v_e(tn)
            activation = np.gradient(np.gradient(potential))
            b += dt / tau * activation

        # Solve system
        V_n = np.linalg.solve(A, b)
        V.append(V_n)
        currents.append(currents_dict)

    return np.array(V), timearray

