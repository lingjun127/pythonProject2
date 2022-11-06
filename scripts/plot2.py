import matplotlib.pyplot as plt
from src.measure import *
import numpy as np

SFn300_30_k4 = np.loadtxt('../notebooks/results/SF/t20/SFn300_30_k4.csv', delimiter=",")
SFn300_27_k4 = np.loadtxt('../notebooks/results/SF/t20/SFn300_27_k4.csv', delimiter=",")
SFn300_23_k4 = np.loadtxt('../notebooks/results/SF/t20/SFn300_23_k4.csv', delimiter=",")
ERn300k4_20 = np.loadtxt('../notebooks/results/ER/t20/ERn300k4_20.csv', delimiter=",")
path = '../notebooks/figure/FIG7.png'
results = [SFn300_30_k4, SFn300_27_k4, SFn300_23_k4, ERn300k4_20]
plt.figure(figsize=(10, 7))
plt.rcParams.update({'font.size': 14})
for i, res in enumerate(results):
    pks = res[0]
    p_infs = res[1]
    plt.plot(pks, p_infs, 'o-', )
plt.xlabel('p')
plt.ylabel('$P_{\inf}$')
plt.legend(["SF  $\lambda$=3", "SF  $\lambda$=2.7", "SF  $\lambda$=2.3", "ER  k=4"])
plt.ylim(0, 1)
plt.savefig(path, dpi=600, bbox_inches='tight')
# 生成网格线
plt.grid()
plt.show()
