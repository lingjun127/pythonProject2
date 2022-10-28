import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from datetime import datetime
from time import sleep
from tqdm import tqdm
import src.create as gen_rand
import src.attack as att


def compute_pinf(G_att, G_init, mut=None):
    """

    :param G_att: 被攻击后的网络
    :param G_init: [Graph] 初始网络
    :param mut:
    :return:
        - p_inf:[float] 属于连通巨大组件的节点数/总的节点数

    """
    if len(G_att.nodes()) == 0:
        return 0, 0, 0
    total_num_nodes = len(G_init.nodes())

    if mut is not None:
        total_num_nodes = mut

    # 计算被攻击后的分别属于网络A和网络B的节点数
    comp_set = list(nx.connected_components(G_att))
    giant_comp = max(comp_set, key=len)
    layer1, layer2 = giant_layercount(G_att, giant_comp)

    # 计算初始网络属于网络A和网络B的节点数
    comp_set_init = list(nx.connected_components(G_init))
    gaint_comp_init = max(comp_set_init, key=len)
    layer1_init, layer2_init = giant_layercount(G_init, gaint_comp_init)

    # 计算结果
    p_inf = len(giant_comp) / len(gaint_comp_init)
    p_inf_layer1 = layer1 / layer1_init
    p_inf_layer2 = layer2 / layer2_init
    return p_inf, p_inf_layer1, p_inf_layer2


def giant_layercount(G, giant_comp):
    """
    计算级联网络中分别属于网络A和网络B的节点数
    :param G:
    :param giant_comp:极大连通子图
    :return:
        - layer1：属于网络A的节点数量
        - layer2：属于网络B的节点数量
    """
    layer1 = 0
    layer2 = 0
    layer_dict = dict(nx.get_node_attributes(G, 'layer'))
    for node in giant_comp:
        layer = layer_dict[node]
        if layer == 1:
            layer1 += 1
        if layer == 2:
            layer2 += 1

    return layer1, layer2


def generate_pinf_ER(n, k, t=2, hasGraph=False, files=[]):
    """
    生成ER网络模型的数据
    :param n: 网络节点个数
    :param k: 平均度
    :param t: 循环次数
    :param hasGraph:
    :param files:
    :return: [p,p_inf]
       -p:每个节点被攻击的概率
       -p_inf:存在相互连通组件的概率
    """
    if hasGraph:
        g1 = nx.read_gpickle(files[0])
        g2 = nx.read_gpickle(files[1])
        G_int = nx.read_gpickle(files[2])
        print("级联网络的数据已给出")

    else:
        start = datetime.now()
        g1 = gen_rand.networkER_w_3Dpos(n, k, 1)
        g2 = gen_rand.networkER_w_3Dpos(n, k, 2)
        G_int = gen_rand.intd_random_net(g1, g2)
        time = datetime.now() - start
        print("级联网络已生成", time)

    p_infs = []
    ps = np.linspace(0, 1, 10)
    for p in tqdm(ps):
        print("当前p:\n", p)
        start = datetime.now()
        mean_p_inf = 0
        for i in range(t):
            print("本轮次数:", i+1, "/", t)
            G_att = att.attack_network(G_int, g1, g2, p, False)
            p_inf = compute_pinf(G_att, G_int)
            mean_p_inf += p_inf[0]

        p_infs.append(mean_p_inf / t)

    time = datetime.now() - start
    print(": '%f' 完成!" % (p), time)
    return ps, np.array(p_infs)


def plot_pinf(results, k=1, xlim=None, labels=None, path=None, p_theory=False, residual=False):
    """
    :param results:数据
    :param k:网络的平均度
    :param xlim:
    :param labels:每个结果的标签
    :param path:保存图的路径
    :param p_theory:p_c的理论值
    :param residual:
    :return:
    """

    plt.figure(figsize=(10, 7))
    plt.rcParams.update({'font.size': 14})
    color = iter(plt.cm.rainbow(np.linspace(0.0, 1, len(results))))
    # 点的图形
    # marker = ['o', 's', 'D', 'v',]

    for i, res in enumerate(results):
        pks = res[0] * k
        p_infs = res[1]
        plt.plot(pks, p_infs, c=next(color), linewidth=2,  mfc="None")

    if p_theory:
        plt.vlines(2.4554, ymin=0, ymax=1, colors='k', linestyles='dashdot', label='$p_{c}$=2.4554/<k>')

        plt.xlabel('pa')

    if residual:
        plt.hlines(results[0][1][0], xmin=0, xmax=1, linestyles='dotted', colors='k')
    plt.ylabel('$P_{inf}$')
    # plt.xlim(0,0.9)
    plt.ylim(0, 1)
    # plt.ylabel('$P_{node}$(in Gcomponent)')
    if labels:
        plt.legend(labels)
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.grid()
    plt.show()
