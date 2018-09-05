import sys
import csv
import requests
from qiime_neotaxapi import req_name

"""
IMPORTANTE
Rodar o script na pasta na qual está o qiime_neotaxapi!

USO
python taxid_to_taxname.py <INPUT> <OUTPUT>
"""

# Load the csv data and append the SET of taxids to tax_ids
# Substituir path por sys.argv[1]
with open(sys.argv[1]) as csvin:
    reader = csv.reader(csvin, delimiter='\t')
    tax_ids = [i[0] for i in reader]
    tax_ids = [int(i) for i in tax_ids[1:]]
    print("This is your total count %s" % len(tax_ids))
    tax_ids_set = list(set([i for i in tax_ids]))
    print("This is how many different OTUs you have %s" % len(tax_ids_set))

    # Now we are running the req_name(taxid) for each taxid in tax_ids
    tax_names_set = []
    for tax_id in tax_ids_set:
        try:
            tax_name = req_name(tax_id).json()['name']
            tax_names_set.append((tax_id, tax_name))
        except:
            tax_names_set.append((tax_id, "Unassigned"))

    tax_names = []
    for taxid in tax_ids:
        name = [i[1] for i in tax_names_set if taxid == i[0]]
        tax_names.append(name)

    # Substituir path por sys.argv[2]
    with open(sys.argv[2], 'w') as csvout:
        writer = csv.writer(csvout, delimiter='\t')
        # Substituir path por sys.argv[1]
        with open(sys.argv[1]) as csvin:
            reader = csv.reader(csvin, delimiter='\t')
            ix = 0
            for row in reader:
                writer.writerow(row)
                break
            for row in reader:
                writer.writerow([tax_names[ix][0], row[1], row[2]])
                ix += 1
