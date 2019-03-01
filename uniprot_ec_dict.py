
def uniprot_ec_dict(tab_file, SDR=1):

    fr = open(tab_file, 'r')
    fr.next()
    id_to_ec = {}
    ec_to_ids = {}

    for line in fr:

        line = line.strip()
        temp_array = line.split('\t')
        id = temp_array[0]

        if SDR == 2:
            ec = temp_array[-1]
        else:
            ec = temp_array[3]

        if ec not in ec_to_ids:
            ec_to_ids[ec] = [id]

        else:
            ec_to_ids[ec].append(id)

        id_to_ec[id] = ec

    return id_to_ec, ec_to_ids
