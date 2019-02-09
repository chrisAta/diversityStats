

fr = open('./STR_TR40.sif', 'r')
fw = open('./examples/new_ssn_SDR_n40.sif', 'w')

dict = {}

for line in fr:

    line = line.strip()

    temp = line.split(' edge ')

    if len(temp) == 1:
        fw.write(line + '\n')
        continue

    for entry in temp[1].split(' '):
        fw.write(temp[0] + ' edge ' + entry + '\n')

fr.close()
fw.close()
