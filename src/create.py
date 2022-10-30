import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import powerlaw


def new_network(n, k):
    """
    生成两个网络
    :param n:节点数
    :param k:连边概率系数
    :return:
    G:
    g1:
    g2:
    """
    # 生成两个随机图
    g1 = nx.gnp_random_graph(n, k / n)
    g2 = nx.gnp_random_graph(n, k / n)

    # 重新标记节点
    nx.relabel_nodes(g2, lambda x: x + len(g1.nodes()), copy=False)
    for node in g1.nodes:
        g1.nodes[node]['layer'] = 1
    for node in g2.nodes:
        g2.nodes[node]['layer'] = 2

    for e in g1.edges:
        g1.edges[e]['layer'] = 1
    for e in g2.edges:
        g2.edges[e]['layer'] = 2

    # 组合g1和g2成为G
    G = nx.union(g1, g2)
    n1 = set(g1.nodes())
    n2 = set(g2.nodes())

    # 全连接
    while n1:
        a = n1.pop()
        while n2:
            b = n2.pop()
            break
        G.add_edge(a, b, layer=3)
    return G, g1, g2


# def nodeSetting(G, layer=1):
#     """
#     生成(x,y,z)坐标，节点ID和属性设置级联方法(x,y)坐标遵循networkx spring布局
#     将(x,y,z)坐标保存为名为'3D_pos'节点的属性。该信息用于绘制相互依赖的图
#     :param G:
#     :param layer:
#     :return:
#     """
#     pos = nx.spring_layout(G)
#     for node in pos:
#         pos[node] = np.append(pos[node], layer)
#     nx.set_node_attributes(G, pos, name='3D_pos')
#
#     # 添加节点属性 'layer'
#     for node in G.nodes():
#         G.nodes[node]['layer'] = layer
#
#     for e in G.edges():
#         G.edges[e]['lager'] = layer
#
#     # 节点重命名
#     mapping = {}
#     for node in G.nodes():
#         mapping[node] = str(layer) + '-' + str(node)
#
#     return nx.relabel_nodes(G, mapping)


def SF_powerlaw_exp(G):
    """
    计算幂律度分布的伽马值
    :param G:网络图
    :return:幂律度分布的伽玛值
    """
    # 拟合幂律，放到名为fit的对象中。网络度是离散的，所以要用discrete=True。
    # 是不是离散型数据，可以用fit.discrete来查看。
    # 计算fit的最小界值。
    # 计算fit的alpha值。根据所遵循公式，alpha是幂指数，即P(x)是x的-alpha次方。
    # 也就是我们想要的参数值了，参考文献中讲到是通过最大似然估计得到的。一般幂律分布的该参数范围在2-3是很典型的值。
    d = [G.degree()[i] for i in G.nodes()]
    fit = powerlaw.Fit(d, discrete=True, verbose=False)
    alpha = fit.alpha
    return alpha


def networkER_w_3Dpos(N, avg_degree, layer=1):
    """

    :param N: 节点数量
    :param avg_degree: 期望的平均度
    :param layer: 层级
    :return:ER网络的图
    """
    G = nx.erdos_renyi_graph(N, avg_degree / N)
    return nodeSetting(G, layer)
def intd_random_net(G_a, G_b):
    """
    连接两个节点数相同的随机网络
    :param G_a:网络A
    :param G_b:网络B
    :return:
    """
    if len(G_a.nodes()) != len(G_b.nodes()):
        print("所给的网络节点数不同")

    else:
        _ = list(G_a.nodes())[0]
        a_layer = _.split('-')[0]
        _ = list(G_b.nodes())[0]
        b_layer = _.split('-')[0]

        G = nx.union(G_a, G_b)
        for i in range(len(G_a.nodes())):
            G.add_edge(a_layer + '-' + str(i),
                       b_layer + '-' + str(i)
                       )

    return G
