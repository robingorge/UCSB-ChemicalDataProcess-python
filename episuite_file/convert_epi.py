import csv
import json


with open('epibat.json') as json_data:
    x = json.load(json_data)


    f = csv.writer(open("test.csv", "wb+"))

    #save all the endpoints name into keyarray
    keyarray=list()
    for key,value in x[0].items():
        keyarray.append(key)





    # Write CSV Header, If you dont need that, remove this line
    f.writerow(keyarray)


#write values of each component, one by one, and each time print a rwo
    for i in x:
        thisone=list()
        for key,value in i.items():
            thisone.append(value)
        f.writerow(thisone)
