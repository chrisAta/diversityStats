
import networkx as nx
from sifToNX import sifToNX
from gini_simpson import gini_simpson_dict, gini_simpson_value
from random import choice, sample
import max_min_diversity

def uniprot_EC_dict(tab_file):

    fr = open(tab_file, 'r')
    temp_dict = {}

    for line in fr:

        line = line.strip()
        temp_array = line.split('\t')
        id = temp_array[0]
        ec = temp_array[3]
        # ec = temp_array[-1]


        temp_dict[id] = ec

    return temp_dict

def sample_from_components(components, num_comp):

    temp_list = []
    # print components
    for i in range(0, num_comp):

            comp = sample(components, 1)[0]
            temp_entry = choice(comp)
            # print temp_entry
            temp_list += [temp_entry]

    return temp_list

def sample_from_components_cliques(components, num_comp):

    temp_list = []

    for comp in components:

        max_clique = max(list(nx.find_cliques(comp)))
        # print comp.nodes()
        # print max_clique
        temp_list += [choice(max_clique)]
        # print temp_list
        # print comp.nodes()
    # print temp_list
    # print len(temp_list)

    return temp_list

def multi_ginisimpson(iterations, components, dict, head, mat, graph=None):

    avg_coverage = 0.0
    avg_value = 0.0
    ec_num = len(set(dict.values())) / 2
    # ec_num = 50


    for i in range(0, iterations):
        # print i
        # rand_sample = sample_from_components(components, ec_num)
        # rand_sample = sample_from_components_cliques(components, ec_num)

        rand_sample = max_min_diversity.compute_diverse_set(mat, head, ec_num)
        # print rand_sample
        ginisimps_dict = gini_simpson_dict(rand_sample, dict)
        ginisimps_value = gini_simpson_value(ginisimps_dict)
        avg_coverage += len(ginisimps_dict.keys())
        avg_value += ginisimps_value

        # components = nx.connected_component_subgraphs(graph)


    # print min

    avg_coverage /= iterations
    avg_value /= iterations
    return avg_coverage, avg_value


def get_edgeless_nodes(components):

    count = 0

    for comp in components:
        if len(comp) == 1:
            count += 1

    return count

def main():

    ssn_file = './examples/ssn_transIII_n50.gml'
    csn_file = './examples/csn_transIII_n41.sif'
    # ssn_file = './examples/ssn_SDR_n50.gml'
    # csn_file = './examples/csn_SDR_n57.sif'


    tab_file = './transaminases_edited.tab.csv'
    # tab_file = './STR_143_annotation_edited.csv'

    # ssn_graph = sifToNX(ssn_file)
    ssn_graph = nx.read_gml(ssn_file)
    csn_graph = sifToNX(csn_file)

    uniprot_EC = uniprot_EC_dict(tab_file)
    ec_num = len(set(uniprot_EC.values()))
    iterations = 1

    print "Calculating SSN Component Count.."
    ssn_components = list(nx.connected_components(ssn_graph))
    ssn_components_graphs = nx.connected_component_subgraphs(ssn_graph)
    ssn_comp_num = nx.number_connected_components(ssn_graph)
    print "SSN Component Count: " + str(ssn_comp_num) + '\n'

    print "Calculating CSN Component Count.."
    csn_components = list(nx.connected_components(csn_graph))
    csn_components_graphs = nx.connected_component_subgraphs(csn_graph)
    csn_comp_num = nx.number_connected_components(csn_graph)
    print "CSN Component Count: " + str(csn_comp_num) + '\n'

    print "Calculating SSN Edgeless Nodes Count.."
    ssn_edgeless = get_edgeless_nodes(ssn_components)
    print "SSN Edgeless Nodes Count: " + str(ssn_edgeless) + '\n'

    print "Calculating CSN Edgeless Nodes Count.."
    csn_edgeless = get_edgeless_nodes(csn_components)
    print "CSN Edgeless Nodes Count: " + str(csn_edgeless) + '\n'

    print "Calculating SSN Average EC Coverage and Gini-Simpson Index for " \
                            + str(iterations) \
                            + " iterations of Component Sampling.."



    ssn_avg_coverage, ssn_avg_ginisimpson = multi_ginisimpson(iterations, ssn_components, uniprot_EC, './new_ssn_headings.json', './new_ssn_identities.npy')
    # ssn_avg_coverage, ssn_avg_ginisimpson = multi_ginisimpson(iterations, ssn_components_graphs, uniprot_EC, ssn_graph)



    print "SSN Average EC Coverage: " + str(ssn_avg_coverage) + "\n"
    print "SSN Average Gini-Simpson Index: " + str(ssn_avg_ginisimpson) + "\n"


    print "Calculating CSN Average EC Coverage and Gini-Simpson Index for " \
                            + str(iterations) \
                            + " iterations of Component Sampling.."

    csn_avg_coverage, csn_avg_ginisimpson = multi_ginisimpson(iterations, csn_components, uniprot_EC, './new_csn_headings.json', './new_csn_identities.npy')
    # csn_avg_coverage, csn_avg_ginisimpson = multi_ginisimpson(iterations, csn_components_graphs, uniprot_EC, csn_graph)

    print "CSN Average EC Coverage: " + str(csn_avg_coverage) + "\n"
    print "CSN Average Gini-Simpson Index: " + str(csn_avg_ginisimpson) + "\n"


    print "Total EC Numbers: " + str(ec_num)


if __name__ == '__main__':
    main()
