

def gini_simpson_dict(key_subset, sig_dict):

    p_dict = {}

    for key in key_subset:

        # print key_subset
        sig = str(sig_dict[key])

        if sig in p_dict.keys():
            p_dict[sig] += 1.0
        else:
            p_dict[sig] = 1.0

    max = len(key_subset)

    for key, value in p_dict.items():
        p_dict[key] = (value/max)**2
        # print key, value
    return p_dict

def gini_simpson_value(gini_simps_dict):

    val = 1 - sum(gini_simps_dict.values())

    return val
