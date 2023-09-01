# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk


def generate_rubik_cube(nx, ny, nz):
    """
    根据输入生成指定尺寸的魔方
    :param nx:
    :param ny:
    :param nz:
    :return:
    """
    # 准备一些坐标
    n_voxels = np.ones((nx + 2, ny + 2, nz + 2), dtype=bool)

    # 生成间隙
    size = np.array(n_voxels.shape) * 2
    filled_2 = np.zeros(size - 1, dtype=n_voxels.dtype)
    filled_2[::2, ::2, ::2] = n_voxels

    # 缩小间隙
    # 构建voxels顶点控制网格
    # x, y, z均为6x6x8的矩阵，为voxels的网格，3x3x4个小方块，共有6x6x8个顶点。
    # 这里//2是精髓，把索引范围从[0 1 2 3 4 5]转换为[0 0 1 1 2 2],这样就可以单独设立每个方块的顶点范围
    x, y, z = np.indices(np.array(filled_2.shape) + 1).astype(float) // 2  # 3x6x6x8，其中x,y,z均为6x6x8

    x[1::2, :, :] += 0.95
    y[:, 1::2, :] += 0.95
    z[:, :, 1::2] += 0.95

    # 修改最外面的面
    x[0, :, :] += 0.94
    y[:, 0, :] += 0.94
    z[:, :, 0] += 0.94

    x[-1, :, :] -= 0.94
    y[:, -1, :] -= 0.94
    z[:, :, -1] -= 0.94

    # 去除边角料
    filled_2[0, 0, :] = 0
    filled_2[0, -1, :] = 0
    filled_2[-1, 0, :] = 0
    filled_2[-1, -1, :] = 0

    filled_2[:, 0, 0] = 0
    filled_2[:, 0, -1] = 0
    filled_2[:, -1, 0] = 0
    filled_2[:, -1, -1] = 0

    filled_2[0, :, 0] = 0
    filled_2[0, :, -1] = 0
    filled_2[-1, :, 0] = 0
    filled_2[-1, :, -1] = 0

    # 给魔方六个面赋予不同的颜色
    colors = np.array(['#ffd400', "#fffffb", "#f47920", "#d71345", "#145b7d", "#45b97c"])
    facecolors = np.full(filled_2.shape, '#77787b')  # 设一个灰色的基调
    # facecolors = np.zeros(filled_2.shape, dtype='U7')
    facecolors[:, :, -1] = colors[0]  # 上黄
    facecolors[:, :, 0] = colors[1]  # 下白
    facecolors[:, 0, :] = colors[2]  # 左橙
    facecolors[:, -1, :] = colors[3]  # 右红
    facecolors[0, :, :] = colors[4]  # 前蓝
    facecolors[-1, :, :] = colors[5]  # 后绿
    ax = plt.figure().add_subplot(projection='3d')
    ax.voxels(x, y, z, filled_2, facecolors=facecolors)
    # 隐藏坐标轴
    ax.set_axis_off()
    return ax


class RubikCubeApp:
    def __init__(self, root, nx, ny, nz):
        self.root = root
        self.root.title("妃妃魔方")

        # 创建一个Frame来容纳Matplotlib图形
        self.frame = ttk.Frame(self.root)
        self.frame.pack(expand=True, fill=tk.BOTH)

        # 生成魔方并将其添加到Matplotlib图形中
        self.ax = generate_rubik_cube(nx, ny, nz)
        self.canvas = FigureCanvasTkAgg(self.ax.figure, master=self.frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(expand=True, fill=tk.BOTH)

        # 鼠标事件处理
        self.canvas_widget.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas_widget.bind("<B1-Motion>", self.on_mouse_drag)

        # 初始化鼠标拖动状态
        self.dragging = False
        self.prev_x = None
        self.prev_y = None

    def on_mouse_press(self, event):
        # 记录鼠标按下的初始位置
        self.dragging = True
        self.prev_x = event.x
        self.prev_y = event.y

    def on_mouse_drag(self, event):
        if self.dragging:
            # 计算鼠标拖动的距离
            delta_x = event.x - self.prev_x
            delta_y = event.y - self.prev_y

            # 根据鼠标拖动距离旋转魔方
            self.ax.view_init(elev=self.ax.elev + delta_y, azim=self.ax.azim + delta_x)
            self.canvas.draw()

            # 更新鼠标位置
            self.prev_x = event.x
            self.prev_y = event.y


if __name__ == '__main__':
    root = tk.Tk()
    app = RubikCubeApp(root, 3, 3, 3)
    root.mainloop()
