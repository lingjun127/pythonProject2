from src.create import *
from src.attack import *
from src.measure import *

G_int, g1, g2 = new_network(1000, 8)

# 失效概率
p = 2.45 / 8
# 结果集
p_infs = []
# 第一阶段
G_att, g1, g2 = att.attack_network_option(G_int, g1, g2, p, False)
p_inf, p_inf_layer1, p_inf_layer2 = compute_pinf(G_att, G_int)
print(p_inf)
p_infs.append(p_inf)
print("----------")
n = 2

while n <= 80:
    if n % 2 == 0:
        G_att, g1, g2 = cascade_rec_option(G_att, g1, g2, counter=1, verbose=False)
        p_inf, p_inf_layer1, p_inf_layer2 = compute_pinf(G_att, G_int)
        p_infs.append(p_inf)
    else:
        G_att, g1, g2 = cascade_rec_option(G_att, g2, g1, counter=1, verbose=False)
        p_inf, p_inf_layer1, p_inf_layer2 = compute_pinf(G_att, G_int)
        p_infs.append(p_inf)
        # 交换让g1、g2正常顺序
        t = g2
        g2 = g1
        g1 = t

    n = n + 1
ERn1000k8 = np.array(p_infs)
print(ERn1000k8)
np.savetxt('../notebooks/results/ER/FIG6/ERn4000k8.csv', ERn1000k8, delimiter=',')
