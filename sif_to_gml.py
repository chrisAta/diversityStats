

import networkx as nx


sif_file = './examples/new_ssn_SDR_n40.sif'

gml_file = './examples/ssn_SDR_n40.gml'

fr = open(sif_file, 'r')

G = nx.Graph()

for edge in fr:

    edge = edge.strip()
    # temp_list = edge.split('\tedge\t')
    temp_list = edge.split(' edge ')
    if len(temp_list) > 1:
        G.add_edge(temp_list[0], temp_list[1])
        G.add_node(temp_list[0], id = temp_list[0])
        G.add_node(temp_list[1], id = temp_list[1])
    else:
        G.add_node(temp_list[0], id = temp_list[0])


print G.nodes()
nx.write_gml(G, gml_file)
