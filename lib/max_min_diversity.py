import numpy as np
from .data_prep import initialise_matrix, initialise_headings, get_matrix_min

def greedy_min_max_alg(dist, headings, subset, k, stochastic=False):

        while len(subset) < k:

            min_val = 10
            min_ind = 0

            for i in range(0, len(dist)):

                if i in subset:
                    continue

                rand = np.random.randint(0,10000)

                max_val = 0

                # print [dist[i,j] for j in subset]

                for j in subset:
                    if dist[i,j] > max_val:
                        # print dist[i,j]
                        max_val = dist[i,j]
                # print 'YAY'
                # max_val = np.nanmax(dist[i])

                if max_val < min_val:

                    min_val = max_val
                    min_ind = i
                    # print min_val

            # print "ADDED %s" % (headings[min_ind])

            subset += [min_ind]
            subset = list(set(subset))

        return subset



def compute_diverse_subset(dist_file, heading_file, k, stochastic=False):

    subset = []

    dist = initialise_matrix(dist_file)

    headings = initialise_headings(heading_file)

    min = get_matrix_min(dist)

    subset += [min[0], min[1]]

    # subset += [np.random.randint(0,241)]
    #
    # subset += [np.random.randint(0,241)]

    subset = greedy_min_max_alg(dist, headings, subset, k, stochastic)

    binary = []

    for i in range(0, len(headings)):
        if i in subset:
            binary += [1]
        else:
            binary += [0]

    subset = sorted([headings[x] for x in subset])

    # print subset

    return subset, binary
