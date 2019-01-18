
import netconv
import networkx as nx


def sifToNX(graph_file):

        n = netconv.Network()
        netconv.importSIF(n, graph_file)
        G = nx.Graph()
        netconv.netconv2NX(n,G)
        return G
