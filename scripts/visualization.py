import matplotlib.pyplot as plt


def load_matplotlib():
    plt.rc('figure', figsize=(8, 6))
    plt.rcParams['font.size'] = 17
    plt.rcParams['text.usetex'] = True
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = 'Coolvetica'
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'


def add_legend(loc='best', ncol=1, frameon=False, fontsize=14, labelspacing=0.02):
    plt.legend(fontsize=fontsize, loc=loc, handlelength=1, frameon=frameon,
               borderpad=0.1, ncol=ncol, labelspacing=labelspacing, fancybox=False,
               columnspacing=0.3)


def save_figure(filename: str):
    """
    Save matplotlib figure in correct extension
    :param filename: Name of output plot
    """
    extension = filename.split('.')[-1]
    if extension == "png":
        plt.savefig(filename, bbox_inches='tight', dpi=300)
    elif extension == "pdf" or extension == "svg":
        plt.savefig(filename, bbox_inches='tight')
    else:
        print('Error. Cannot save figure, unsupported extension: [{}]'.format(extension))