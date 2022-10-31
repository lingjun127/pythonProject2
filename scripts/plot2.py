import matplotlib.pyplot as plt
# 测试
from src.measure import *
import numpy as np
from scipy.interpolate import make_interp_spline, interp1d

ER500 = np.loadtxt('../notebooks/results/ER/t20/ERn500k4_20.csv', delimiter=",")
ER1000 = np.loadtxt('../notebooks/results/ER/t20/ERn1000k4_20.csv', delimiter=",")
ER2000 = np.loadtxt('../notebooks/results/ER/t20/ERn2000k4_20.csv', delimiter=",")
ER4000 = np.loadtxt('../notebooks/results/ER/t20/ERn4000k4_20.csv', delimiter=",")
k = 4
path = '../notebooks/figure/figure4.png'
results = [ER500, ER1000, ER2000, ER4000]
# results = [ER500, ER1000]
# results = [ER500, ER1000, ER2000]

re = []
for data in [ER500, ER1000, ER2000, ER4000]:
    x = data[0]
    y = data[1]
    model = make_interp_spline(x, y)
    xs = np.linspace(0, 1, 100)
    ys = model(xs)
    re.append([xs, ys])

plt.figure(figsize=(10, 7))
plt.rcParams.update({'font.size': 14})

for i, res in enumerate(results):
    pks = res[0] *k
    p_infs = res[1]
    plt.plot(pks, p_infs)

# plt.vlines(2.4554, ymin=0, ymax=1, colors='k', linestyles='dashdot', label='$p_{c}$=2.4554/<k>')
plt.xlabel('pa')
plt.ylabel('$P_{inf}$')

# plt.ylim(0, 1)
plt.xlim(2.36, 2.5)
plt.savefig(path, dpi=600, bbox_inches='tight')
# 生成网格线
plt.grid()
plt.show()
