import shutil
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.offsetbox as msb


def read_conf(path):
    '''传入配置文件路径，返回配置文件中的变量的字典。'''
    try:
        with open(path, encoding = 'utf-8') as conf:
            exec(conf.read())
    except:
        print('配置文件"phyplot.conf"损坏！\n请正确设置配置文件后重试。')
        input('按<Enter>退出。')

    info = vars()

    return info 

def calculate(info):
    '''传入配置文件字典，返回线性回归方程的参数。'''
    x_data = info['x_data']
    y_data = info['y_data']

    n = len(x_data)
    if n != len(y_data) or n < 3:
        raise Exception

    x_sum = sum(x_data)
    y_sum = sum(y_data)
    x_average = x_sum / n
    y_average = y_sum / n
    xx_sum = sum((x * x for x in x_data))
    xy_sum = sum((x * y for (x, y) in zip(x_data, y_data)))
    l_xx = xx_sum - x_sum * x_sum / n
    l_xy = xy_sum - x_sum * y_sum / n
    k = l_xy / l_xx
    b = y_average - k * x_average
    r = l_xy / math.sqrt(l_xx * l_xy)
    
    y_pre = [k * x + b for x in x_data]
    y_dev = [y_data[i] - y_pre[i] for i in range(n)]
    y_dev_square_sum = sum((dev * dev for dev in y_dev))
    s_y = math.sqrt(y_dev_square_sum / (n - 2))
    s_k = s_y / math.sqrt(l_xx)
    s_b = s_k * math.sqrt(xx_sum / n)

    reg = vars()

    return reg


def draw(info, reg, path):
    '''传入配置文件字典、参数字典、图像保存路径，作图并保存在特定路径。'''
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure()
    plt.grid(True)
    plt.scatter(info['x_data'], info['y_data'], color = 'black')
    plt.plot(info['x_data'], reg['y_pre'], color = 'black')
    plt.xlabel(info['x_label'])
    plt.ylabel(info['y_label'])
    plt.text(4.2, 2, s = info['text'])
    plt.savefig(path)
    