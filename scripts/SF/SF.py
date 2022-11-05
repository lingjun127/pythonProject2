import networkx as nx
import powerlaw
import numpy as np

def new_networkSF(n, gamma):
    g1 = generateSFNetwork(n=n, gamma=gamma)
    g2 = generateSFNetwork(n=n, gamma=gamma)
    nx.relabel_nodes(g2, lambda x: x + len(g1.nodes()), copy=False)
    for e in g1.edges():
        g1.edges[e]['Value'] = 1
    for e in g2.edges():
        g2.edges[e]['Value'] = 2
    for node in g1.nodes():
        g1.nodes[node]['Value'] = 1
    for node in g2.nodes():
        g2.nodes[node]['Value'] = 2

    G = nx.union(g1, g2)
    n1 = set(g1.nodes())
    n2 = set(g2.nodes())

    while n1:
        a = n1.pop()
        while n2:
            b = n2.pop()
            break
        G.add_edge(a, b, Value=3)
    return G, g1, g2


def is_graphic_Erdos_Gallai(degree_sequence_to_test):
    degree_sequence = sorted(degree_sequence_to_test, reverse=True)
    S = sum(degree_sequence)
    n = len(degree_sequence)
    if S % 2 != 0:
        return False
    for r in range(1, n):
        M = 0
        S = 0
        for i in range(1, r + 1):
            S += degree_sequence[i - 1]
        for i in range(r + 1, n + 1):
            M += min(r, degree_sequence[i - 1])
        if S > r * (r - 1) + M:
            return False
    return True

def ConfigurationModel(degrees, relax=False):
    # assume that we are given a graphical degree sequence
    if not is_graphic_Erdos_Gallai(degrees):
        return 0

    # create empty network with n nodes
    n = len(degrees)
    g = nx.Graph()

    # generate link stubs based on degree sequence
    stubs = []
    for i in range(n):
        for k in range(degrees[i]):
            stubs.append(i)

    # connect randomly chosen pairs of link stubs
    # note: if relax is True, we conceptually allow self-loops
    # and multi-edges, but do not add them to the network/
    # This implies that the generated network may not have
    # exactly sum(degrees)/2 links, but it ensures that the algorithm
    # always finishes.
    while (len(stubs) > 0):
        v, w = np.random.choice(stubs, 2, replace=False)
        if relax or (v != w and ((v, w) not in g.edges.keys())):
            # do not add self-loops and multi-edges
            if (v != w and ((v, w) not in g.edges.keys())):
                g.add_edge(v, w)
            stubs.remove(v)
            stubs.remove(w)
    return g


def generateSFNetwork(n=1000, gamma=2.1):

    # degrees_zipf = [1]
    degrees_powerlaw = [1]
    while not is_graphic_Erdos_Gallai(degrees_powerlaw):
        # degrees_zipf = [int(x) for x in np.random.zipf(gamma, n)]
        degrees_powerlaw = powerlaw.Power_Law(xmin=2, parameters=[gamma]).generate_random(n).astype('int')
    g = ConfigurationModel(degrees_powerlaw, relax=True)
    return g
