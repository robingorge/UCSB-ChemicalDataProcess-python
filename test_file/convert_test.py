import csv
import json


with open('for_testing/temp_result2/test_results.json') as json_data:
    x = json.load(json_data)


    f = csv.writer(open("test.csv", "wb+"))

#save all the endpoint name in key array
    keyarray=list()
    for key,value in x[0].items():
        a=key.encode('utf-8')
        keyarray.append(a)





    # Write CSV Header, If you dont need that, remove this line
    f.writerow(keyarray)


#read all values of each component, and organize them in one row
    for i in x:
        thisone=list()
        for key,value in i.items():
            thisone.append(value)
        f.writerow(thisone)
