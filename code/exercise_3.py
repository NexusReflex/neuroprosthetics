from .Neuroprosthetics.solver import plotSolver, forwardEuler, heun, expoEuler
from .Neuroprosthetics.LIF_neuron import plotLif, lif as LIF


def main():
    start = -4.5
    stop = 5
    stepsizes = [1, 0.5, 0.1, 0.012]
    v_init = -4

    # DGL
    dV_dt = lambda V, t: 1 - V - t  # DGL nr.1

    plotSolver('forwardEul.eps', forwardEuler, v_init, stepsizes, start, stop, dV_dt)

    plotSolver('heun.eps', heun, v_init, stepsizes, start, stop, dV_dt)

    plotSolver('expo.eps', expoEuler, v_init, stepsizes, start, stop, dV_dt)

    input_current_1 = 0.00001
    voltages_10mu, times_10mu = LIF(input_current_1)
    plotLif('10muA_const_curr.eps', voltages_10mu,times_10mu)

    voltages_10mu_rect, times_10mu_rect = LIF(input_current_1, i_const=False)
    plotLif('10muA_rect_curr.eps', voltages_10mu_rect,times_10mu_rect)

    input_current_2 = 0.00002
    voltages_20mu, times_20mu = LIF(input_current_2)
    plotLif('20muA_const_curr.eps', voltages_20mu,times_20mu)

    input_current_3 = 0.00003
    voltages_30mu_rect, times_30mu_rect = LIF(input_current_3, i_const=False)
    plotLif('30muA_rect_curr.eps', voltages_30mu_rect,times_30mu_rect)


if __name__== "__main__":
    main()