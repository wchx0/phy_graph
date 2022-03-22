import phyplot as pp

# 读取配置文件
conf_path = './config.ini'
conf, data = pp.read_conf(conf_path)

# 计算方程表达式
reg = pp.calculate(data)

# 作图
fig_path = './graph/'
pp.draw(conf, data, reg, fig_path)
