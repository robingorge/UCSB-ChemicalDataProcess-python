import csv
import json


with open('result_test.json') as json_data:
    x = json.load(json_data)


    f = csv.writer(open("test.csv", "wb+"))


    keyarray=list()
    for key,value in x[0].items():
        keyarray.append(key)





    # Write CSV Header, If you dont need that, remove this line
    f.writerow(keyarray)

    for i in x:
        thisone=list()
        for j in keyarray:
            thisone.append(i[j])
        f.writerow(thisone)