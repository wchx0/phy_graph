from email.policy import default
import os
import math
import shutil
import configparser
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.offsetbox as msb


def read_conf(path):
    '''传入配置文件路径；
以ConfigParser类返回配置文件中的变量。'''
    conf = configparser.ConfigParser()
    conf.read(path, encoding = 'utf-8')
    data = {
    'x':np.float64(conf.get('data', 'x').replace(' ', '').split(',')),
    'y':np.float64(conf.get('data', 'y').replace(' ', '').split(','))
    }
    conf.set('caption', 'text', '')

    x_data = data['x']

    return conf, data


def calculate(data):
    '''传入配置文件字典；
返回线性回归方程的参数。'''
    x_data = data['x']
    y_data = data['y']

    n = np.size(x_data)
    if n != np.size(y_data) or n < 3:
        raise Exception

    x_sum = x_data.sum()
    y_sum = y_data.sum()
    x_average = x_sum / n
    y_average = y_sum / n
    xx_sum = np.square(x_data).sum()
    xy_sum = (x_data * y_data).sum()
    l_xx = xx_sum - x_sum * x_sum / n
    l_xy = xy_sum - x_sum * y_sum / n
    k = l_xy / l_xx
    b = y_average - k * x_average
    r = l_xy / math.sqrt(l_xx * l_xy)
    
    y_pre = k * x_data + b
    y_dev = y_data - y_pre
    y_dev_square_sum = np.square(y_dev).sum()
    s_y = math.sqrt(y_dev_square_sum / (n - 2))
    s_k = s_y / math.sqrt(l_xx)
    s_b = s_k * math.sqrt(xx_sum / n)

    reg = {'k':k, 'b':b, 's_k':s_k, 's_b':s_b, 'y_pre':y_pre}

    return reg


def draw(conf, data, reg, path):
    '''传入配置文件字典、参数字典、图像保存路径；
作图并保存在特定路径。'''
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure()
    plt.grid(True)
    plt.scatter(data['x'], data['y'], color = 'black')
    plt.plot(data['x'], reg['y_pre'], color = 'black')
    plt.xlabel(conf.get('caption', 'x_label'))
    plt.ylabel(conf.get('caption', 'y_label'))
    plt.text(4.2, 2, s = conf.get('caption', 'text'))

    fig_name = '{}.png'.format(conf.get('caption', 'title'))
    try:
        plt.savefig(path + fig_name)
    except FileNotFoundError:
        os.makedirs(path)
        plt.savefig(path + fig_name)
    