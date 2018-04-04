# -*- coding: utf-8 -*-
'''
Last modified on March 8, 2017

@author: Yiting Ju
'''
import csv
import json
from pprint import pprint


NUM_VEGA_ENDPOINT = 29	# number of endpoints support by the VEGA cmd;
						#   the number is used for deciding how many lines will be 
						#   skipped when the result file is read


"""
	read the vega result file, parse it, and reformat it into .JSON file.

	[
		{
			"No.": "1",
			"Id": "Molecule 1",
 			"SMILES": "c1ccccc1",
 			"BCF model (CAESAR) - ADI": "0.75",
 			...
 			...
		},
		{
			"No.": "2",
			"Id": "Molecule 2",
 			"SMILES": "CC",
 			"BCF model (CAESAR) - ADI": "0",
 			...
 			...
		},
		...
		...
		{
			...
			...
		}
	]
"""
def read_vega_result_toJSON(resultFilePath, jsonOutputPath="default"):
	with open(resultFilePath, 'rb') as csvfile:
		csvReader = csv.reader(csvfile, delimiter='\t')
		rowCounter = 0
		headers = []
		resultJsonObject = []
		for row in csvReader:
			rowCounter += 1
			itemCount = 0
			if rowCounter >= NUM_VEGA_ENDPOINT+4:	# skip the header lines (not the line of headers)
				if rowCounter == NUM_VEGA_ENDPOINT+4:	# go the line of headers
					for item in row:
						itemCount += 1
						headers.append(item)
				else:									# go to lines of results
					itemJsonObject = {}
					for item in row:
						itemCount += 1
						if item == "-" or item == "[ERROR]":	# all error cells change to "N/A"
							item = "N/A"
						itemJsonObject[headers[itemCount-1]] = item
					resultJsonObject.append(itemJsonObject)
		# resultJsonObject = json.dumps(resultJsonObject, sort_keys=True, separators=(',', ': '))
				# print len(row)
				# print row

	# write JSON to file
	if jsonOutputPath == "default":
		jsonOutputPath = resultFilePath[:-3]+"json"
	with open(jsonOutputPath, "w") as outputFile:
		json.dump(resultJsonObject, outputFile, sort_keys=True, indent= 4, separators=(',', ': '))

	# print headers
	# print resultJsonObject



def readJSON(jsonFilePath):
	with open(jsonFilePath) as jsonFile:
		jsonData = json.load(jsonFile)
		# pprint(jsonData)
	return jsonData



if __name__ == '__main__':
	print "VEGA--Parsing"
	vegaResultFilePath = "/home/awsgui/Desktop/qsar/vega_file/result_test.txt"
	read_vega_result_toJSON(vegaResultFilePath)
#print readJSON("VEGA_summary_sample.json")
