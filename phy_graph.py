import time
import phyplot as pp

# 读取配置文件
conf_path = './phy_graph.conf'
info = pp.read_conf(conf_path)

# 计算方程表达式
reg = pp.calculate(info)

# 作图
fig_path = './graph/{}.png'.format(time.strftime('%Y%m%d_%H%M%S', time.localtime()))
pp.draw(info, reg, fig_path)
