import os
import json, math
import numpy as np
import pprint
import time
#from qsar_mod import QSARmod
from multiprocessing import cpu_count
from combine_results import parse

EPI_SUITE_SAMPLE_RESULTS_JSON_FILEPATH = "/home/awsgui/Desktop/qsar/episuite_file/epibat.json"
VEGA_SAMPLE_RESULTS_JSON_FILEPATH = "/home/awsgui/Desktop/qsar/vega_file/result_test.json"
TEST_SAMPLE_RESULTS_JSON_FILEPATH = "/home/awsgui/Desktop/qsar/test_file/for_testing/temp_result2/test_results.json"
DEFAULT_JSON_OUTPUT_FILEPATH = "/home/awsgui/Desktop/qsar/QSAR_summay_sample.json"
def readJSON(jsonFilePath):
	with open(jsonFilePath) as jsonFile:
		jsonData = json.load(jsonFile)
		# pprint(jsonData)
	return jsonData


epinone=    {
        "BP  C  est": "N/A",
        "BP  C  exp": "N/A",
        "CAS": "N/A",
        "HLC  Pa-m3/mole  Bond":"N/A" ,
        "HLC  Pa-m3/mole  Group":"N/A" ,
        "HLC  Pa-m3/mole  exp":"N/A",
        "HLDegAero  hour": "N/A",
        "HLDegAir  hour":"N/A" ,
        "HLDegSed  hour": "N/A",
        "HLDegSoil  hour": "N/A",
        "HLDegSsed  hour": "N/A",
        "HLDegWater  hour": "N/A",
        "Kb_HL_pH7  days":"N/A" ,
        "Kb_HL_pH8  days": "N/A",
        "Kb_rateC  L/mol-sec": "N/A",
        "Km_10  /day": "N/A",
        "LogBCF  L/kg wet-wt  Arnot-Gobas":"N/A" ,
        "LogBCF  L/kg wet-wt  Regression": "N/A",
        "MP  C  est":"N/A" ,
        "MP  C  exp":"N/A" ,
        "MW  g/mol": "N/A",
        "Mol Formula": "N/A",
        "OH_HL  days": "N/A",
        "SMILES": "N/A",
        "VP  mmHg  est": "N/A",
        "VP  mmHg  exp":"N/A" ,
        "WS  mg/L  WATERNT  est":"N/A" ,
        "WS  mg/L  WATERNT  exp":"N/A" ,
        "WS  mg/L  WSKOW  est":"N/A" ,
        "WS  mg/L  WSKOW  exp":"N/A" ,
        "WWTair  %  10000hr":"N/A",
        "WWTair  %  Biowin/EPA":"N/A" ,
        "WWTbio  %  10000hr": "N/A",
        "WWTbio  %  Biowin/EPA": "N/A",
        "WWTremoval  %  10000hr": "N/A",
        "WWTremoval  %  Biowin/EPA": "N/A",
        "WWTslu  %  10000hr":"N/A" ,
        "WWTslu  %  Biowin/EPA": "N/A",
        "algaeChV_ecosar  mg/L": "N/A",
        "algaeEC50_96hr_ecosar  mg/L": "N/A",
        "aquaTox_acute  unitless": "N/A",
        "bioHC_HL  days": "N/A",
        "bio_HL  days": "N/A",
        "biodeg_MITIlinear  unitless":"N/A" ,
        "biodeg_MITInonlinear  unitless": "N/A",
        "biodeg_anaerobic  unitless": "N/A",
        "biodeg_linear  unitless":"N/A" ,
        "biodeg_nonlinear  unitless": "N/A",
        "biodeg_primary  unitless": "N/A",
        "biodeg_ready  unitless":"N/A" ,
        "biodeg_ultimate  unitless":"N/A" ,
        "biotrans_HL  days":"N/A" ,
        "dmChV_ecosar  mg/L":"N/A" ,
        "dmLC50_48hr_ecosar  mg/L":"N/A" ,
        "earthworm_14day_ecosar  mg/L":"N/A" ,
        "fishChVSW_ecosar  mg/L":"N/A" ,
        "fishChV_ecosar  mg/L":"N/A" ,
        "fishLC50SW_96hr_ecosar  mg/L":"N/A",
        "fishLC50_96hr_ecosar  mg/L":"N/A" ,
        "kAerAir  m3/ug  Koa":"N/A" ,
        "kAerAir  m3/ug  Mackay":"N/A" ,
        "kAirWater  unitless":"N/A",
        "kNO3  cm3/molecule-sec": "N/A",
        "kO3  cm3/molecule-sec": "N/A",
        "kOH  cm3/molecule-sec": "N/A",
        "kOctAir  unitless  est": "N/A",
        "kOctAir  unitless  exp": "N/A",
        "kOctWater  unitless  est":"N/A" ,
        "kOctWater  unitless  exp": "N/A",
        "kOrgWater  L/kg  Kow": "N/A",
        "kOrgWater  L/kg  MCI": "N/A",
        "kOrgWater  L/kg  exp": "N/A",
        "shrimpLC50_96hr_ecosar  mg/L": "N/A",
        "shrimpSWChV_ecosar  mg/L": "N/A"
    }




# empty TEST json component
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


#empty vega component
veganone={
        "BCF model (CAESAR) - ADI": "N/A",
        "BCF model (CAESAR) - assessment": "N/A",
        "BCF model (CAESAR) - experimental value": "N/A",
        "BCF model (CAESAR) - prediction [log(L/kg)]": "N/A",
        "BCF model (KNN/Read-Across) - ADI": "N/A",
        "BCF model (KNN/Read-Across) - assessment": "N/A",
        "BCF model (KNN/Read-Across) - experimental value": "N/A",
        "BCF model (KNN/Read-Across) - prediction [log(L/kg)]": "N/A",
        "BCF model (Meylan) - ADI": "N/A",
        "BCF model (Meylan) - assessment": "N/A",
        "BCF model (Meylan) - experimental value": "N/A",
        "BCF model (Meylan) - prediction [log(L/kg)]": "N/A",
        "Carcinogenicity model (CAESAR) - ADI": "N/A",
        "Carcinogenicity model (CAESAR) - assessment": "N/A",
        "Carcinogenicity model (CAESAR) - experimental value": "N/A",
        "Carcinogenicity model (CAESAR) - prediction": "N/A",
        "Carcinogenicity model (IRFMN/Antares) - ADI": "N/A",
        "Carcinogenicity model (IRFMN/Antares) - assessment": "N/A",
        "Carcinogenicity model (IRFMN/Antares) - experimental value": "N/A",
        "Carcinogenicity model (IRFMN/Antares) - prediction": "N/A",
        "Carcinogenicity model (IRFMN/ISSCAN-CGX) - ADI": "N/A",
        "Carcinogenicity model (IRFMN/ISSCAN-CGX) - assessment": "N/A",
        "Carcinogenicity model (IRFMN/ISSCAN-CGX) - experimental value": "N/A",
        "Carcinogenicity model (IRFMN/ISSCAN-CGX) - prediction": "N/A",
        "Carcinogenicity model (ISS) - ADI": "N/A",
        "Carcinogenicity model (ISS) - assessment": "N/A",
        "Carcinogenicity model (ISS) - experimental value": "N/A",
        "Carcinogenicity model (ISS) - prediction": "N/A",
        "Daphnia Magna LC50 48h (DEMETRA) - ADI": "N/A",
        "Daphnia Magna LC50 48h (DEMETRA) - assessment": "N/A",
        "Daphnia Magna LC50 48h (DEMETRA) - experimental value": "N/A",
        "Daphnia Magna LC50 48h (DEMETRA) - prediction [-log(mol/l)]": "N/A",
        "Daphnia Magna LC50 48h (EPA) - ADI": "N/A",
        "Daphnia Magna LC50 48h (EPA) - assessment": "N/A",
        "Daphnia Magna LC50 48h (EPA) - experimental value": "N/A",
        "Daphnia Magna LC50 48h (EPA) - prediction [-log(mol/l)]": "N/A",
        "Developmental Toxicity model (CAESAR) - ADI": "N/A",
        "Developmental Toxicity model (CAESAR) - assessment": "N/A",
        "Developmental Toxicity model (CAESAR) - experimental value": "N/A",
        "Developmental Toxicity model (CAESAR) - prediction": "N/A",
        "Developmental/Reproductive Toxicity library (PG) - ADI": "N/A",
        "Developmental/Reproductive Toxicity library (PG) - assessment": "N/A",
        "Developmental/Reproductive Toxicity library (PG) - experimental value": "N/A",
        "Developmental/Reproductive Toxicity library (PG) - prediction": "N/A",
        "Estrogen Receptor Relative Binding Affinity model (IRFMN) - ADI": "N/A",
        "Estrogen Receptor Relative Binding Affinity model (IRFMN) - assessment": "N/A",
        "Estrogen Receptor Relative Binding Affinity model (IRFMN) - experimental value": "N/A",
        "Estrogen Receptor Relative Binding Affinity model (IRFMN) - prediction": "N/A",
        "Estrogen Receptor-mediated effect (IRFMN/CERAPP) - ADI": "N/A",
        "Estrogen Receptor-mediated effect (IRFMN/CERAPP) - assessment": "N/A",
        "Estrogen Receptor-mediated effect (IRFMN/CERAPP) - experimental value": "N/A",
        "Estrogen Receptor-mediated effect (IRFMN/CERAPP) - prediction": "N/A",
        "Fathead Minnow LC50 96h (EPA) - ADI": "N/A",
        "Fathead Minnow LC50 96h (EPA) - assessment": "N/A",
        "Fathead Minnow LC50 96h (EPA) - experimental value": "N/A",
        "Fathead Minnow LC50 96h (EPA) - prediction [-log(mol/l)]": "N/A",
        "Fish Acute (LC50) Toxicity classification (SarPy/IRFMN) - ADI": "N/A",
        "Fish Acute (LC50) Toxicity classification (SarPy/IRFMN) - assessment": "N/A",
        "Fish Acute (LC50) Toxicity classification (SarPy/IRFMN) - experimental value": "N/A",
        "Fish Acute (LC50) Toxicity classification (SarPy/IRFMN) - prediction": "N/A",
        "Fish Acute (LC50) Toxicity model (KNN/Read-Across) - ADI": "N/A",
        "Fish Acute (LC50) Toxicity model (KNN/Read-Across) - assessment": "N/A",
        "Fish Acute (LC50) Toxicity model (KNN/Read-Across) - experimental value": "N/A",
        "Fish Acute (LC50) Toxicity model (KNN/Read-Across) - prediction [-log(mg/L)]": "N/A",
        "Fish Acute (LC50) Toxicity model (NIC) - ADI": "N/A",
        "Fish Acute (LC50) Toxicity model (NIC) - assessment": "N/A",
        "Fish Acute (LC50) Toxicity model (NIC) - experimental value": "N/A",
        "Fish Acute (LC50) Toxicity model (NIC) - prediction [log(1/(mmol/L))]": "N/A",
        "Id": "Molecule 1",
        "LogP model (ALogP) - ADI": "N/A",
        "LogP model (ALogP) - assessment": "N/A",
        "LogP model (ALogP) - experimental value": "N/A",
        "LogP model (ALogP) - prediction": "N/A",
        "LogP model (MLogP) - ADI": "N/A",
        "LogP model (MLogP) - assessment": "N/A",
        "LogP model (MLogP) - experimental value": "N/A",
        "LogP model (MLogP) - prediction": "N/A",
        "LogP model (Meylan/Kowwin) - ADI": "N/A",
        "LogP model (Meylan/Kowwin) - assessment": "N/A",
        "LogP model (Meylan/Kowwin) - experimental value": "N/A",
        "LogP model (Meylan/Kowwin) - prediction": "N/A",
        "Mutagenicity (Ames test) model (CAESAR) - ADI": "N/A",
        "Mutagenicity (Ames test) model (CAESAR) - assessment": "N/A",
        "Mutagenicity (Ames test) model (CAESAR) - experimental value": "N/A",
        "Mutagenicity (Ames test) model (CAESAR) - prediction": "N/A",
        "Mutagenicity (Ames test) model (ISS) - ADI": "N/A",
        "Mutagenicity (Ames test) model (ISS) - assessment": "N/A",
        "Mutagenicity (Ames test) model (ISS) - experimental value": "N/A",
        "Mutagenicity (Ames test) model (ISS) - prediction": "N/A",
        "Mutagenicity (Ames test) model (KNN/Read-Across) - ADI": "N/A",
        "Mutagenicity (Ames test) model (KNN/Read-Across) - assessment": "N/A",
        "Mutagenicity (Ames test) model (KNN/Read-Across) - experimental value": "N/A",
        "Mutagenicity (Ames test) model (KNN/Read-Across) - prediction": "N/A",
        "Mutagenicity (Ames test) model (SarPy/IRFMN) - ADI": "N/A",
        "Mutagenicity (Ames test) model (SarPy/IRFMN) - assessment": "N/A",
        "Mutagenicity (Ames test) model (SarPy/IRFMN) - experimental value": "N/A",
        "Mutagenicity (Ames test) model (SarPy/IRFMN) - prediction": "N/A",
        "No.": "1",
        "Persistence (sediment) model (IRFMN) - ADI": "N/A",
        "Persistence (sediment) model (IRFMN) - assessment": "N/A",
        "Persistence (sediment) model (IRFMN) - experimental value": "N/A",
        "Persistence (sediment) model (IRFMN) - prediction": "N/A",
        "Persistence (soil) model (IRFMN) - ADI": "N/A",
        "Persistence (soil) model (IRFMN) - assessment": "N/A",
        "Persistence (soil) model (IRFMN) - experimental value": "N/A",
        "Persistence (soil) model (IRFMN) - prediction": "N/A",
        "Persistence (water) model (IRFMN) - ADI": "N/A",
        "Persistence (water) model (IRFMN) - assessment": "N/A",
        "Persistence (water) model (IRFMN) - experimental value": "N/A",
        "Persistence (water) model (IRFMN) - prediction": "N/A",
        "Ready Biodegradability model (IRFMN) - ADI": "N/A",
        "Ready Biodegradability model (IRFMN) - assessment": "N/A",
        "Ready Biodegradability model (IRFMN) - experimental value": "N/A",
        "Ready Biodegradability model (IRFMN) - prediction": "N/A",
        "Remarks": "N/A",
        "SMILES": "N/A",
        "Skin Sensitization model (CAESAR) - ADI": "N/A",
        "Skin Sensitization model (CAESAR) - assessment": "N/A",
        "Skin Sensitization model (CAESAR) - experimental value": "N/A",
        "Skin Sensitization model (CAESAR) - prediction": "N/A"}



# smile: string, epi,vega,test: true and false switch
def switch(smile,epi,vega,test,testopt=1):
	import os 
	dir_path = os.path.dirname(os.path.realpath(__file__))
	print(dir_path)
	text_file = open(os.path.join(dir_path, "vega_file/source_test.txt"), "w")	
	text_file.write(smile+"\n")
	text_file.close()

	text_file = open(os.path.join(dir_path, "test_file/for_testing/smiles.txt"), "w")
	text_file.write(smile+"\n")
	text_file.close()

	text_file = open(os.path.join(dir_path, "episuite_file/epi_smiles.txt"), "w")
	# place holder for batch mode	
	text_file.write("CC\n"+smile+"\n")
	text_file.close()
	
	print(epi,vega,test)

	if epi:
		# run sikulix script to operate epi
		#epi = QSARmod()
		#epi.run(input_hash={"smiles_in":smile})
		epi_time = time.time()
		#os.system("/home/awsgui/Desktop/sikulix/runsikulix -r /home/awsgui/Desktop/qsar/sikuli_scripts/epi_script.sikuli")
		os.system("/home/awsgui/Desktop/qsar/sikulix/runsikulix -r /home/awsgui/Desktop/qsar/sikuli_scripts/call_epi.sikuli")		
		os.system("python " +dir_path+ "/episuite_file/parse_episuite.py")
		#os.system("rm "+dir_path+"/episuite_file/epibat.out")
		print("EPI used {} seconds to complete.".format(time.time()-epi_time))
		#pass
	else:
		currentepi=epinone
		currentepi["SMILES"]=smile

		resultJsonObject=[currentepi]

		jsonOutputPath = os.path.join(dir_path,"episuite_file/epibat.json")
		with open(jsonOutputPath, "w") as outputFile:
			json.dump(resultJsonObject, outputFile,
					sort_keys=True, indent= 4, separators=(',', ': '))
	
	#vega switch to turn on or off
	if vega:
		vega_time = time.time()
		#os.system("java -jar ./vega_file/VEGA_CMD/VEGA-CLI.jar -script ./vega_file/script_allModule_test")
		os.system("java -jar {0}/vega_file/VEGA_CMD/VEGA-CLI.jar -script {1}/vega_file/script_shaoyi".format(dir_path,dir_path))
		os.system("python " +dir_path+ "/vega_file/call_parse_vega.py")
		print("VEGA used {} seconds to complete.".format(time.time()-vega_time))
		#print("{} process used".format(cpu_count()))
	else:
        #create the empty vage component if switch is off
		currentvega=veganone
		currentvega["SMILES"]=smile

		resultJsonObject = [currentvega]
		
        #output the result
		jsonOutputPath = os.path.join(dir_path,"vega_file/result_test.json")
		with open(jsonOutputPath, "w") as outputFile:
			json.dump(resultJsonObject, outputFile,
					sort_keys=True, indent= 4, separators=(',', ': '))


    #test switch to turn on or off
	test_time = time.time()
	if test:
		try:
			os.system("rm -rf /test_file/for_testing/temp_result2")
		except Exception:
			pass
		os.system("python " +dir_path+ "/test_file/call_parse_test.py "+str(testopt))
		#os.system("rm -rf /test_file/for_testing/temp_result2")
		print("TEST used {} seconds to complete.".format(time.time()-test_time))
		print("{} process used".format(cpu_count()))
	else:
    #create the empty test component if switch is off
		currenttest={}

		for a in TEST_Headers:
			currenttest[a]="N/A"

		currenttest["Smiles"]=smile

		resultJsonObject = [currenttest]

        #output the result
		jsonOutputPath = os.path.join(dir_path,"test_file/for_testing/temp_result2/test_results.json")
		with open(jsonOutputPath, "w") as outputFile:
			json.dump(resultJsonObject, outputFile,
					sort_keys=True, indent= 4, separators=(',', ': '))


	#os.system("python parsing.py")

	epiJSON = readJSON(EPI_SUITE_SAMPLE_RESULTS_JSON_FILEPATH)
	vegaJSON = readJSON(VEGA_SAMPLE_RESULTS_JSON_FILEPATH)
	testJSON = readJSON(TEST_SAMPLE_RESULTS_JSON_FILEPATH)
	outputFilePath = DEFAULT_JSON_OUTPUT_FILEPATH
	qsar_dict = parse(epiJSON,vegaJSON,testJSON,outputFilePath)
	#print(qsar_dict)
	return qsar_dict

if __name__ == '__main__':
	aaa="CC(=O)OC(CC(=O)O)C[N+](C)(C)C\nc1cc(cc(c1)O)CO\nCC(=CCCl)C\nC(CSSCCC(=O)OCC(CO)O)C(=O)OCC(CO)O\nC(CSCCC(=O)OCC(CO)O)C(=O)OCC(CO)O\nC[Sn+3].C(C[S-])C(=O)OCC(C(C(C(CO)O)O)O)O.C(C[S-])C(=O)OCC(C(C(C(CO)O)O)O)O.C(C[S-])C(=O)OCC(C(C(C(CO)O)O)O)O\nC(CS)C(=O)OCC(C(C(C(CO)O)O)O)O\nC(CS)C(=O)OCC(C(C(C(COC(=O)CCS)O)O)O)O\nCCOC(C)OCCC(C)CCC=C(C)C\nCCCCCCCCCCCCCCCOCCCNC(=O)C(CC(=O)[O-])S(=O)(=O)[O-].[Na+].[Na+]\nCCCCCCCCCCCCCCCOCCCNC(=O)C(CC(=O)O)S(=O)(=O)O"
	#switch("C(Cl)Cl",True,True,False)
	#testopt, 1:all,0:density and orat
	test_opt = 1
	#switch("C(C)(C1C(C)CCCC1)CC",True,True,True,test_opt)
	#switch("c1ccc2c(c1)ccc3c2ccc4c3cc5ccc6c7ccccc7cc8c6c5c4cc8",False,False,True,test_opt)
	switch("C(Cl)Cl",True,False,False,0)


