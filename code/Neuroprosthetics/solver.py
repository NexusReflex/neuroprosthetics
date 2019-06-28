import numpy as np
import matplotlib.pyplot as plt
# Implement the following numerical differential equation solvers as functions

def forwardEuler(stepsize, start_time, end_time, v_n, dVdt):
    # 1. Forward (Explicit) Euler
    voltages = [v_n]
    times = [start_time]

    # Solve forward Euler for each timestep
    for t_n in frange(start_time, end_time-stepsize+0.0001, stepsize):
        # for "perfect" plot, all lines ending latest at 5 on x-axis
        v_n_plus_1 = v_n + dVdt(v_n, t_n) * stepsize
        v_n = v_n_plus_1

        voltages.append(v_n)
        times.append(t_n+stepsize)

    return voltages, times


def heun(stepsize, start_time, end_time, v_n, dVdt):
    # 2. Heun
    voltages = [v_n]
    times = [start_time]

    # Solve Heun for each timestep
    for t_n in frange(start_time, end_time-stepsize+0.0001, stepsize):
        # for "perfect" plot, all lines ending latest at 5 on x-axis
        A = dVdt(v_n, t_n)
        v_approx = v_n + A * stepsize
        t_n_plus_1 = t_n + stepsize
        B = dVdt(v_approx, t_n_plus_1)
        v_n_plus_1 = v_n + ((A+B)/2) * stepsize
        v_n = v_n_plus_1
        voltages.append(v_n)
        times.append(t_n+stepsize)

    return voltages, times


def expoEuler(stepsize, start_time, end_time, v_n):
    # 3. Exponential Euler
    voltages = [v_n]
    times = [start_time]

    for t_n in frange(start_time, end_time-stepsize+0.0001, stepsize):
        # for "perfect" plot, all lines ending latest at 5 on x-axis
        A_n = -1
        B_n = 1 - t_n
        v_n_plus_1 = v_n * np.exp(A_n * stepsize) + ((B_n/A_n)*(np.exp(A_n * stepsize) - 1))
        v_n = v_n_plus_1
        voltages.append(v_n)
        times.append(t_n + stepsize)

    return voltages, times


def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step


def plotSolver(name, solver, v_zero, steps, first, last, dvdt, fontsize=13):
    # Create everything, plot some data stored in `x` and `y`

    plt.rcParams['figure.figsize'][0] = 10  # LaTeX \textwidth
    plt.rcParams['legend.fontsize'] = 11
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.spines.top'] = False
    ax = plt.axes()

    ax.tick_params(axis='both', which='major', pad=10, labelsize=fontsize,
                   direction='in')  # set tick properties


    plt.xlim(-4.5, 5.5)  # set axis limits
    plt.ylim(-4.5, 6)
    plt.xticks(np.arange(-5, 5.000001, step=1))  # set tick ranges
    plt.yticks(np.arange(-4, 6.000001, step=2))

    for step in steps:
        voltages, timesteps = solver(step, first, last, v_zero, dvdt)
        plt.plot(timesteps, voltages, label='$\Delta$ t = ' + str(step) + ' s')

    plt.legend(loc='upper right')
    plt.grid(True)
    plt.xlabel('t (s)', fontsize=fontsize)
    plt.ylabel('V (V)', fontsize=fontsize)
    plt.tight_layout()

    # path = '../latex/tex_3/imgs/'
    # plt.savefig(path + name, format='eps')
    plt.show()