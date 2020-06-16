

import networkx as nx


sif_file = './examples/networks/coev_graph_0_32.sif'

gml_file = './csn_transIII_n32.graphml'

fr = open(sif_file, 'r')

G = nx.Graph()

for edge in fr:

    edge = edge.strip()
    # temp_list = edge.split('\linked\t')
    temp_list = edge.split(' coevSimilar ')
    if len(temp_list) > 1:
        G.add_edge(temp_list[0], temp_list[1])
        G.add_node(temp_list[0], id = temp_list[0])
        G.add_node(temp_list[1], id = temp_list[1])
    else:
        G.add_node(temp_list[0], id = temp_list[0])


print G.nodes()
nx.write_graphml(G, gml_file)
