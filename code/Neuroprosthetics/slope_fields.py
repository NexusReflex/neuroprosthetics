import numpy as np
import matplotlib.pyplot as plt


def plotIsoc(t_grid_array, v_grid_array, dv_iso_array, dt, dv, name,
             list_of_isoc_constants=[-2, -1, 0, 1, 2], fontsize=13,
             plot_isoclines=True, save=False):
    # Create everything, plot some data stored in `x` and `y`

    plt.rcParams['figure.figsize'][0] = 10  # LaTeX \textwidth
    plt.rcParams['legend.fontsize'] = 11
    ax = plt.axes()

    ax.tick_params(axis='both', which='major', pad=10, labelsize=fontsize,
                   direction='in')  # set tick properties

    plt.xlim(-6, 6)  # set axis limits
    plt.ylim(-5, 5)
    plt.xticks(np.arange(-6, 6.000001, step=2))  # set tick ranges
    plt.yticks(np.arange(-5, 5.000001, step=5))

    plt.quiver(t_grid_array, v_grid_array, dt, dv, width=0.0014, headwidth=4,
               label='Slope field',
               color='xkcd:azure')  # Plot the vectors

    if (plot_isoclines):
        isoclines = plt.contour(t_grid_array, v_grid_array, dv_iso_array,
                                list_of_isoc_constants,
                                linewidths=1)  # plot isocs

        labels = ['isocline -2 v/s', 'isocline -1 v/s', 'isocline 0 v/s',
                  'isocline 1 v/s',
                  'isocline 2 v/s']

        for i in range(len(labels)):
            isoclines.collections[i].set_label(
                labels[i])  # labels for isoc lines
        plt.legend(loc='upper right')

    plt.xlabel('t(s)', fontsize=fontsize)
    plt.ylabel('V(V)', fontsize=fontsize)
    plt.tight_layout()

    if save:
        path = '../latex/tex_2/imgs/'
        plt.savefig(path + name, format='eps')

    plt.show()
