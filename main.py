
from sifToNX import sifToNX
from gini_simpson import gini_simpson_dict, gini_simpson_value

def uniprot_EC_dict(tab_file):

    fr = open(tab_file, 'r')
    temp_dict = {}

    for line in fr:

        line = line.strip()
        temp_array = line.split('\t')
        id = temp_array[0]
        ec = temp_array[3]

        temp_dict[id] = ec

    return temp_dict


def main():

    ssn_file = './examples/ssn_transIII_n50.sif'
    csn_file = './examples/coev_graph_0_41.sif'

    tab_file = './transaminases.tab'

    ssn_graph = sifToNX(ssn_file)
    csn_graph = sifToNX(csn_file)

    uniprot_EC = uniprot_EC_dict(tab_file)

    print uniprot_EC

if __name__ == '__main__':
    main()
