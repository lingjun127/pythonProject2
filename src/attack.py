import networkx as nx
import numpy as np


def foreign_neighbors(node, G):
    """
    找出目标节点的非本网络的所有邻居节点的集合
    :param node:目标节点
    :param G:任意一个图
    :return:目标节点在非本网络的所有邻居节点的集合
    """
    foreign = []
    t = G.nodes[node]['layer']
    s = set(G.neighbors(node))
    while s:
        x = s.pop()
        if G.nodes[x]['layer'] != t:
            foreign.append(x)

    if len(foreign) == 0:
        foreign = [None]

    return set(foreign)


def cascade_fail(G, g1, g2, target, verbose=False):
    """
    删除目标节点和与它相邻的节点
    :param G:级联网络
    :param g1:网络A
    :param g2:网络B
    :param target:目标节点
    :param verbose:可视化选项
    :return:G2 ,g1, g2 更新后的图
    """
    G2 = G.copy()
    # 如果是级联网络，从其他网络删除相邻节点

    # 目标节点所属网络
    num = G2.nodes[target]['layer']
    # print("所属网络", num)
    foreign_nodes = foreign_neighbors(target, G)
    if len(foreign_nodes) != 0:
        for node in foreign_nodes:
            G2.remove_node(node)
            # 如果被攻击的g2网络中节点，删除与其相连的g1中的节点
            if num == 2:
                g1.remove_node(node)
            else:
                g2.remove_node(node)
            if verbose:
                print("删除邻居节点", node)
    # 删除目标节点
    G2.remove_node(target)
    if num == 1:
        g1.remove_node(target)
    else:
        g2.remove_node(target)
    if verbose:
        print('删除目标节点', target)
    return G2, g1, g2


def cascade_rec(G, g1, g2, counter, verbose):
    """
    删除与远处节点的连边
    步骤：获取g2中的边。对于边的每个节点，找到它们的外部邻居。
    如果这两个集合中的节点位于g1中的不同簇中，则删除g2和G中的边对连接。
    :param G:
    :param g1:
    :param g2:
    :param counter:
    :param verbose:
    :return:G, g1, g2
    """
    removed = 0
    # 获取g2的边
    edges = set(g2.edges())
    # g1的组件
    components = list(nx.connected_components(g1))
    while edges:
        a, b = edges.pop()
        n1 = foreign_neighbors(a, G)
        n2 = foreign_neighbors(b, G)
        if n1 == {None} or n2 == {None}:
            continue

        for comp in components:
            if (n1.issubset(comp) and not n2.issubset(comp)) or (not n1.issubset(comp) and n2.issubset(comp)):
                G.remove_edge(a, b)
                g2.remove_edge(a, b)

                removed = 1
                if verbose:
                    print('删除', (a, b))
                break

    # 删除边后，检查其他边
    if removed == 1:
        cascade_rec(G, g2, g1, 1, verbose)

    # 计数器递减，递归出口
    if removed == 0 and counter > 0:
        cascade_rec(G, g2, g1, counter - 1, verbose)
    return G, g1, g2


def cascade_rec_optional(G, g1, g2, counter, verbose):
    """
    第2,3阶段去除边的方法
    步骤：得到g2的边。对于边缘对的每个节点，找出它的外部邻居。
    如果这两个集合中至少有一个节点在g1的同一个集群中，则在g2和G中保持连接。
    :param G:级联网络
    :param g1:网络A
    :param g2:网络B
    :param counter:计数器
    :param verbose:可视化选项
    :return:
    """
    removed = 0
    # g2的边
    edges = set(g2.edges())
    # g1的巨片
    components = list(nx.connected_components(g1))
    while edges:
        a, b = edges.pop()
        n1 = foreign_neighbors(a, G)
        n2 = foreign_neighbors(b, G)
        if n1 == set([]) or n2 == set([]):
            continue
        # 集合n1和n2中属于g1的同一个集群的节点数
        t = 0
        # 如果g2中边的两端连接g1中的两个不同巨片，则删边
        for _, comp in enumerate(components):
            if ({a}.issubset(comp) and not {b}.issubset(comp)) or (not {a}.issubset(comp) and {b}.issubset(comp)):
                g2.remove_edge(a, b)
                G.remove_edge(a, b)
                removed = 1

                if verbose:
                    print("删除边", (a, b))

        # 删除一条边，检查其他边
        if removed == 1:
            cascade_rec_optional(G, g2, g1, 1, verbose)
        # 递归出口
        if removed == 0 and counter > 0:
            cascade_rec_optional(G, g2, g1, counter - 1, verbose)
    return G, g1, g2


def attack_network(G, g1=nx.Graph(), g2=nx.Graph(), p=0.5, verbose=True):
    """
    在main中调用的入口函数。选择要攻击的节点，对每个目标运行级联失败
    :param G:
    :param g1:
    :param g2:
    :param p:
    :param verbose:
    :return: G
    """

    g1 = g1.copy()
    g2 = g2.copy()
    G = G.copy()

    # 随机选择节点从网络g1移除
    candidates = set()
    for node in g1.nodes():
        if np.random.random() < 1 - p:
            candidates.add(node)

    # 删除节点并更新集合
    while candidates:
        target = candidates.pop()
        if verbose:
            print('正在攻击', target)
        G, g1, g2 = cascade_fail(G, g1, g2, target=target, verbose=verbose)
        nodes_updated = set(G.nodes())
        candidates.intersection_update(nodes_updated)

    # 递归检测集群并移除相邻网络的连边
    G2, g1, g2 = cascade_rec(G, g1, g2, 1, verbose)
    return G2
