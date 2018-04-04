# -*- coding: utf-8 -*-
'''
Last modified on March 8, 2017

@author: Yiting Ju
'''
import csv
import sys
import inspect
import json
from multiprocessing import Pool,cpu_count
import os
import shutil
from subprocess import Popen

#from TESTHeaderRow import TEST_Headers 
#from TESTHeaderRow import TEST_Headers_New



#The two arrays import from the TESTHeaderRow, is for the json output.
TEST_Headers_New = [
    'Oral rat LD50  Exp_Value:-Log10(mol/kg)  HC',
    'Oral rat LD50  Pred_Value:-Log10(mol/kg)  HC',
    'Oral rat LD50  Exp_Value:mg/kg  HC',
    'Oral rat LD50  Pred_Value:mg/kg  HC',
    'Oral rat LD50  Exp_Value:-Log10(mol/kg)  FDA',
    'Oral rat LD50  Pred_Value:-Log10(mol/kg)  FDA',
    'Oral rat LD50  Exp_Value:mg/kg  FDA',
    'Oral rat LD50  Pred_Value:mg/kg  FDA',
    'Oral rat LD50  Exp_Value:-Log10(mol/kg)  NN',
    'Oral rat LD50  Pred_Value:-Log10(mol/kg)  NN',
    'Oral rat LD50  Exp_Value:mg/kg  NN',
    'Oral rat LD50  Pred_Value:mg/kg  NN',
    'Oral rat LD50  Exp_Value:-Log10(mol/kg)  C',
    'Oral rat LD50  Pred_Value:-Log10(mol/kg)  C',
    'Oral rat LD50  Exp_Value:mg/kg  C',
    'Oral rat LD50  Pred_Value:mg/kg  C',
    'Density  Exp_Value:g/cm\xc2\xb3  HC',
    'Density  Pred_Value:g/cm\xc2\xb3  HC',
    'Density  Exp_Value:g/cm\xc2\xb3  FDA',
    'Density  Pred_Value:g/cm\xc2\xb3  FDA',
    'Density  Exp_Value:g/cm\xc2\xb3  NN',
    'Density  Pred_Value:g/cm\xc2\xb3  NN',
    'Density  Exp_Value:g/cm\xc2\xb3  GC',
    'Density  Pred_Value:g/cm\xc2\xb3  GC',
    'Density  Exp_Value:g/cm\xc2\xb3  C',
    'Density  Pred_Value:g/cm\xc2\xb3  C',
]





TEST_Headers = [
    'Fathead minnow LC50 (96 hr)  Exp_Value:-Log10(mol/L)',
    'Fathead minnow LC50 (96 hr)  Pred_Value:-Log10(mol/L)',
    'Fathead minnow LC50 (96 hr)  Exp_Value:mg/L',
    'Fathead minnow LC50 (96 hr)  Pred_Value:mg/L',
    'Daphnia magna LC50 (48 hr)  Exp_Value:-Log10(mol/L)',
    'Daphnia magna LC50 (48 hr)  Pred_Value:-Log10(mol/L)',
    'Daphnia magna LC50 (48 hr)  Exp_Value:mg/L',
    'Daphnia magna LC50 (48 hr)  Pred_Value:mg/L',
    'T. pyriformis IGC50 (48 hr)  Exp_Value:-Log10(mol/L)',
    'T. pyriformis IGC50 (48 hr)  Pred_Value:-Log10(mol/L)',
    'T. pyriformis IGC50 (48 hr)  Exp_Value:mg/L',
    'T. pyriformis IGC50 (48 hr)  Pred_Value:mg/L',
    'Oral rat LD50  Exp_Value:-Log10(mol/kg)  HC',
    'Oral rat LD50  Pred_Value:-Log10(mol/kg)  HC',
    'Oral rat LD50  Exp_Value:mg/kg  HC',
    'Oral rat LD50  Pred_Value:mg/kg  HC',
    'Oral rat LD50  Exp_Value:-Log10(mol/kg)  FDA',
    'Oral rat LD50  Pred_Value:-Log10(mol/kg)  FDA',
    'Oral rat LD50  Exp_Value:mg/kg  FDA',
    'Oral rat LD50  Pred_Value:mg/kg  FDA',
    'Oral rat LD50  Exp_Value:-Log10(mol/kg)  NN',
    'Oral rat LD50  Pred_Value:-Log10(mol/kg)  NN',
    'Oral rat LD50  Exp_Value:mg/kg  NN',
    'Oral rat LD50  Pred_Value:mg/kg  NN',
    'Oral rat LD50  Exp_Value:-Log10(mol/kg)  C',
    'Oral rat LD50  Pred_Value:-Log10(mol/kg)  C',
    'Oral rat LD50  Exp_Value:mg/kg  C',
    'Oral rat LD50  Pred_Value:mg/kg  C',
    'Bioaccumulation factor  Exp_Value:Log10',
    'Bioaccumulation factor  Pred_Value:Log10',
    'Bioaccumulation factor  Exp_Value:',
    'Bioaccumulation factor  Pred_Value:',
    'Developmental Toxicity  Exp_Value',
    'Developmental Toxicity  Pred_Value',
    'Developmental Toxicity  Exp_Result',
    'Developmental Toxicity  Pred_Result',
    'Mutagenicity  Exp_Value',
    'Mutagenicity  Pred_Value',
    'Mutagenicity  Exp_Result',
    'Mutagenicity  Pred_Result',
    'Normal boiling point  Exp_Value:\xc2\xb0C',
    'Normal boiling point  Pred_Value:\xc2\xb0C',
    'Vapor pressure at 25\xc2\xb0C  Exp_Value:Log10(mmHg)',
    'Vapor pressure at 25\xc2\xb0C  Pred_Value:Log10(mmHg)',
    'Vapor pressure at 25\xc2\xb0C  Exp_Value:mmHg',
    'Vapor pressure at 25\xc2\xb0C  Pred_Value:mmHg',
    'Melting point  Exp_Value:\xc2\xb0C',
    'Melting point  Pred_Value:\xc2\xb0C',
    'Flash point  Exp_Value:\xc2\xb0C',
    'Flash point  Pred_Value:\xc2\xb0C',
    'Density  Exp_Value:g/cm\xc2\xb3  HC',
    'Density  Pred_Value:g/cm\xc2\xb3  HC',
    'Density  Exp_Value:g/cm\xc2\xb3  FDA',
    'Density  Pred_Value:g/cm\xc2\xb3  FDA',
    'Density  Exp_Value:g/cm\xc2\xb3  NN',
    'Density  Pred_Value:g/cm\xc2\xb3  NN',
    'Density  Exp_Value:g/cm\xc2\xb3  GC',
    'Density  Pred_Value:g/cm\xc2\xb3  GC',
    'Density  Exp_Value:g/cm\xc2\xb3  C',
    'Density  Pred_Value:g/cm\xc2\xb3  C',
    'Surface tension at 25\xc2\xb0C  Exp_Value:dyn/cm',
    'Surface tension at 25\xc2\xb0C  Pred_Value:dyn/cm',
    'Thermal conductivity at 25\xc2\xb0C  Exp_Value:mW/mK',
    'Thermal conductivity at 25\xc2\xb0C  Pred_Value:mW/mK',
    'Viscosity at 25\xc2\xb0C  Exp_Value:Log10(cP)',
    'Viscosity at 25\xc2\xb0C  Pred_Value:Log10(cP)',
    'Viscosity at 25\xc2\xb0C  Exp_Value:cP',
    'Viscosity at 25\xc2\xb0C  Pred_Value:cP',
    'Water solubility at 25\xc2\xb0C  Exp_Value:-Log10(mol/L)',
    'Water solubility at 25\xc2\xb0C  Pred_Value:-Log10(mol/L)',
    'Water solubility at 25\xc2\xb0C  Exp_Value:mg/L',
    'Water solubility at 25\xc2\xb0C  Pred_Value:mg/L'
]



TEST_Endpoints = [
    "Fathead minnow LC50 (96 hr)",
    "Daphnia magna LC50 (48 hr)",
    "T. pyriformis IGC50 (48 hr)",
    "Oral rat LD50",
    "Bioaccumulation factor",
    "Developmental Toxicity",
    "Mutagenicity",
    "Normal boiling point",
    "Vapor pressure at 25°C",
    "Melting point",
    "Flash point",
    "Density",
    "Surface tension at 25°C",
    "Thermal conductivity at 25°C",
    "Viscosity at 25°C",
    "Water solubility at 25°C"
]







DEFAULT_FILE_TYPE = 2	# smiles
default_method = 10
DEFAULT_ENDPOINT_LIST = [1, 2, 3, 4, 5, 6, 7, 20, 21, 22, 23, 24, 25, 26, 27, 28]
DEFAULT_flag="1"

# get the directory where this "Call_TEST.py" file is
CLASS_DIRECTORY = os.path.dirname(os.path.abspath(
	inspect.getfile(inspect.currentframe()))
)
#TEST_JAR_FOLDER_PATH = "/home/yiting/Dropbox/Spring2016/CLiCC/ModuleIntegration/clicc-flask-master/modules/qsar/batch_files/TEST_CMD"
#TEST_JAR_FOLDER_PATH = "/Users/lizehao/desktop/general/test_file/TEST_CMD"
TEST_JAR_FOLDER_PATH = "/home/awsgui/Desktop/qsar/test_file/TEST_CMD"
#TEST_JAR_FOLDER_PATH = os.path.join(CLASS_DIRECTORY, "TEST_CMD")
PROCESSES_USED = cpu_count()*2+1



'''
	Call the TEST to get QSAR of all endpoints for a batch of test_chemicals
	  The results are categorized for each chemicals in a single folder
	  Everything will be summarized in a single summary.json
	inputFilePath: Path to a .smi file of a list of chemicals' smiles (one smiles for each line)
	outputFolderPath: Path to a folder where the result will be stored
	fileType: 1 for SDF; 2 for SMILES (.smi); [We use 2]
	method: 10 for Consensus (density and oral rat need 1, 2, 3, 4, 5)
	endpointList: The list of endpoints to be calculated

	Folder structure:
		cmd_results
		-smile1
		|-result_endpoint_1.csv
		|-result_endpoint_2.csv
		|-...
		|-summary.csv
		-smile2
		|-...
		...
		...
		-summary.json

	summary.json:
	[
		{
			"No.": "1",
 			"SMILES": "OCCOCCOCCOCCOCCOCC(C)OCC(C)OCC(C)OCC(C)OCC(C)O",
 			"Bioaccumulation factor  Exp_Value:dyn/cm": "N/A",
        	"Bioaccumulation factor  Pred_Value:dyn/cm": "7204.49",
 			...
 			...
		},
		{
			"No.": "2",
 			"SMILES": "KO",
 			"Bioaccumulation factor  Exp_Value:dyn/cm": "N/A",
        	"Bioaccumulation factor  Pred_Value:dyn/cm": "N/A",
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
'''
def TEST_batch_allEndpoints(testJarFilePath, inputFilePath, outputFolderPath, 
					fileType = DEFAULT_FILE_TYPE, endpointList = DEFAULT_ENDPOINT_LIST):
	if not os.path.exists(outputFolderPath):
			os.makedirs(outputFolderPath)
	folderPath = os.path.dirname(inputFilePath)
	# print folderPath   	# ./test_chemicals/
	numSmiles, smilesList = listToFiles(inputFilePath, os.path.join(folderPath, "tempSMIFolder"))
	testResultList = []
	for i in range(numSmiles):
		tempInputPath = os.path.join(folderPath, "tempSMIFolder", "smile_" + str(i+1) + ".smi")
		outputFolderPathIns = os.path.join(outputFolderPath, "smile" + str(i+1))
		if not os.path.exists(outputFolderPathIns):
			os.makedirs(outputFolderPathIns)
		TEST_allEndpoints(testJarFilePath, tempInputPath,
							outputFolderPathIns, fileType, endpointList)
		resultList = organizeResultToSingleCSV(outputFolderPathIns, 
									os.path.join(outputFolderPathIns, "summary.csv"),
									endpointList)
		testResultList.append(resultList)
	writeJSONSummary(testResultList, smilesList, outputFolderPath)
	shutil.rmtree(os.path.join(folderPath, "tempSMIFolder"))
	print "temp folder " + os.path.join(folderPath, "tempSMIFolder") + " is removed"
	print "[info] TEST done >>", os.path.join(outputFolderPath, "test_results.json")


"""
	Call the TEST cmd to get QSAR results for (all) endpoints in endpointList
	  note: multi-processing is employed in this function
	  Sample TEST CMD: 
	  	>>  To run the consensus method for the T. pyriformis IGC50 (48 hr) 
			  endpoint for SDF input use the following
		java -Xmx512m -cp "test.jar" ToxPredictor.Application.runTEST_From_Command_Line
		  \u201cSample_MDL_SDfile.sdf\u201d 1 \u201cresultsIGC50.txt\u201d 3 10
"""

#run all the commands in the command line, to get the results
def TEST_allEndpoints(testJarFilePath, inputFilePath, outputFolderPath, 
						fileType = DEFAULT_FILE_TYPE, endpointList = DEFAULT_ENDPOINT_LIST):
	commands = []
	for endpoint in endpointList:
		if endpoint < 10:
			endpoint = "0" + str(endpoint)
		# "Oral rat" and "Density" need methods 1,2,3,4,5
		if not(endpoint == "04" or endpoint == 24):
			if DEFAULT_flag=="1":
				method = 10
				outputFilePath = os.path.join(outputFolderPath,("result_endpoint_{0}.csv").format(endpoint))
				command = 'java -Xmx512m -cp "' + testJarFilePath + \
							'" ToxPredictor.Application.runTEST_From_Command_Line "' + \
							inputFilePath + '" ' + str(fileType) + ' "' + \
							outputFilePath + '" ' + str(endpoint) + ' ' + str(method)
				commands.append(command)
		elif endpoint == "04":
			for method in [1, 2, 4,10]:
				outputFilePath = os.path.join(outputFolderPath,
								("result_endpoint_{0}_{1}.csv").format(endpoint, method))
				command = 'java -Xmx512m -cp "' + testJarFilePath + \
					'" ToxPredictor.Application.runTEST_From_Command_Line "' + \
					inputFilePath + '" ' + str(fileType) + ' "' + \
					outputFilePath + '" ' + str(endpoint) + ' ' + str(method)
				commands.append(command)
		elif endpoint == 24:
			for method in [1, 2, 4, 5,10]:
				outputFilePath = os.path.join(outputFolderPath, 
								("result_endpoint_{0}_{1}.csv").format(endpoint, method))
				command = 'java -Xmx512m -cp "' + testJarFilePath + \
					'" ToxPredictor.Application.runTEST_From_Command_Line "' + \
					inputFilePath + '" ' + str(fileType) + ' "' + \
					outputFilePath + '" ' + str(endpoint) + ' ' + str(method)
				commands.append(command)
	# watch out the next line, which may be dangerous...			
	TEST_JAR_FOLDER_PATH = os.path.dirname(testJarFilePath)
	pool = Pool(processes = PROCESSES_USED)
	pool.map(call_popen, commands)

#call the command by one function
def call_popen(command):
	print "Calling", command
	try:
		e = Popen(
			command,
			cwd = TEST_JAR_FOLDER_PATH,
			shell = True
		)
		stdout, stderr = e.communicate()
	except IOError as (errno,strerror):
		print "I/O error({0}): {1}".format(errno, strerror)


def listToFiles(inputListFilePath, outputFolder):
	smilesList = []
	with open(inputListFilePath, 'r') as f:
		for row in f:
			smilesList.append(row)
	if not os.path.exists(outputFolder):
		os.makedirs(outputFolder)
		print "temp folder " + outputFolder + " is created"
	for i in range(len(smilesList)):
		with open(os.path.join(outputFolder, "smile_" + str(i+1) + ".smi"), 'w') as f:
			f.write(smilesList[i])
	return len(smilesList), smilesList

#combile all the result into one csv
def organizeResultToSingleCSV(smilesResultFolderPath, 
							summaryFilePath,
							endpointList = DEFAULT_ENDPOINT_LIST):
	headerRowList = []
	dataRowList = []
	for i in endpointList:
		if i != 4 and i != 24: # "Oral rat" and "Density" need methods 1,2,3,4,5
			if DEFAULT_flag=="1":
				if i < 10:
					i = "0" + str(i)
				headerRow, dataRow = readTESTResult(os.path.join(smilesResultFolderPath,"result_endpoint_" + str(i) + ".csv"))
				headerRowList.append(headerRow)
				dataRowList.append(dataRow)
		elif i == 4:
			i = "04"
			for method in [1, 2, 4,10]:
				headerRow, dataRow = readTESTResult(os.path.join(smilesResultFolderPath,
													"result_endpoint_"+str(i)+"_"+str(method)+".csv"))
				headerRowList.append(headerRow)
				dataRowList.append(dataRow)
		elif i == 24:
			i = "24"
			for method in [1, 2, 4, 5,10]:
				headerRow, dataRow = readTESTResult(os.path.join(smilesResultFolderPath,
													"result_endpoint_"+str(i)+"_"+str(method)+".csv"))
				headerRowList.append(headerRow)
				dataRowList.append(dataRow)
	with open(summaryFilePath, 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter = ',',
							quotechar= '"', quoting = csv.QUOTE_MINIMAL)
		for dataRowIns in dataRowList:
			spamwriter.writerow(dataRowIns)
	return dataRowList


def readTESTResult(resultFilePath):
	headerRow = []
	dataRow = []
	if not os.path.isfile(resultFilePath):
		return "N/A", "N/A"
	with open(resultFilePath, 'rb') as csvfile:
		csvReader = csv.reader(csvfile, delimiter='\t')
		row_count = 0
		for row in csvReader:
			if row_count == 0:
				headerRow = row[2:-1]	# the first and last row are discarded
				row_count += 1
			elif row_count == 1:
				dataRow = row[2:-1]
				row_count += 1
		if row_count != 2:
			print "error: the result file should only have two lines"
	return headerRow, dataRow


def writeJSONSummary(testResultList, smilesList, outputFolderPath):
	resultJsonObject = []
	resultCounter = 0
	for testResult in testResultList:		
		itemJsonObject = {}
		itemJsonObject["No."] = resultCounter+1
		itemJsonObject["Smiles"] = (smilesList[resultCounter]).strip()
		itemCount = 0
		for itemList in testResult:
			if DEFAULT_flag=="1":
				for item in itemList:
					itemJsonObject[TEST_Headers[itemCount]] = item
					itemCount += 1
			else:
				for item in itemList:
					itemJsonObject[TEST_Headers_New[itemCount]] = item
					itemCount += 1
		resultJsonObject.append(itemJsonObject)
		resultCounter += 1

	# write JSON to file
	jsonOutputPath = os.path.join(outputFolderPath, "test_results.json")
	with open(jsonOutputPath, "w") as outputFile:
		json.dump(resultJsonObject, outputFile,
				sort_keys=True, indent= 4, separators=(',', ': '))



if __name__ == "__main__":
	print "TEST"
	DEFAULT_flag=sys.argv[1]
	TEST_batch_allEndpoints(os.path.join(TEST_JAR_FOLDER_PATH, "TEST.jar"), 
					os.path.join(CLASS_DIRECTORY, "for_testing", "smiles.txt"),
					os.path.join(CLASS_DIRECTORY, "for_testing", "temp_result2"))
