from src.measure import *
import numpy as np
from scipy.interpolate import make_interp_spline

ER500 = np.loadtxt('../notebooks/results/ER/t20/ERn500k4_20.csv', delimiter=",")
ER1000 = np.loadtxt('../notebooks/results/ER/t20/ERn1000k4_20.csv', delimiter=",")
ER2000 = np.loadtxt('../notebooks/results/ER/t20/ERn2000k4_20.csv', delimiter=",")
ER4000 = np.loadtxt('../notebooks/results/ER/t20/ERn4000k4_20.csv', delimiter=",")

# 平滑曲线
re = []
for data in [ER500, ER1000, ER2000, ER4000]:
    x = data[0]
    y = data[1]
    model = make_interp_spline(x, y)
    xs = np.linspace(0, 1, 100)
    ys = model(xs)
    re.append([xs, ys])


plot_pinf(re, k=4,
          labels=["ER model, N=500,  <k>=4", "ER model, N=1000, <k>=4", "ER model, N=2000, <k>=4",
                  "ER model, N=4000, <k>=4",
                  ],
          path="../notebooks/figure/ER_t20.png", p_theory=True)



