import requests as req
import time 

test_url = 'http://0.0.0.0:2346/qsar?smiles={}&epi=1&vega=0&test=0'
with open ('source_test.txt','rt') as fp:
    smiles_list = fp.readlines()
    for smiles in smiles_list:
        #wprint(test_url.format(smiles.strip()))
        res = req.get(test_url.format(smiles.strip()))
	if res.status_code == 500:
	    print(test_url.format(smiles.strip())) 
        print(res)
