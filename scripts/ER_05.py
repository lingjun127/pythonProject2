from src.measure import *

print("\n++++++++++++++++++++++++++++++")
print("ER N300 Test Start...")
print("++++++++++++++++++++++++++++++\n")
ERn300k4_20 = generate_pinf_ER(300, 4, 1, s=0.5, e=1, d=30)
np.savetxt('../notebooks/results/ER/t20/ERn300k4_20.csv', ERn300k4_20, delimiter=',')
