from src.measure import *

print("\n++++++++++++++++++++++++++++++")
print("SF N500  gamma=3 Test Start...")
print("++++++++++++++++++++++++++++++\n")
SFn300_30_k4 = generate_pinf_SF(n=300, gamma=3, t=100, s=0.5, e=1, d=30)
np.savetxt('../../notebooks/results/SF/t20/SFn300_30_k4.csv', SFn300_30_k4, delimiter=',')
