import matplotlib.pyplot as plt

def set_plot_params(size=[5,5], fontsize=None, ticksize=None, tickwidth=None, spines=False):
    plt.rcParams['figure.figsize'] = size
    plt.rcParams['axes.spines.right'] = spines
    plt.rcParams['axes.spines.top'] = spines

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


def __create_figures(n):
    import matplotlib.pyplot as plt
    for i in range(n):
        yield plt.figure()


def multiple_axes(rows, cols, multiplot=True, title=None, do_flatten=True, **kwargs):
    import matplotlib.pyplot as plt
    import numpy as np
    f = plt.gcf()
    if multiplot:
        f, axes = plt.subplots(rows, cols, **kwargs)
        if do_flatten:
            axes = axes.flatten()
    else:
        figures = [f for f in __create_figures(rows*cols)]
        if do_flatten:
            axes = [f.gca() for f in figures]
        else:
            f2 = figures[:]
            axes = [[f2.pop(0).gca() for _ in range(cols)] for _ in range(rows)]
        axes = np.array(axes)
    yield axes
    if multiplot:
        f.tight_layout()
        if title is not None:
            f.suptitle(title)
    else:
        for fig in figures:
            fig.tight_layout()