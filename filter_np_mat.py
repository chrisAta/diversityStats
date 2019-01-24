
import numpy as np
import json
from data_prep import initialise_headings, initialise_matrix

mat_path = './sdr142_csn_identities.npy'
head_path = './sdr142_csn_headings.json'
filter_list_path = './sdr142_filter_list.txt'

new_mat_path = './newsdr142_csn_identities.npy'
new_head_path = './newsdr142_csn_headings.json'

mat = initialise_matrix(mat_path)
head = initialise_headings(head_path)

fr = open(filter_list_path, 'r')
filter_list = fr.readlines()
filter_list = list(set([line.strip() for line in filter_list]))


print filter_list
filter_indices = [head.values().index(x) for x in filter_list]
print filter_indices


mat = np.delete(mat, filter_indices, 0)
mat = np.delete(mat, filter_indices, 1)

[head.pop(x) for x in filter_indices]
new_head = {}

head_count = 0

for key in sorted(head.keys()):
    new_head[head_count] = head[key]
    head_count += 1

np.save(new_mat_path, mat)

with open(new_head_path, 'w') as outfile:
    json.dump(new_head.values(), outfile)
