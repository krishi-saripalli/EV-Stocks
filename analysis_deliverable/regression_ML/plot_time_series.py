import matplotlib.pyplot as plt
from regression import preprocess_sequential_data


def make_time_plots():
    prices = preprocess_sequential_data()
    indices = [i for i in range(436)]
    fig, ax = plt.subplots(2, 2)
    fig.suptitle("Prices of Assets over Time")
    ax[0, 0].plot(indices, prices['Stocks'], 'tab:orange')
    ax[0, 0].set_title("Stocks")
    ax[0, 0].set_xticks([])
    ax[0, 1].plot(indices, prices['Oil'], 'tab:green')
    ax[0, 1].set_title("Oil")
    ax[0, 1].set_xticks([])
    ax[1, 0].plot(indices, prices['Lithium'], 'tab:red')
    ax[1, 0].set_title("Lithium")
    ax[1, 0].set_xticks([])
    ax[1, 1].plot(indices, prices['Gold'])
    ax[1, 1].set_title("Gold")
    ax[1, 1].set_xticks([])
    plt.show()


make_time_plots()
