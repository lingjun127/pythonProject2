import matplotlib.pyplot as plt
from src.measure import *
import numpy as np

path = '../notebooks/figure/FIG4.png'
ERn2000k8 = np.loadtxt('../notebooks/results/ER/FIG4/ERn2000k8.csv', delimiter=",")
ERn1000k8 = np.loadtxt('../notebooks/results/ER/FIG4/ERn1000k8.csv', delimiter=",")
results = [ERn2000k8, ERn1000k8]
plt.figure(figsize=(10, 7))
plt.rcParams.update({'font.size': 14})

a = np.arange(80)
print(a)
print(ERn2000k8)

plt.plot(a, ERn2000k8)
plt.plot(a, ERn1000k8)
plt.ylim(0, 1)
plt.savefig(path, dpi=600, bbox_inches='tight')
plt.show()
