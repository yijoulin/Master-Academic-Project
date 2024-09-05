import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.gridspec as gridspec
import numpy as np

def plot_grid(DATA_float_sets_1,DATA_float_sets_2,DATA_color_sets_1,DATA_color_sets_2,points_count_11, points_count_12, points_count_21, points_count_22):
    fig, axs = plt.subplots(2, 2)
    axs = axs.flatten()
    for ax in axs:
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
    gs = gridspec.GridSpec(5, 2, height_ratios=[1, 1, 1, 1, 1])

    axs[0] = fig.add_subplot(gs[0:3, 0])  # 占据第一行的全部列
    axs[1] = fig.add_subplot(gs[0:3, 1])  # 占据第二行的第一列
    axs[2] = fig.add_subplot(gs[3:, 0])  # 占据第二行的第二列
    axs[3] = fig.add_subplot(gs[3:, 1])  # 占据第三行的全部列


    def init():
        axs[2].set_xlim(0, 500)  # x轴显示从0到6
        axs[2].set_ylim(0, 33) # y轴显示从0到30
        axs[3].set_xlim(0, 500)  # x轴显示从0到6
        axs[3].set_ylim(0, 33) # y轴显示从0到30
        # 初始化时创建一个占位图例
        axs[2].plot([], [], '-', color='blue', label="Individual")
        axs[2].plot([], [], '-', color='red', label="Social")
        axs[3].plot([], [], '-', color='blue', label="Individual")
        axs[3].plot([], [], '-', color='red', label="Social")
        axs[2].legend(loc="upper right", fontsize='small')
        axs[3].legend(loc="upper right", fontsize='small')
        axs[0].set_title('High variance', fontsize=10)
        axs[1].set_title('No variance', fontsize=10)
        return tuple(axs)


    def update(frame):

        if frame == 0:  # 仅在第一帧绘制，避免重复绘制
            axs[2].plot(np.arange(frame + 1), points_count_11[:frame + 1], '-', color='blue', label="Individual")
            axs[2].plot(np.arange(frame + 1), points_count_12[:frame + 1], '-', color='red', label="Social")
            axs[3].plot(np.arange(frame + 1), points_count_21[:frame + 1], '-', color='blue', label="Individual")
            axs[3].plot(np.arange(frame + 1), points_count_22[:frame + 1], '-', color='red', label="Social")
        frame_color_1 = DATA_color_sets_1[frame]
        frame_color_2 = DATA_color_sets_2[frame]
        """更新动画帧"""
        # 前两个子图更新
        for i, data_float, data_color in zip(range(2), 
                                            [DATA_float_sets_1[frame], DATA_float_sets_2[frame]], 
                                            [DATA_color_sets_1[frame], DATA_color_sets_2[frame]]):
            axs[i].clear()  # 清除之前的内容
            axs[i].matshow(data_float, cmap='Greens')  # 更新背景色
            for x in range(10):
                for y in range(10):
                            # 在两个子图中绘制颜色点
                    colors1 = frame_color_1[x][y]
                    colors2 = frame_color_2[x][y]
                    for k, color in enumerate(colors1):
                        # 计算点的位置
                        row, col = divmod(k, 3)
                        xx = y - 0.3*(col % 3)+0.3
                        yy = x - 0.3*(row % 3)+0.3
                        axs[0].plot(xx, yy, '.', color=color, markersize=5)
                    for k, color in enumerate(colors2):
                        # 计算点的位置
                        row, col = divmod(k, 3)
                        xx = y - 0.3*(col % 3)+0.3
                        yy = x - 0.3*(row % 3)+0.3
                        axs[1].plot(xx, yy, '.', color=color, markersize=5)    
        
        # 后两个子图：折线图更新
        # 重新设置子图标题
        axs[0].set_title('High variance', fontsize=10)
        axs[1].set_title('No variance', fontsize=10)
        
        xdata = np.arange(frame + 1)
        axs[2].plot(xdata, points_count_11[:frame + 1],'-', color = 'blue',label="Individual")
        axs[2].plot(xdata, points_count_12[:frame + 1],'-', color = 'red',label="Social")
        axs[3].plot(xdata, points_count_21[:frame + 1],'-', color = 'blue',label="Individual")
        axs[3].plot(xdata, points_count_22[:frame + 1],'-', color = 'red',label="Social")

        return tuple(axs)

    ani = FuncAnimation(fig, update, frames=range(500), init_func=init, blit=False, interval=10)
    
    plt.tight_layout()
    plt.show()



def plot_bar_compare(list1, list2):
    fig, ax = plt.subplots(figsize=(5,7))
    ax.set_title("Last 500 round's average individual bee's number",fontsize=10)

    def animate(frame):
        ax.clear()
        ax.set_title("Last 500 round's average individual bee's number",fontsize=10)
        bar_locations = np.arange(1)
        ax.bar(bar_locations - 0.2, np.average(list1[:frame]), width=0.4, color = 'white',edgecolor='black', label='high_variance' )
        ax.bar(bar_locations + 0.2, np.average(list2[:frame]), width=0.4, color = 'grey',edgecolor='black', label='no_variance')
        ax.set_ylim(0, 1)
        ax.legend(fontsize=8)

        ax.text(0.58, 0.985, f'current timestep: {frame}', transform=ax.transAxes, horizontalalignment='right', verticalalignment='top', fontsize=8)
        ax.text(0.41, 0.1, f"current average: {format(list1[frame], '.2f')}", transform=ax.transAxes, horizontalalignment='right', verticalalignment='top', fontsize=8)
        ax.text(0.90, 0.1, f"current average: {format(list2[frame], '.2f')}", transform=ax.transAxes, horizontalalignment='right', verticalalignment='top', fontsize=8)
    ani = FuncAnimation(fig, animate, frames=len(list1), repeat = False, interval=100)
    plt.tight_layout()
    plt.show()
    plt.close()  # Prevents duplicate display
