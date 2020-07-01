
from uniprot_ec_dict import uniprot_ec_dict
from max_min_diversity import compute_diverse_subset
from collections import defaultdict

#########################################

import argparse

parser = argparse.ArgumentParser(description="MDP Filler stuff") #TODO: Change desc
parser.add_argument("-a", "--annotation", help="Path to the annotation", type=str, required=True)
parser.add_argument("-hd", "--heading", help="Path to heading file", type=str, required=True)
parser.add_argument("-d", "--distance", help="Path to distance file", type=str, required=True)
parser.add_argument("-k", "--subset", help="Subset size", type=int, required=True)


args = parser.parse_args()
_ANNPATH = args.annotation
_HEADPATH = args.heading
_DISTPATH = args.distance
_K = args.subset


#########################################

def get_ec_subset(subset, ac_to_ec):

    ec_dict = defaultdict(int)

    for ac in subset:
        ec_str = ac_to_ec[ac]
        ec_lst = ec_str.split(';')

        for ec in ec_lst:
            ec_dict[ec] += 1

    return ec_dict


def main():

    ac_to_ec, ec_to_ac = uniprot_ec_dict(_ANNPATH, 2)
    ec_num = len(set(ac_to_ec.values()))

    ac_subset, binary = compute_diverse_subset(_DISTPATH, _HEADPATH, _K)
    ec_subset = get_ec_subset(ac_subset, ac_to_ec)

    print(ec_to_ac.keys())
    print(len(ec_to_ac.keys()))
    print(len(ec_subset.keys()))

    print(ec_subset)
    print(ac_subset)
    print(binary)


if __name__ == '__main__':
    main()
