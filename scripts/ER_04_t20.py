from src.measure import *

print("\n++++++++++++++++++++++++++++++")
print("ER N500 Test Start...")
print("++++++++++++++++++++++++++++++\n")
ERn500k4_20 = generate_pinf_ER(500, 4, 1)
np.savetxt('../notebooks/results/ER/t20/ERn500k4_20.csv', ERn500k4_20, delimiter=',')
