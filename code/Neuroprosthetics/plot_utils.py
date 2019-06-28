import matplotlib.pyplot as plt

def set_plot_params(size=[5,5], fontsize=None, ticksize=None, tickwidth=None):
    plt.rcParams['figure.figsize'] = size
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.spines.top'] = False

    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    if fontsize is not None:
        plt.rcParams['axes.labelsize'] = fontsize
        plt.rcParams['xtick.labelsize'] = fontsize
        plt.rcParams['ytick.labelsize'] = fontsize

    if ticksize is not None:
        plt.rcParams['xtick.major.size'] = ticksize
        plt.rcParams['ytick.major.size'] = ticksize

    if tickwidth is not None:
        plt.rcParams['xtick.major.width'] = tickwidth
        plt.rcParams['ytick.major.width'] = tickwidth