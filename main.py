
import networkx as nx
from sifToNX import sifToNX
from gini_simpson import gini_simpson_dict, gini_simpson_value
from random import choice, sample
import max_min_diversity
from uniprot_ec_dict import *
from copy import deepcopy

# def uniprot_EC_dict(tab_file):
#
#     fr = open(tab_file, 'r')
#     fr.next()
#     id_to_ec = {}
#     ec_to_ids = {}
#
#     for line in fr:
#
#         line = line.strip()
#         temp_array = line.split('\t')
#         id = temp_array[0]
#         ec = temp_array[3]
#         # ec = temp_array[-1]
#
#         if ec not in ec_to_ids:
#             ec_to_ids[ec] = [id]
#
#         else:
#             ec_to_ids[ec].append(id)
#
#         id_to_ec[id] = ec
#
#     return id_to_ec, ec_to_ids

def sample_from_components(components, num_comp):

    # fr = open('./sdr142_filter_list.txt')
    # fr = open('./transIII_filter_list.txt')
    #
    # illegal = fr.readlines()
    # illegal = [line.strip() for line in illegal]

    temp_list = []
    i = 0
    temp_components = deepcopy(components)
    while len(temp_list) != num_comp:

            comp = choice(temp_components)

            if len(comp) == 0:
                continue

            comp_ind = temp_components.index(comp)
            temp_entry = choice(comp)
            node_ind = comp.index(temp_entry)

            temp_components[comp_ind].pop(node_ind)

            temp_list += [temp_entry]
            i += 1
    #
    # while len(temp_list) != num_comp:
    #
    #         comp = choice(temp_components)
    #         comp_ind = temp_components.index(comp)
    #         temp_entry = choice(comp)







    # while len(temp_list) != num_comp:
    #
    #     comp = choice(temp_components)
    #
    #     if len(comp) == 0:
    #         continue
    #
    #     comp_ind = temp_components.index(comp)
    #     temp_entry = choice(comp)
    #     node_ind = comp.index(temp_entry)
    #
    #     temp_components[comp_ind]
    #
    #     temp_list += [temp_entry]
    #     i += 1

    return temp_list
#
# def sample_from_components_cliques(components, num_comp):
#
#     temp_list = []
#
#     for comp in components:
#
#         max_clique = max(list(nx.find_cliques(comp)))
#         # print comp.nodes()
#         # print max_clique
#         temp_list += [choice(max_clique)]
#         # print temp_list
#         # print comp.nodes()
#     # print temp_list
#     # print len(temp_list)
#
#     return temp_list

def multi_ginisimpson(iterations, components, dict, head, mat, size, graph=None):

    avg_coverage = 0.0
    max_coverage = 0.0
    avg_value = 0.0
    max_value = 0.0
    ec_num = len(set(dict.values()))
    # ec_num = 24
    # ec_num = len(components)
    # components = [comp for comp in components if len(comp) > 1]

    for i in range(0, iterations):
        # print i
        rand_sample = sample_from_components(components, size)
        # rand_sample = sample_from_components_cliques(components, ec_num)

        # rand_sample = max_min_diversity.compute_diverse_set(mat, head, size)[0]
        # print sorted(rand_sample)
        # print len(rand_sample)

        ginisimps_dict = gini_simpson_dict(rand_sample, dict)
        ginisimps_value = gini_simpson_value(ginisimps_dict)
        avg_coverage += len(ginisimps_dict.keys())
        avg_value += ginisimps_value

        # print(sorted(ginisimps_dict.keys()))

        if len(ginisimps_dict.keys()) > max_coverage:
            max_coverage = len(ginisimps_dict.keys())

        if ginisimps_value > max_value:
            max_value = ginisimps_value

        # components = nx.connected_component_subgraphs(graph)


    # print min

    avg_coverage /= iterations
    avg_value /= iterations

    # print "MAX COVERAGE: " + str(max_coverage)
    # print "MAX GINISIMPSON VALUE: " + str(max_value)

    return avg_coverage, avg_value


def get_edgeless_nodes(components):

    count = 0

    for comp in components:
        if len(comp) == 1:
            count += 1

    return count


def ec_max_fraction(ec_to_ids, graph):

    for ec, ids in ec_to_ids.items():

        total_ids = list(set(ids + [item for x in [list(nx.all_neighbors(graph, node)) for node in ids] for item in x]))
        temp_graph = nx.subgraph(graph, total_ids)

        num_nodes = len(ids) * 1.0

        comps = list(nx.connected_components(temp_graph))

        for i in range(0, len(comps)):
            for id in comps[i]:
                if id not in ids:
                    comps[i] = [x for x in comps[i] if x != id]

        num_comp = len(comps)

        max_comp = max(comps, key=len)

        max_fraction = len(max_comp) / num_nodes

        print ec + "\t" + str(len(max_comp)) + "\t" +  str(max_fraction)


def ec_edges(ec_to_ids, graph):

    for ec, ids in ec_to_ids.items():

        # edges_num = sum([len(list(nx.all_neighbors(graph, node))) for node in ids]) / 2
        #



        print ec + "\t" + str(len(list(graph.edges(ids))))



def ec_analysis(id_to_ec, ec_to_ids, graph):

    print "MAX FRACTION: "
    ec_max_fraction(ec_to_ids, graph)
    print "\nEDGES: "
    ec_edges(ec_to_ids, graph)

    # print sorted(graph.nodes())

def rand_index(graph1, graph2):

    print list(graph1.edges())

def iterate_subset_size(iterations, components, dict, head, mat):

    max = len(dict.keys())
    ec_num = max / 20 #5% AT A TIME

    for size in range(ec_num, max, ec_num):

        avg_coverage, avg_ginisimpson = multi_ginisimpson(iterations, \
                                    components, dict, head, mat, size)

        print str(size) + "\t" + str(avg_coverage) + "\t" + str(avg_ginisimpson)
        print ""





def main():

    # ssn_file = './examples/networks/ssn_transIII_n50.gml'
    # csn_file = './examples/networks/csn_transIII_n41.sif'
    ssn_file = './examples/networks/ssn_SDR_n50.gml'
    csn_file = './examples/networks/csn_SDR_n57.sif'

    # ssn_file = './examples/networks/ssn_SDR_n40.gml'
    # csn_file = './examples/networks/coev_graph_0_41.sif'

    # ssn_file = './examples/networks/ssn_transIII_n40.gml'
    # csn_file = './examples/networks/coev_graph_0_32.sif'



    # tab_file = './examples/tables/transaminases_edited.tab.csv'
    tab_file = './examples/tables/STR_143_annotation_edited.csv'

    # ssn_graph = sifToNX(ssn_file)
    ssn_graph = nx.read_gml(ssn_file)
    csn_graph = sifToNX(csn_file)

    uniprot_EC, ec_to_ids = uniprot_ec_dict(tab_file, 2)

    ec_num = len(set(uniprot_EC.values()))
    iterations = 10000

    print "Calculating SSN Component Count.."
    ssn_components = list(nx.connected_components(ssn_graph))
    ssn_components_graphs = nx.connected_component_subgraphs(ssn_graph)
    ssn_comp_num = nx.number_connected_components(ssn_graph)
    # print "SSN Component Count: " + str(ssn_comp_num) + '\n'
    #
    # print "Calculating CSN Component Count.."
    csn_components = list(nx.connected_components(csn_graph))
    csn_components_graphs = nx.connected_component_subgraphs(csn_graph)
    csn_comp_num = nx.number_connected_components(csn_graph)
    # print "CSN Component Count: " + str(csn_comp_num) + '\n'
    #
    # print "Calculating SSN Edgeless Nodes Count.."
    # ssn_edgeless = get_edgeless_nodes(ssn_components)
    # print "SSN Edgeless Nodes Count: " + str(ssn_edgeless) + '\n'
    #
    # print "Calculating CSN Edgeless Nodes Count.."
    # csn_edgeless = get_edgeless_nodes(csn_components)
    # print "CSN Edgeless Nodes Count: " + str(csn_edgeless) + '\n'
    # #
    # print "Calculating SSN Average EC Coverage and Gini-Simpson Index for " \
    #                         + str(iterations) \
    #                         + " iterations of Component Sampling.."
    #
    #
    #
    # ssn_avg_coverage, ssn_avg_ginisimpson = multi_ginisimpson(iterations, ssn_components, uniprot_EC, './examples/max_min/trans241_ssn_headings.json', './examples/max_min/trans241_ssn_identities.npy', 24)
    # # ssn_avg_coverage, ssn_avg_ginisimpson = multi_ginisimpson(iterations, ssn_components, uniprot_EC, './newtrans241_ssn_headings.json', './newtrans241_ssn_identities.npy')
    #
    # ssn_avg_coverage, ssn_avg_ginisimpson = multi_ginisimpson(iterations, ssn_components, uniprot_EC, './examples/max_min/sdr142_ssn_headings.json', './examples/max_min/sdr142_ssn_identities.npy', ec_num)
    # # ssn_avg_coverage, ssn_avg_ginisimpson = multi_ginisimpson(iterations, ssn_components, uniprot_EC, './newsdr142_ssn_headings.json', './newsdr142_ssn_identities.npy')
    #
    # #
    # #
    # print "SSN Average EC Coverage: " + str(ssn_avg_coverage) + "\n"
    # print "SSN Average Gini-Simpson Index: " + str(ssn_avg_ginisimpson) + "\n"
    # #
    # # #
    # print "Calculating CSN Average EC Coverage and Gini-Simpson Index for " \
    #                         + str(iterations) \
    #                         + " iterations of Component Sampling.."
    #
    # csn_avg_coverage, csn_avg_ginisimpson = multi_ginisimpson(iterations, csn_components, uniprot_EC, './examples/max_min/trans241_csn_headings.json', './examples/max_min/trans241_csn_identities.npy', 24)
    # csn_avg_coverage, csn_avg_ginisimpson = multi_ginisimpson(iterations, csn_components, uniprot_EC, './newtrans241_csn_headings.json', './newtrans241_csn_identities.npy')

    # csn_avg_coverage, csn_avg_ginisimpson = multi_ginisimpson(iterations, csn_components, uniprot_EC, './examples/max_min/sdr142_csn_headings.json', './examples/max_min/sdr142_csn_identities.npy', ec_num)
    # csn_avg_coverage, csn_avg_ginisimpson = multi_ginisimpson(iterations, csn_components, uniprot_EC, './newsdr142_csn_headings.json', './newsdr142_csn_identities.npy')



    # print "CSN Average EC Coverage: " + str(csn_avg_coverage) + "\n"
    # print "CSN Average Gini-Simpson Index: " + str(csn_avg_ginisimpson) + "\n"
    #

    print "Total EC Numbers: " + str(ec_num)

    print "SSN EC Analysis: "
    ec_analysis(uniprot_EC, ec_to_ids, ssn_graph)

    print "CSN EC Analysis: "
    ec_analysis(uniprot_EC, ec_to_ids, csn_graph)

    # rand_index(ssn_graph, csn_graph)

    # iterate_subset_size(iterations, ssn_components, uniprot_EC, "./examples/max_min/sdr142_ssn_headings.json", './examples/max_min/sdr142_ssn_identities.npy')
    # iterate_subset_size(iterations, csn_components, uniprot_EC, "./examples/max_min/sdr142_csn_headings.json", './examples/max_min/sdr142_csn_identities.npy')

    # iterate_subset_size(iterations, csn_components, uniprot_EC, "./examples/max_min/trans241_csn_headings.json", './examples/max_min/trans241_csn_identities.npy')

    # iterate_subset_size(iterations, ssn_components, uniprot_EC, "./examples/max_min/trans241_ssn_headings.json", './examples/max_min/trans241_ssn_identities.npy')



if __name__ == '__main__':
    main()
