import csv
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

with open('QSAR_summay_sample.json') as json_data:
    x = json.load(json_data)


    f = csv.writer(open("test.csv", "wb+"))


    keyarray=list()
    key2array=list()
    for key,value in x[0].items():
        keyarray.append(key)
        fl=0

        if key=="CAS" or key=="No." or key=="Smiles":
            key2array.append(" ")
        elif len(value)>1:
            for k,v in value.items():
                key2array.append(k)
                if fl<0:
                    keyarray.append(" ")
                fl=fl-1





    # Write CSV Header, If you dont need that, remove this line
    f.writerow(keyarray)
    f.writerow(key2array)
    # for i in x:
    #     thisone=list()
    #     for j in keyarray:
    #         thisone.append(i[j])
    #     f.writerow(thisone)

    for i in x:
        thisone=list()
        for key,value in i.items():
            if key=="CAS" or key=="No." or key=="Smiles":
                thisone.append(value)
            else:
                if value!=None:
                    for k,v in value.items():
                        thisone.append(v)
                else:
                    for k,v in x[0][key].items():
                        thisone.append(" ")
        f.writerow(thisone)





