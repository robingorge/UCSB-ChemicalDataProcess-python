# -*- coding: utf-8 -*-
import json, math
import numpy as np
import pprint

# 3 source location & 1 destination location
#EPI_SUITE_SAMPLE_RESULTS_JSON_FILEPATH = "/Users/lizehao/desktop/general/episuite_file/epibat.json"
#VEGA_SAMPLE_RESULTS_JSON_FILEPATH = "/Users/lizehao/desktop/general/vega_file/result_test.json"
#TEST_SAMPLE_RESULTS_JSON_FILEPATH = "/Users/lizehao/desktop/general/test_file/for_testing/temp_result2/test_results.json"
#DEFAULT_JSON_OUTPUT_FILEPATH = "/Users/lizehao/desktop/general/QSAR_summay_sample.json"
EPI_SUITE_SAMPLE_RESULTS_JSON_FILEPATH = "/home/awsgui/Desktop/qsar/episuite_file/epibat.json"
VEGA_SAMPLE_RESULTS_JSON_FILEPATH = "/home/awsgui/Desktop/qsar/vega_file/result_test.json"
TEST_SAMPLE_RESULTS_JSON_FILEPATH = "/home/awsgui/Desktop/qsar/test_file/for_testing/temp_result2/test_results.json"
DEFAULT_JSON_OUTPUT_FILEPATH = "/home/awsgui/Desktop/qsar/QSAR_summay_sample.json"




"""
	parse JSON results from three QSAR models and output results as a single JSON file
"""
def parse(epi_json, vega_json, test_json, outputFilePath):
	if not ensureSameLength(epi_json, vega_json, test_json):
		print "[error] Three JSON files have different number of chemicals"
	chemicalsJson = []
	for index in range(len(vega_json)):
		print index

		#used to parse one smile at a time
		#it reads in the information from the three files and parse them in each function
		#the index could track the same chemical in defferent files

		chemicalObj = {}

		chemicalObj["No."] = index+1
		chemicalObj["Smiles"] = epi_json[index]["SMILES"]
		print(chemicalObj["Smiles"])
		chemicalObj["CAS"] = epi_json[index]["CAS"]


		chemicalObj["aquaTox_acute"]=parse_ata_stat(epi_json,index)

		chemicalObj["MW"] = parse_mw_stat(epi_json, index)
		chemicalObj["MD"] = parse_density_stat(test_json, index)

		chemicalObj["BCF"] = parse_bcf_stat(epi_json, vega_json, index)
		#unlog the log bcf
		try:
			bcfmin=math.pow(10,chemicalObj["BCF"]["minimum"])
			bcfmax=math.pow(10,chemicalObj["BCF"]["maximum"])
			bcfavg=math.pow(10,chemicalObj["BCF"]["average"])
			chemicalObj["BCF"]["minimum"]=bcfmin
			chemicalObj["BCF"]["maximum"]=bcfmax
			chemicalObj["BCF"]["average"]=bcfavg
		except Exception:
			chemicalObj["BCF"]["minimum"]="na"
			chemicalObj["BCF"]["maximum"]="na"
			chemicalObj["BCF"]["average"]="na"		

		chemicalObj["Kow"] = parse_kow_stat(epi_json, vega_json, index)
		chemicalObj["Koc"] = parse_koc_stat(epi_json, index)
		chemicalObj["Kaw"] = parse_kaw_stat(epi_json, index)
		# ########## change
		chemicalObj["Kp"] = parse_kaerair_stat(epi_json, index)		
		chemicalObj["HL_air"] = parse_DegAir_stat(epi_json, index)
		chemicalObj["HL_water"] = parse_DegWater_stat(epi_json, index)
		chemicalObj["HL_soil"] = parse_DegSoil_stat(epi_json, index)
		chemicalObj["HL_sediment"] = parse_DegSed_stat(epi_json, index)
		chemicalObj["HL_aer"] = parse_DegAero_stat(epi_json, index)
		chemicalObj["HL_sussed"] = parse_DegSSed_stat(epi_json, index)
		#chemicalObj["kOctAir"] = parse_koa_stat(epi_json, index)
		chemicalObj["VP"] = parse_vp_stat(epi_json, test_json, index)
		chemicalObj["WS"] = parse_ws_stat(epi_json, test_json, index)
		chemicalObj["BP"] = parse_bp_stat(epi_json, test_json, index)
		chemicalObj["MP"] = parse_mp_stat(epi_json, test_json, index)

		# test only
		chemicalObj["FP"] = parse_fp_stat(test_json, index)
		chemicalObj["TC"] = parse_tc_stat(test_json, index)
		chemicalObj["Vis"] = parse_vis_stat(test_json, index)
		



		# epi only
		chemicalObj["Koa"] = parse_koctair_stat(epi_json, index)

		chemicalObj["kOH"] = parse_ohratec_stat(epi_json, index)
		chemicalObj["OH_HL"] = parse_ohhl_stat(epi_json, index)
		chemicalObj["HLC"] = parse_hlc_stat(epi_json, index)
		
		chemicalObj["bioHC_HL"] = parse_biohchl_stat(epi_json, index)
		chemicalObj["bio_HL"] = parse_biohl_stat(epi_json, index)

		chemicalObj["Kb_rateC"] = parse_kbratec_stat(epi_json, index)
		chemicalObj["Kb_HL_pH8"] = parse_kbhlph8_stat(epi_json, index)
		chemicalObj["Kb_HL_pH7"] = parse_kbhlph7_stat(epi_json, index)
		chemicalObj["biotrans_HL"] = parse_biotranshl_stat(epi_json, index)

		chemicalObj["biodeg_ultimate"] = parse_bultimate_stat(epi_json, index)
		chemicalObj["biodeg_primary"] = parse_bprimary_stat(epi_json, index)

		chemicalObj["kO3"]=parse_ko3_stat(epi_json,index)
		chemicalObj["kNO3"]=parse_kno3_stat(epi_json,index)

		chemicalObj["Km_10"]=parse_km10_stat(epi_json,index)
		# chemicalObj["biodeg_linear"] = parse_blinear_stat(epi_json, index)
		# chemicalObj["biodeg_nonlinear"] = parse_bnonlinear_stat(epi_json, index)
		# chemicalObj["biodeg_MITIlinear"] = parse_bmitilinear_stat(epi_json, index)
		# chemicalObj["biodeg_MITInonlinear"] = parse_bmitinonlinear_stat(epi_json, index)
		# chemicalObj["biodeg_anaerobic"] = parse_banaerobic_stat(epi_json, index)
		# chemicalObj["biodeg_ready"] = parse_bready_stat(epi_json, index)
		chemicalObj["biodeg_ready_all"]=parse_biodeg(epi_json,vega_json,index)


		#{avg,note,source,unit}
		ecostarend=["fish_LC50_96hr","dm_LC50_48hr","algae_EC50_96hr","fish_ChV","dm_ChV","algae_ChV","fishSW_LC50_96hr","fishSW_ChV","shrimp_LC50_96hr","shrimpSW_ChV","earthworm_14day"]
		ecostarlist=["fishLC50_96hr_ecosar","dmLC50_48hr_ecosar","algaeEC50_96hr_ecosar","fishChV_ecosar","dmChV_ecosar","algaeChV_ecosar","fishLC50SW_96hr_ecosar","fishChVSW_ecosar","shrimpLC50_96hr_ecosar","shrimpSWChV_ecosar","earthworm_14day_ecosar"]

		for i in range(len(ecostarend)):
			a=ecostarend[i]
			b=ecostarlist[i]
			chemicalObj[a]=parse_ecostar_stat(epi_json, index, b)

		# no change #############





		chemicalObj["WWTremoval_10000hr"] = parse_totalRemoval_10000hr_stat(epi_json, index)
		chemicalObj["WWTremoval_EPAmethod"] = parse_totalRemoval_EPAmethod_stat(epi_json, index)
		chemicalObj["WWTbio_10000hr"] = parse_totalBiodeg_10000hr_stat(epi_json, index)
		chemicalObj["WWTbio_EPAmethod"] = parse_totalBiodeg_EPAmethod_stat(epi_json, index)
		chemicalObj["WWTslu_10000hr"] = parse_totalSldAds_10000hr_stat(epi_json, index)
		chemicalObj["WWTslu_EPAmethod"] = parse_totalSldAds_EPAmethod_stat(epi_json, index)
		chemicalObj["WWTair_10000hr"] = parse_totalToAir_10000hr_stat(epi_json, index)
		chemicalObj["WWTair_EPAmethod"] = parse_totalToAir_EPAmethod_stat(epi_json, index)
	
		chemicalObj["fish_LC50_acute_class"] = parse_fishLC50class_stat(vega_json, index)
		chemicalObj["fish_LC50_acute"] = parse_fishLC50_stat(vega_json, index)
		chemicalObj["fm_LC50_96hr"] = parse_fmLC50_stat(vega_json, test_json, index)
		chemicalObj["dm_LC50_48hr"] = parse_dmLC50_stat(vega_json, test_json,epi_json, index)

		chemicalObj["mutaTox"] = parse_mutaTox_stat(vega_json, test_json, index)
		chemicalObj["carTox"] = parse_carciTox_stat(vega_json, index)
		chemicalObj["devTox"] = parse_deveTox_stat(vega_json, test_json, index)
		chemicalObj["ER"] = parse_ER_stat(vega_json, index)
		chemicalObj["skinSensi"] = parse_skinSensi_stat(vega_json, index)
		chemicalObj["OratLD50"] = parse_OratLD50_stat(test_json, index)

		#change the attributes of each endpoints
		#change the name avg to average
		#if cannot get any average result, then the attribute of the endpoint is 'na'
		for currentobject in chemicalObj:
			if currentobject!="No." and currentobject!="CAS" and currentobject!="Smiles":
				if "avg" in chemicalObj[currentobject]:
					chemicalObj[currentobject]["average"] = chemicalObj[currentobject]["avg"]
					del chemicalObj[currentobject]["avg"]

					if chemicalObj[currentobject]["average"]=="N/A":
						chemicalObj[currentobject]["source"]="na"
						if "standard_deviation" in chemicalObj[currentobject]:
							chemicalObj[currentobject]["standard_deviation"]="na"
				
				if "average" in chemicalObj[currentobject]:
					if ("count_positive" not in chemicalObj[currentobject]) and (chemicalObj[currentobject]["average"]=="N/A" or chemicalObj[currentobject]["average"]=="na"):
						chemicalObj[currentobject]["source"]="na"
						if "standard_deviation" in chemicalObj[currentobject]:						
							chemicalObj[currentobject]["standard_deviation"]="na"
					if chemicalObj[currentobject]["average"]=="not classifiable" and "count_positive" in chemicalObj[currentobject]:
						chemicalObj[currentobject]["note"]="not classifiable"
						chemicalObj[currentobject]["average"]="na"	

				for element in chemicalObj[currentobject]:
					if chemicalObj[currentobject][element]=="N/A":
						chemicalObj[currentobject][element]="na"
			else:
				if chemicalObj[currentobject]=="N/A":
					chemicalObj[currentobject]="na"

		# print chemicalObj["No."]
		# print chemicalObj["Smiles"]

		# print len(chemicalObj["MW"])
		# print len(chemicalObj["MD"])
		# print len(chemicalObj["BCF"])
		# print len(chemicalObj["kOctWater"])
		# print len(chemicalObj["kOrgWater"])
		# print len(chemicalObj["kAirWater"])
		# print len(chemicalObj["kOctAir"])
		# print len(chemicalObj["HL_air"])
		# print len(chemicalObj["HL_water"])
		# print len(chemicalObj["HL_soil"])
		# print len(chemicalObj["HL_sediment"])
		# print len(chemicalObj["HL_aer"])
		# print len(chemicalObj["HL_sussed"])
		# print len(chemicalObj["VP"])
		# print len(chemicalObj["WS"])

		# print len(chemicalObj["WWTremoval_10000hr"])
		# print len(chemicalObj["WWTremoval_EPAmethod"])
		# print len(chemicalObj["WWTbio_10000hr"])
		# print len(chemicalObj["WWTbio_EPAmethod"])
		# print len(chemicalObj["WWTslu_10000hr"])
		# print len(chemicalObj["WWTslu_EPAmethod"])
		# print len(chemicalObj["WWTair_10000hr"])
		# print len(chemicalObj["WWTair_EPAmethod"])

		# print len(chemicalObj["fishLC50class"])
		# print len(chemicalObj["fishLC50"])
		# print len(chemicalObj["fmLC50"])
		# print len(chemicalObj["dmLC50"])

		# print len(chemicalObj["mutaTox"])
		# print len(chemicalObj["carciTox"])
		# print len(chemicalObj["deveTox"])
		# print len(chemicalObj["ER"] )
		# print len(chemicalObj["skinSensi"])
		# print len(chemicalObj["OratLD50"])


		# print vega_json[index]["SMILES"]
		# print test_json[index]["Smiles"]
		chemicalsJson.append(chemicalObj)


	# pp = pprint.PrettyPrinter(indent=4)
	# pp.pprint(chemicalsJson)
	with open(outputFilePath, "w") as outputFile:
		json.dump(chemicalsJson, outputFile, sort_keys=True, indent= 4, separators=(',', ': '))
	return chemicalsJson





#From here is about the parse function#
#For each end point, there is a function that will parse the endpoint as the hierachy#


def parse_ata_stat(epi_json,index):
	value=epi_json[index]["aquaTox_acute  unitless"]
	stat={}

	if value!="N/A":
		stat["average"]=value
		stat["sample_size"]=1
		stat["minimum"]=value
		stat["maximum"]=value
	else:
		stat["average"]="N/A"
		stat["sample_size"]=0
		stat["minimum"]="N/A"
		stat["maximum"]="N/A"

	stat["note"]="medium"
	stat["source"]="EPI Suite"
	stat["unit"]="N/A"	
	stat["standard_deviation"]="N/A"
	return stat

def parse_ko3_stat(epi_json,index):
	value=epi_json[index]["kO3  cm3/molecule-sec"]
	stat={}

	if value!="N/A":
		stat["average"]=value
		stat["sample_size"]=1
		stat["minimum"]=value
		stat["maximum"]=value
	else:
		stat["average"]="N/A"
		stat["sample_size"]=0
		stat["minimum"]="N/A"
		stat["maximum"]="N/A"

	stat["note"]="medium"
	stat["source"]="EPI Suite"
	stat["unit"]="cm3/molecule-sec"	
	stat["standard_deviation"]="N/A"
	return stat

def parse_kno3_stat(epi_json,index):
	value=epi_json[index]["kNO3  cm3/molecule-sec"]
	stat={}

	if value!="N/A":
		stat["average"]=value
		stat["sample_size"]=1
		stat["minimum"]=value
		stat["maximum"]=value
	else:
		stat["average"]="N/A"
		stat["sample_size"]=0
		stat["minimum"]="N/A"
		stat["maximum"]="N/A"

	stat["note"]="medium"
	stat["source"]="EPI Suite"
	stat["unit"]="cm3/molecule-sec"	
	stat["standard_deviation"]="N/A"
	return stat


def parse_km10_stat(epi_json,index):
	value=epi_json[index]["Km_10  /day"]
	stat={}

	if value!="N/A":
		stat["average"]=float(value)
		stat["sample_size"]=1
		stat["minimum"]=float(value)
		stat["maximum"]=float(value)
	else:
		stat["average"]="N/A"
		stat["sample_size"]=0
		stat["minimum"]="N/A"
		stat["maximum"]="N/A"

	stat["note"]="medium"
	stat["source"]="EPI Suite"
	stat["unit"]="/day"	
	stat["standard_deviation"]="N/A"
	return stat



"""
	Viscosity at 25C
	  TEST
"""
def parse_vis_stat(test_json, index):
	md = [test_json[index][u"Viscosity at 25\u00b0C  Exp_Value:cP"]]
	md = floatList(md)
	md_stat = getStat(md, "exp", "TEST", "cP")
	if md_stat["average"] == "N/A":
		md = [test_json[index][u"Viscosity at 25\u00b0C  Pred_Value:cP"]]
		md = floatList(md)
		md_stat = getStat(md, "medium", "TEST", "cP")
	return md_stat



"""
	Flash Point
	  TEST
"""
def parse_fp_stat(test_json, index):
	md = [test_json[index][u"Flash point  Exp_Value:\u00b0C"]]
	md = floatList(md)
	md_stat = getStat(md, "exp", "TEST", "C")
	if md_stat["average"] == "N/A":
		md = [test_json[index][u"Flash point  Pred_Value:\u00b0C"]]
		md = floatList(md)
		md_stat = getStat(md, "medium", "TEST", "C")
	return md_stat

"""
	Thermal Conductivity at 25C
	  TEST
"""
def parse_tc_stat(test_json, index):
	md = [test_json[index][u"Thermal conductivity at 25\u00b0C  Exp_Value:mW/mK"]]
	md = floatList(md)
	md_stat = getStat(md, "exp", "TEST", "mW/mK")
	if md_stat["average"] == "N/A":
		md = [test_json[index][u"Thermal conductivity at 25\u00b0C  Pred_Value:mW/mK"]]
		md = floatList(md)
		md_stat = getStat(md, "medium", "TEST", "mW/mK")
	return md_stat


"""
	Boiling Point
	EPI Suite & T.E.S.T
"""
def c_to_k(origin):
	thislist=list()
	print(origin)
	for i in origin:
		if i!="N/A":
			a=i+273.15
			thislist.append(a)
		else:
			thislist.append(i)
	return thislist



def parse_bp_stat(epi_json, test_json, index):
	# first look at the experimental data
	vp_epi_exp = [epi_json[index]["BP  C  exp"]]
	vp_epi_exp = floatList(vp_epi_exp)
	#vp_epi_exp = c_to_k(vp_epi_exp)
	vp_test_exp = [test_json[index][u"Normal boiling point  Exp_Value:\u00b0C"]]
	vp_test_exp = floatList(vp_test_exp)
	#vp_test_exp = c_to_k(vp_test_exp)
	# vp_test_exp = mmHgToPa(vp_test_exp)
	if vp_epi_exp[0] != "N/A" and vp_test_exp[0] != "N/A":
		vp_exp = [vp_epi_exp[0], vp_test_exp[0]]
		return getStat(vp_exp, "exp", "EPI Suite & TEST", "C")
	elif vp_epi_exp[0] != "N/A":
		return getStat(vp_epi_exp, "exp", "EPI Suite", "C")
	elif vp_test_exp[0] != "N/A":
		return getStat(vp_test_exp, "exp", "TEST", "C")
	else:
		# then estimation data
		vp_epi_est = [epi_json[index]["BP  C  est"]]
		vp_epi_est = floatList(vp_epi_est)
		#vp_epi_est = c_to_k(vp_epi_est)
		vp_test_est = [test_json[index][u"Normal boiling point  Pred_Value:\u00b0C"]]
		vp_test_est = floatList(vp_test_est)
		#vp_test_est = c_to_k(vp_test_est)
		# vp_test_est = mmHgToPa(vp_test_est)
		if (vp_epi_est[0] != "N/A" and vp_test_est[0] != "N/A") \
			or (vp_epi_est[0] == "N/A" and vp_test_est[0] == "N/A"):
			vp_est = [vp_epi_est[0], vp_test_est[0]]
			return getStat(vp_est, "medium", "EPI Suite & TEST", "C")
		elif vp_epi_est[0] != "N/A":
			return getStat(vp_epi_est, "medium", "EPI Suite", "C")
		elif vp_test_est[0] != "N/A":
			return getStat(vp_test_est, "medium", "TEST", "C")

"""
	Melting Point
	EPI Suite & T.E.S.T
"""
def parse_mp_stat(epi_json, test_json, index):
	# first look at the experimental data
	vp_epi_exp = [epi_json[index]["MP  C  exp"]]
	vp_epi_exp = floatList(vp_epi_exp)
	vp_test_exp = [test_json[index][u"Melting point  Exp_Value:\u00b0C"]]
	vp_test_exp = floatList(vp_test_exp)
	# vp_test_exp = mmHgToPa(vp_test_exp)
	if vp_epi_exp[0] != "N/A" and vp_test_exp[0] != "N/A":
		vp_exp = [vp_epi_exp[0], vp_test_exp[0]]
		return getStat(vp_exp, "exp", "EPI Suite & TEST", "C")
	elif vp_epi_exp[0] != "N/A":
		return getStat(vp_epi_exp, "exp", "EPI Suite", "C")
	elif vp_test_exp[0] != "N/A":
		return getStat(vp_test_exp, "exp", "TEST", "C")
	else:
		# then estimation data
		vp_epi_est = [epi_json[index]["MP  C  est"]]
		vp_epi_est = floatList(vp_epi_est)
		vp_test_est = [test_json[index][u"Melting point  Pred_Value:\u00b0C"]]
		vp_test_est = floatList(vp_test_est)
		# vp_test_est = mmHgToPa(vp_test_est)
		if (vp_epi_est[0] != "N/A" and vp_test_est[0] != "N/A") \
			or (vp_epi_est[0] == "N/A" and vp_test_est[0] == "N/A"):
			vp_est = [vp_epi_est[0], vp_test_est[0]]
			return getStat(vp_est, "medium", "EPI Suite & TEST", "C")
		elif vp_epi_est[0] != "N/A":
			return getStat(vp_epi_est, "medium", "EPI Suite", "C")
		elif vp_test_est[0] != "N/A":
			return getStat(vp_test_est, "medium", "TEST", "C")


"""
	Particle/gas partition coef. Mackay model
		EPI Suite
"""
def parse_kaerair_stat(epi_json, index):
	mw1 = epi_json[index]["kAerAir  m3/ug  Mackay"]
	mw2 = epi_json[index]["kAerAir  m3/ug  Koa"]
	mw=list()
	if mw1 != "N/A":
		mw.append(float(mw1))
	if mw2 != "N/A":
		mw.append(float(mw2))
	return getStat(mw, "medium", "EPI Suite", "m3/ug")

"""
	Atmospheric Oxidation - OH Rate Constant
		EPI Suite
"""
def parse_ohratec_stat(epi_json, index):
	mw = epi_json[index]["kOH  cm3/molecule-sec"]
	if mw != "N/A":
		mw = float(mw)
	return getStat([mw], "medium", "EPI Suite", "cm3/molecule-sec")

"""
	Atmospheric Oxidation - OH halflife
		EPI Suite
"""
def parse_ohhl_stat(epi_json, index):
	mw = epi_json[index]["OH_HL  days"]
	if mw != "N/A":
		mw = float(mw)
	return getStat([mw], "medium", "EPI Suite", "days")

"""
	Henry's Law Constant
		EPI Suite
"""

def pa_to_atm(origin):
	thislist=list()
	for i in origin:
		if i!="N/A":
			a=i*0.00000986923
			thislist.append(a)
		else:
			thislist.append(i)
	return thislist

def parse_hlc_stat(epi_json, index):
	expvalue=[epi_json[index]["HLC  Pa-m3/mole  exp"]]
	mw = [epi_json[index]["HLC  Pa-m3/mole  Bond"],epi_json[index]["HLC  Pa-m3/mole  Group"]]
	if expvalue[0]!="N/A":
		mw=floatList(expvalue)
		#mw = pa_to_atm(mw)
		return getStat(mw, "exp", "EPI Suite", "Pa-m3/mole")
	elif mw[0] != "N/A" and mw[1] !="N/A":
		mw = floatList(mw)
		#mw = pa_to_atm(mw)
	elif mw[0] != "N/A":
		mw=[epi_json[index]["HLC  Pa-m3/mole  Bond"]]
		mw = floatList(mw)
		#mw = pa_to_atm(mw)
	elif mw[1] != "N/A":
		mw=[epi_json[index]["HLC  Pa-m3/mole  Group"]]
		mw = floatList(mw)
		#mw = pa_to_atm(mw)
	return getStat(mw, "medium", "EPI Suite", "Pa-m3/mole")

"""
	Hydrocarbon biodegradation half life
		EPI Suite
"""
def parse_biohchl_stat(epi_json, index):
	mw = epi_json[index]["bioHC_HL  days"]
	if mw != "N/A":
		mw = float(mw)
	return getStat([mw], "medium", "EPI Suite", "days")

def parse_biohl_stat(epi_json, index):
	mw = epi_json[index]["bio_HL  days"]
	if mw != "N/A":
		mw = float(mw)
	return getStat([mw], "medium", "EPI Suite", "days")

"""
	Aqueous Base/Acid-catalyzed Hydrolysis - Rate Constant (pH > 8)
		EPI Suite
"""
def parse_kbratec_stat(epi_json, index):
	mw = epi_json[index]["Kb_rateC  L/mol-sec"]
	if mw != "N/A":
		mw = float(mw)
	return getStat([mw], "medium", "EPI Suite", "L/mol-sec")

"""
	Aqueous Base/Acid-catalyzed Hydrolysis - halflife (pH = 8)
		EPI Suite
"""
def parse_kbhlph8_stat(epi_json, index):
	mw = epi_json[index]["Kb_HL_pH8  days"]
	if mw != "N/A":
		mw = float(mw)
	return getStat([mw], "medium", "EPI Suite", "days")

"""
	Aqueous Base/Acid-catalyzed Hydrolysis - halflife (pH = 7)
		EPI Suite
"""
def parse_kbhlph7_stat(epi_json, index):
	mw = epi_json[index]["Kb_HL_pH7  days"]
	if mw != "N/A":
		mw = float(mw)
	return getStat([mw], "medium", "EPI Suite", "days")


"""
	Biotransformation Half-life (HL)
		EPI Suite
"""
def parse_biotranshl_stat(epi_json, index):
	mw = epi_json[index]["biotrans_HL  days"]
	if mw != "N/A":
		mw = float(mw)
	return getStat([mw], "medium", "EPI Suite", "days")


# """
# 	Biodegradation (Biowin1, linear)
# 		EPI Suite
# """
# def parse_blinear_stat(epi_json, index):
# 	mw = epi_json[index]["biodeg_linear"]
# 	if mw != "N/A":
# 		mw = float(mw)
# 	return getStat([mw], "est", "EPI", "N/A")

# """
# 	Biodegradation (Biowin2, non-linear)
# 		EPI Suite
# """
# def parse_bnonlinear_stat(epi_json, index):
# 	mw = epi_json[index]["biodeg_nonlinear"]
# 	# if mw != "N/A":
# 	# 	mw = float(mw)
# 	return getStat([mw], "est", "EPI", "N/A")

"""
	Biodegradation (ultimate)
			EPI Suite
"""
def parse_bultimate_stat(epi_json, index):
	mw = epi_json[index]["biodeg_ultimate  unitless"]
	stat={}
	stat["average"]=mw
	stat["note"]="medium"
	stat["source"]="EPI Suite"
	stat["unit"]="N/A"
	stat["minimum"]="N/A"
	stat["maximum"]="N/A"
	stat["sample_size"]=1
	stat["standard_deviation"]="N/A"
	return stat

"""
	Biodegradation (primary)
			EPI Suite
"""
def parse_bprimary_stat(epi_json, index):
	mw = epi_json[index]["biodeg_primary  unitless"]
	stat={}
	stat["average"]=mw
	stat["note"]="medium"
	stat["source"]="EPI Suite"
	stat["unit"]="N/A"
	stat["minimum"]="N/A"
	stat["maximum"]="N/A"
	stat["sample_size"]=1
	stat["standard_deviation"]="N/A"
	return stat

# """
# 	Biodegradation (MITI linear)
# 		EPI Suite
# """
# def parse_bmitilinear_stat(epi_json, index):
# 	mw = epi_json[index]["biodeg_MITIlinear"]
# 	if mw != "N/A":
# 		mw = float(mw)
# 	return getStat([mw], "est", "EPI", "N/A")

# """
# 	Biodegradation (MITI non-linear)
# 		EPI Suite
# """
# def parse_bmitinonlinear_stat(epi_json, index):
# 	mw = epi_json[index]["biodeg_MITInonlinear"]
# 	if mw != "N/A":
# 		mw = float(mw)
# 	return getStat([mw], "est", "EPI", "N/A")

# """
# 	anaerobic biodegradation
# 		EPI Suite
# """
# def parse_banaerobic_stat(epi_json, index):
# 	mw = epi_json[index]["biodeg_anaerobic"]
# 	if mw != "N/A":
# 		mw = float(mw)
# 	return getStat([mw], "est", "EPI", "N/A")

# """
# 	Ready Biodegradability Prediction
# 		EPI Suite
# """
# def parse_bready_stat(epi_json, index):
# 	mw = epi_json[index]["biodeg_ready"]
# 	stat={}
# 	stat["avg"]=mw
# 	stat["note"]="est"
# 	stat["source"]="EPI"
# 	stat["unit"]="N/A"
# 	return stat


def parse_biodeg(epi_json,vega_json,index):
	elinear = epi_json[index]["biodeg_linear  unitless"]
	enonlinear = epi_json[index]["biodeg_nonlinear  unitless"]
	emlinear = epi_json[index]["biodeg_MITIlinear  unitless"]
	emnonlinear = epi_json[index]["biodeg_MITInonlinear  unitless"]
	eready = epi_json[index]["biodeg_ready  unitless"]
	ea = epi_json[index]["biodeg_anaerobic  unitless"]
	stat={}

	vexp=vega_json[index]["Ready Biodegradability model (IRFMN) - experimental value"]
	va=vega_json[index]["Ready Biodegradability model (IRFMN) - assessment"]

	if vexp!="N/A":
		vep=0
		ven=0
		venotc=0

		if "Possible" in vexp or "Not predicted" in vexp:
			venotc += 1
			stat["average"]="not classifiable"
		elif "NON" in vexp or "Inactive" in vexp:
			ven += 1
			stat["average"]="not ready biodegradable"
		else:
			vep += 1
			stat["average"]="ready biodegradable"

		stat["count_positive"]=vep
		stat["count_negative"]=ven
		stat["count_not_classified"]=venotc
		stat["sample_size"]=1
		stat["source"]="VEGA"
		stat["note"]="exp"
		stat["unit"]="N/A"
		return stat

	if va!="N/A":
		stat["source"]="VEGA & EPI Suite"
		if "high" in va:
			if "Non" in va:
				eready="No"
			else:
				eready="Yes"
	else:
		stat["source"]="EPI Suite"

	p=0
	n=0
	notc=0
	s=6
	alist=[elinear,enonlinear,emlinear,emnonlinear,eready,ea]
	for i in alist:
		if i=="Yes":
			p=p+1
		elif i=="No":
			n=n+1
		else:
			notc=notc+1

	if p==n:
		if eready=="No":
			avg="not ready biodegradable"
		else:
			avg="ready biodegradable"
	else:
		if p>n:
			avg="ready biodegradable"
		elif n>p:
			avg="not ready biodegradable"

	stat["average"]=avg
	if p==0 and n==0:
		stat["average"]="N/A"
	stat["count_positive"]=p
	stat["count_negative"]=n
	stat["count_not_classified"]=notc
	stat["sample_size"]=s
	stat["note"]="medium"
	stat["unit"]="N/A"

	return stat









"""
	ecostar
		EPI Suite
"""
def parse_ecostar_stat(epi_json, index, name):
	mw1 = epi_json[index][name+"  mg/L"]
	mw=list()

	if mw1!="N/A":
		mw.append(float(mw1))


	return getgeoStat(mw,"medium","EPI Suite","mg/L")





"""
	Molecular Weight
		EPI Suite
"""
def parse_mw_stat(epi_json, index):
	mw = epi_json[index]["MW  g/mol"]
	if mw != "N/A":
		mw = float(mw)
	return getStat([mw], "medium", "EPI Suite", "g/mol")


"""
	Density
	  TEST
"""
def parse_density_stat(test_json, index):
	md = [test_json[index][u"Density  Exp_Value:g/cm\u00b3  C"]]
	md = floatList(md)
	md_stat = getStat(md, "exp", "TEST", u"g/cm3")
	if md_stat["average"] == "N/A":
		md = [test_json[index][u"Density  Pred_Value:g/cm\u00b3  C"]]
		md = floatList(md)
		md_stat = getStat(md, "medium", "TEST", u"g/cm3")
	return md_stat


"""
	BCF
		EPI Suite & VEGA
"""
def parse_bcf_stat(epi_json, vega_json, index):
	# experiment data first
	bcf_vega_exp = [vega_json[index]["BCF model (CAESAR) - experimental value"],
					vega_json[index]["BCF model (KNN/Read-Across) - experimental value"],
					vega_json[index]["BCF model (Meylan) - experimental value"]]
	bcf_vega_exp = floatList(bcf_vega_exp)
	bcf_vega_exp = unLogList(bcf_vega_exp)
	bcf_vega_exp_stat = getStat(bcf_vega_exp, "exp", "VEGA", "L/kg wet-wt")		
	if bcf_vega_exp_stat["average"] == "N/A":
		bcf_vega_est = [vega_json[index]["BCF model (CAESAR) - assessment"],
						vega_json[index]["BCF model (KNN/Read-Across) - assessment"],
						vega_json[index]["BCF model (Meylan) - assessment"]]
		# get good reliability first
		bcf_vega_est_good = []
		for bcf_vaga_est_ins in bcf_vega_est:
			if "good reliability" in bcf_vaga_est_ins:
				bcf_vega_est_good.append(bcf_vaga_est_ins)
		if len(bcf_vega_est_good) >= 1:
			bcf_vega_est_good_v = []
			for bcf_vega_est_good_ins in bcf_vega_est_good:
				tempValue = float(bcf_vega_est_good_ins[:bcf_vega_est_good_ins.index("log(L/kg)")].strip())
				bcf_vega_est_good_v.append(tempValue)
			bcf_vega_est_good_stat = getStat(bcf_vega_est_good_v, "high", "VEGA", "L/kg wet-wt")
			# chemicalObj["BCF"] = bcf_vega_est_good_stat
			return bcf_vega_est_good_stat
		else:
			# then get moderate reliability
			bcf_vega_est_moderate = []
			for bcf_vaga_est_ins in bcf_vega_est:
				if "moderate reliability" in bcf_vaga_est_ins:
					bcf_vega_est_moderate.append(bcf_vaga_est_ins)
			if len(bcf_vega_est_moderate) >= 1:
				bcf_vega_est_moderate_v = []
				for bcf_vega_est_moderate_ins in bcf_vega_est_moderate:
					tempValue = float(bcf_vega_est_moderate_ins[:bcf_vega_est_moderate_ins.index("log(L/kg)")].strip())
					bcf_vega_est_moderate_v.append(tempValue)
				bcf_epi = [epi_json[index]["LogBCF  L/kg wet-wt  Arnot-Gobas"],
							epi_json[index]["LogBCF  L/kg wet-wt  Regression"]]
				bcf_epi = floatList(bcf_epi)
				if bcf_epi[0] == "N/A" and bcf_epi[1] == "N/A":
					bcf_vega_est_moderate_stat = getStat(bcf_vega_est_moderate_v, "medium", "VEGA", "L/kg wet-wt")
					# chemicalObj["BCF"] = bcf_vega_est_moderate_stat
					return bcf_vega_est_moderate_stat
				else:						
					bcf_vega_est_moderate_v.append(bcf_epi[0])
					bcf_vega_est_moderate_v.append(bcf_epi[1])
					bcf_vega_est_moderate_stat = getStat(bcf_vega_est_moderate_v, "medium", "VEGA & EPI Suite", "L/kg wet-wt")
					# chemicalObj["BCF"] = bcf_vega_est_moderate_stat
					return bcf_vega_est_moderate_stat
			else:
				# unfortunately use the low reliability
				bcf_vega_est_low = []
				for bcf_vaga_est_ins in bcf_vega_est:
					if "low reliability" in bcf_vaga_est_ins:
						bcf_vega_est_low.append(bcf_vaga_est_ins)
				if len(bcf_vega_est_low) >= 1:
					bcf_vega_est_low_v = []
					for bcf_vega_est_low_ins in bcf_vega_est_low:
						tempValue = float(bcf_vega_est_low_ins[:bcf_vega_est_low_ins.index("log(L/kg)")].strip())
						bcf_vega_est_low_v.append(tempValue)
					bcf_epi = [epi_json[index]["LogBCF  L/kg wet-wt  Arnot-Gobas"],
								epi_json[index]["LogBCF  L/kg wet-wt  Regression"]]
					bcf_epi = floatList(bcf_epi)
					if bcf_epi[0] == "N/A" and bcf_epi[1] == "N/A":
						bcf_vega_est_low_stat = getStat(bcf_vega_est_low_v, "low", "VEGA", "L/kg wet-wt")
						# chemicalObj["BCF"] = bcf_vega_est_low_stat
						return bcf_vega_est_low_stat
					else:
						bcf_vega_est_low_v.append(bcf_epi[0])
						bcf_vega_est_low_v.append(bcf_epi[1])
						bcf_vega_est_low_stat = getStat(bcf_vega_est_low_v, "low", "VEGA & EPI Suite", "L/kg wet-wt")
						# chemicalObj["BCF"] = bcf_vega_est_low_stat
						return bcf_vega_est_low_stat
				else:
					# only epi data
					bcf_epi = [epi_json[index]["LogBCF  L/kg wet-wt  Arnot-Gobas"],
								epi_json[index]["LogBCF  L/kg wet-wt  Regression"]]
					bcf_epi = floatList(bcf_epi)
					bcf_epi_est_stat = getStat(bcf_epi, "medium", "EPI Suite", "L/kg wet-wt")
					# chemicalObj["BCF"] = bcf_epi_est_stat
					return bcf_epi_est_stat
	else:
		# chemicalObj["BCF"] = bcf_vega_exp_stat
		return bcf_vega_exp_stat


"""
	kOctWater: Octanol/water partition coefficient (LogKow/LogP)
		EPI Suite & VEGA
"""
def parse_kow_stat(epi_json, vega_json, index):
	#   experiment data first
	kow_vega_exp = [vega_json[index]["LogP model (ALogP) - experimental value"],
					vega_json[index]["LogP model (MLogP) - experimental value"],
					vega_json[index]["LogP model (Meylan/Kowwin) - experimental value"]]
	kow_vega_exp = floatList(kow_vega_exp)
	kow_vega_exp = unLogList(kow_vega_exp)
	kow_epi_exp = [epi_json[index]["kOctWater  unitless  exp"]]
	kow_epi_exp = floatList(kow_epi_exp)
	if kow_epi_exp[0] == "N/A":
		kow_exp = kow_vega_exp
		kow_exp_stat = getStat(kow_exp, "exp", "VEGA", "N/A")
	else:
		kow_exp = kow_vega_exp
		kow_exp_vega_stat = getStat(kow_exp, "exp", "VEGA", "N/A")
		if kow_exp_vega_stat["average"] == "N/A":
			kow_exp_stat = getStat(kow_epi_exp, "exp", "EPI Suite", "N/A")
		else:
			kow_exp.append(kow_epi_exp[0])
			kow_exp_stat = getStat(kow_exp, "exp", "VEGA & EPI Suite", "N/A")
	# experiment all N/A, let's check est
	if kow_exp_stat["average"] == "N/A":
		# get high reliability first
		kow_vega_est = [vega_json[index]["LogP model (ALogP) - assessment"],
						vega_json[index]["LogP model (MLogP) - assessment"],
						vega_json[index]["LogP model (Meylan/Kowwin) - assessment"]]
		# get good reliability first
		kow_vega_est_good = []
		for kow_vega_est_ins in kow_vega_est:
			if "good reliability" in kow_vega_est_ins:
				kow_vega_est_good.append(kow_vega_est_ins)
		if len(kow_vega_est_good) >= 1:
			kow_vega_est_good_v = []
			for kow_vega_est_good_ins in kow_vega_est_good:
				tempValue = pow(10,float(kow_vega_est_good_ins[:kow_vega_est_good_ins.index("(")].strip()))
				kow_vega_est_good_v.append(tempValue)
			kow_vega_est_good_stat = getStat(kow_vega_est_good_v, "high", "VEGA", "N/A")
			# chemicalObj["kOctWater"] = kow_vega_est_good_stat
			return kow_vega_est_good_stat
		else:
			# then get moderate reliability
			kow_vega_est_moderate = []
			for kow_vaga_est_ins in kow_vega_est:
				if "moderate reliability" in kow_vaga_est_ins:
					kow_vega_est_moderate.append(kow_vaga_est_ins)
			if len(kow_vega_est_moderate) >= 1:
				kow_vega_est_moderate_v = []
				for kow_vega_est_moderate_ins in kow_vega_est_moderate:
					tempValue = pow(10,float(kow_vega_est_moderate_ins[:kow_vega_est_moderate_ins.index("(")].strip()))
					kow_vega_est_moderate_v.append(tempValue)
				kow_epi = [epi_json[index]["kOctWater  unitless  est"]]
				kow_epi = floatList(kow_epi)
				if kow_epi[0] == "N/A":
					kow_vega_est_moderate_stat = getStat(kow_vega_est_moderate_v, "medium", "VEGA", "N/A")
					# chemicalObj["kOctWater"] = kow_vega_est_moderate_stat
					return kow_vega_est_moderate_stat
				else:						
					kow_vega_est_moderate_v.append(kow_epi[0])
					kow_vega_est_moderate_stat = getStat(kow_vega_est_moderate_v, "medium", "VEGA & EPI Suite", "N/A")
					# chemicalObj["kOctWater"] = kow_vega_est_moderate_stat
					return kow_vega_est_moderate_stat
			else:
				# unfortunately use the low reliability
				kow_vega_est_low = []
				for kow_vaga_est_ins in kow_vega_est:
					if "low reliability" in kow_vaga_est_ins:
						kow_vega_est_low.append(kow_vaga_est_ins)
				if len(kow_vega_est_low) >= 1:
					kow_vega_est_low_v = []
					for kow_vega_est_low_ins in kow_vega_est_low:
						tempValue = pow(10,float(kow_vega_est_low_ins[:kow_vega_est_low_ins.index("(")].strip()))
						kow_vega_est_low_v.append(tempValue)
					kow_epi = [epi_json[index]["kOctWater  unitless  est"]]
					kow_epi = floatList(kow_epi)
					if kow_epi[0] == "N/A":
						kow_vega_est_low_stat = getStat(kow_vega_est_low_v, "low", "VEGA", "N/A")
						# chemicalObj["kOctWater"] = kow_vega_est_low_stat
						return kow_vega_est_low_stat
					else:
						kow_vega_est_low_v.append(kow_epi[0])
						kow_vega_est_low_stat = getStat(kow_vega_est_low_v, "low", "VEGA & EPI Suite", "N/A")
						# chemicalObj["kOctWater"] = kow_vega_est_low_stat
						return kow_vega_est_low_stat
				else:
					# only epi data
					kow_epi = [epi_json[index]["kOctWater  unitless  est"]]
					kow_epi = floatList(kow_epi)
					kow_epi_est_stat = getStat(kow_epi, "medium", "EPI Suite", "N/A")
					# chemicalObj["kOctWater"] = kow_epi_est_stat
					return kow_epi_est_stat
	else:
		# chemicalObj["kOctWater"] = kow_exp_stat
		return kow_exp_stat


"""
	kOrgWater: Organic carbon/water partition coefficient (LogKoc)
		EPI
"""
def parse_koc_stat(epi_json, index):
	#   experiment data first
	koc_epi_exp = [epi_json[index]["kOrgWater  L/kg  exp"]]
	koc_epi_exp = floatList(koc_epi_exp)
	if koc_epi_exp[0] == "N/A":
		koc_epi_est = [epi_json[index]["kOrgWater  L/kg  Kow"],
						epi_json[index]["kOrgWater  L/kg  MCI"]]
		koc_epi_est = floatList(koc_epi_est)
		koc_est_stat = getStat(koc_epi_est, "medium", "EPI Suite", "L/kg")
		return koc_est_stat
	else:
		return getStat(koc_epi_exp, "exp", "EPI Suite", "L/kg")


"""
	kAirWater: Air/water partition coefficient (LogKaw)
		EPI
"""
def parse_kaw_stat(epi_json, index):
	#   only estimation data
	kaw_epi_est = [epi_json[index]["kAirWater  unitless"]]
	kaw_epi_est = floatList(kaw_epi_est)
	return getStat(kaw_epi_est, "medium", "EPI Suite", "N/A")


"""
	kOctAir: Aerosol/air partition coefficient (LogKoa)
		EPI
"""
def parse_koa_stat(epi_json, index):
	#   experiment data first
	koa_epi_exp = [epi_json[index]["kOctAir  exp"]]
	koa_epi_exp = floatList(koa_epi_exp)
	if koa_epi_exp[0] == "N/A":
		koa_epi_est = [epi_json[index]["kOctAir  est"]]
		koa_epi_est = floatList(koa_epi_est)
		koa_est_stat = getStat(koa_epi_est, "medium", "EPI Suite", "N/A")
		return koa_est_stat
	else:
		return getStat(koa_epi_exp, "exp", "EPI Suite", "N/A")


"""
	HL_air: Degradation rate in air (halflife)
		EPI
"""
def parse_DegAir_stat(epi_json, index):
	#   only estimation data
	DegAir_epi_est = [epi_json[index]["HLDegAir  hour"]]
	DegAir_epi_est = floatList(DegAir_epi_est)
	return getStat(DegAir_epi_est, "medium", "EPI Suite", "h")


"""
	HL_water: Degradation rate in water (h)
		EPI
"""
def parse_DegWater_stat(epi_json, index):
	#   only estimation data
	DegWater_epi_est = [epi_json[index]["HLDegWater  hour"]]
	DegWater_epi_est = floatList(DegWater_epi_est)
	return getStat(DegWater_epi_est, "medium", "EPI Suite", "h")


"""
	HL_soil: Degradation rate in soil (h)
		EPI
"""
def parse_DegSoil_stat(epi_json, index):
	#   only estimation data
	DegSoil_epi_est = [epi_json[index]["HLDegSoil  hour"]]
	DegSoil_epi_est = floatList(DegSoil_epi_est)
	return getStat(DegSoil_epi_est, "medium", "EPI Suite", "h")


"""
	HL_sediment: Degradation rate in sediment (h)
		EPI
"""
def parse_DegSed_stat(epi_json, index):
	#   only estimation data
	DegSed_epi_est = [epi_json[index]["HLDegSed  hour"]]
	DegSed_epi_est = floatList(DegSed_epi_est)
	return getStat(DegSed_epi_est, "medium", "EPI Suite", "h")


"""
	HL_aer: Degradation rate in aerosol (h)
		EPI
"""
def parse_DegAero_stat(epi_json, index):
	#   only estimation data
	DegAero_epi_est = [epi_json[index]["HLDegAero  hour"]]
	DegAero_epi_est = floatList(DegAero_epi_est)
	return getStat(DegAero_epi_est, "medium", "EPI Suite", "h")


"""
	HL_sussed: Degradation rate in suspendid sediment (h)
		EPI
"""
def parse_DegSSed_stat(epi_json, index):
	#   only estimation data
	DegSSed_epi_est = [epi_json[index]["HLDegSsed  hour"]]
	DegSSed_epi_est = floatList(DegSSed_epi_est)
	return getStat(DegSSed_epi_est, "medium", "EPI Suite", "h")


"""
	VP: Vapor Pressure (Pa)
		EPI & TEST
"""
def mmhg_to_pa(origin):
	thislist=list()
	#print(origin)
	for i in origin:
		if i!="N/A":
			a=i*133.32239
			thislist.append(a)
		else:
			thislist.append(i)
	return thislist

def parse_vp_stat(epi_json, test_json, index):
	# first look at the experimental data
	vp_epi_exp = [epi_json[index]["VP  mmHg  exp"]]
	vp_epi_exp = floatList(vp_epi_exp)
	vp_epi_exp = mmhg_to_pa(vp_epi_exp)

	vp_test_exp = [test_json[index][u"Vapor pressure at 25\u00b0C  Exp_Value:mmHg"]]
	vp_test_exp = floatList(vp_test_exp)
	vp_test_exp = mmhg_to_pa(vp_test_exp)
	# vp_test_exp = mmHgToPa(vp_test_exp)
	if vp_epi_exp != [] and vp_epi_exp[0] != "N/A" and vp_test_exp[0] != "N/A":
		vp_exp = [vp_epi_exp[0], vp_test_exp[0]]
		return getStat(vp_exp, "exp", "EPI Suite & TEST", "Pa")
	elif vp_epi_exp != [] and vp_epi_exp[0] != "N/A":
		return getStat(vp_epi_exp, "exp", "EPI Suite", "Pa")
	elif vp_test_exp != [] and vp_test_exp[0] != "N/A":
		return getStat(vp_test_exp, "exp", "TEST", "Pa")
	else:
		# then estimation data
		vp_epi_est = [epi_json[index]["VP  mmHg  est"]]
		vp_epi_est = floatList(vp_epi_est)
		vp_epi_est = mmhg_to_pa(vp_epi_est)
		vp_test_est = [test_json[index][u"Vapor pressure at 25\u00b0C  Pred_Value:mmHg"]]
		vp_test_est = floatList(vp_test_est)
		vp_test_est = mmhg_to_pa(vp_test_est)
		# vp_test_est = mmHgToPa(vp_test_est)
		if (vp_epi_est != [] and vp_epi_est[0] != "N/A" and vp_test_est[0] != "N/A") \
			or (vp_epi_est != [] and vp_epi_est[0] == "N/A" and vp_test_est[0] == "N/A"):
			vp_est = [vp_epi_est[0], vp_test_est[0]]
			return getStat(vp_est, "medium", "EPI Suite & TEST", "Pa")
		elif vp_epi_est != [] and vp_epi_est[0] != "N/A":
			return getStat(vp_epi_est, "medium", "EPI Suite", "Pa")
		elif vp_test_est != [] and vp_test_est[0] != "N/A":
			return getStat(vp_test_est, "medium", "TEST", "Pa")


"""
	WS: Water Solubility (mg/L)
		EPI & TEST
"""
def parse_ws_stat(epi_json, test_json, index):
	# first look at the experimental data
	ws_epi_exp = [epi_json[index]["WS  mg/L  WATERNT  exp"],epi_json[index]["WS  mg/L  WSKOW  exp"]]
	ws_epi_exp = floatList(ws_epi_exp)
	ws_test_exp = [test_json[index][u"Water solubility at 25\u00b0C  Exp_Value:mg/L"]]
	ws_test_exp = floatList(ws_test_exp)

	ws_epi_est = [epi_json[index]["WS  mg/L  WATERNT  est"],epi_json[index]["WS  mg/L  WSKOW  est"]]
	ws_epi_est = floatList(ws_epi_est)
	ws_test_est = [test_json[index][u"Water solubility at 25\u00b0C  Pred_Value:mg/L"]]
	ws_test_est = floatList(ws_test_est)


	# if ws_epi_exp[0] != "N/A" and ws_test_exp[0] != "N/A":
	# 	ws_exp = [ws_epi_exp[0], ws_test_exp[0]]
	# 	return getStat(ws_exp, "exp", "EPI & VEGA", "mg/L")
	# elif ws_epi_exp[0] != "N/A":
	# 	return getStat(ws_epi_exp, "exp", "EPI", "mg/L")
	# elif ws_test_exp[0] != "N/A":
	# 	return getStat(ws_test_exp, "exp", "VEGA", "mg/L")

		# if (ws_epi_est[0] != "N/A" and ws_test_est[0] != "N/A") \
		# 	or (ws_epi_est[0] == "N/A" and ws_test_est[0] == "N/A"):
		# 	ws_est = [ws_epi_est[0], ws_test_est[0]]
		# 	return getStat(ws_est, "est", "EPI & VEGA", "mg/L")
		# elif ws_epi_est[0] != "N/A":
		# 	return getStat(ws_epi_est, "est", "EPI", "mg/L")
		# elif ws_test_est[0] != "N/A":
		# 	return getStat(ws_test_est, "est", "VEGA", "mg/L")


	if ws_epi_exp[0] != "N/A" or ws_epi_exp[1] != "N/A" or ws_test_exp[0] != "N/A":
		ws_exp=list()
		if ws_epi_exp[0] != "N/A":
			ws_exp.append(ws_epi_exp[0])
		if ws_epi_exp[1] != "N/A":
			ws_exp.append(ws_epi_exp[1])
		if ws_test_exp[0] !="N/A":
			ws_exp.append(ws_test_exp[0])

		if ws_epi_exp[0] == "N/A" and ws_epi_exp[1] == "N/A":
			return getStat(ws_test_exp, "exp", "TEST", "mg/L")
		if ws_test_exp[0] == "N/A":
			return getStat(ws_epi_exp, "exp", "EPI Suite", "mg/L")

		return getStat(ws_exp, "exp", "EPI Suite & TEST", "mg/L")
	else:
		# then estimation data
		ws_est=list()
		if ws_epi_est[0] != "N/A":
			ws_est.append(ws_epi_est[0])
		if ws_epi_est[1] != "N/A":
			ws_est.append(ws_epi_est[1])
		if ws_test_est[0] !="N/A":
			ws_est.append(ws_test_est[0])

		if ws_epi_est[0] == "N/A" and ws_epi_est[1] == "N/A":
			return getStat(ws_test_est, "medium", "TEST", "mg/L")
		if ws_test_est[0] == "N/A":
			return getStat(ws_epi_est, "medium", "EPI Suite", "mg/L")

		return getStat(ws_est, "medium", "EPI Suite & TEST", "mg/L")


"""
	kOctAir: Particle / gas partition coef. (m3/ug)
		EPI
"""
def parse_koctair_stat(epi_json, index):
	#   only estimation data
	a=epi_json[index]["kOctAir  unitless  est"]
	b=epi_json[index]["kOctAir  unitless  exp"]
	if b!="N/A":
		k_epi_est = [b]
		k_epi_est = floatList(k_epi_est)
		return getStat(k_epi_est, "exp", "EPI Suite", "N/A")
	else:
		k_epi_est = [a]
		k_epi_est = floatList(k_epi_est)
		return getStat(k_epi_est, "medium", "EPI Suite", "N/A")		


"""
	WWTremoval_10000hr: WWTP Total Removal -- 10000hr (%)
		EPI
"""
def parse_totalRemoval_10000hr_stat(epi_json, index):
	#   only estimation data
	totalRm_epi_est1 = [epi_json[index]["WWTremoval  %  10000hr"]]
	totalRm_epi_est1 = floatList(totalRm_epi_est1)
	return getStat(totalRm_epi_est1, "medium", "EPI Suite", "%")


"""
	WWTremoval_EPAmethod: WWTP Total Removal -- Biowin/EPA (%)
		EPI
"""
def parse_totalRemoval_EPAmethod_stat(epi_json, index):
	#   only estimation data
	totalRm_epi_est2 = [epi_json[index]["WWTremoval  %  Biowin/EPA"]]
	totalRm_epi_est2 = floatList(totalRm_epi_est2)
	return getStat(totalRm_epi_est2, "medium", "EPI Suite", "%")


"""
	WWTbio_10000hr: WWTP Total Biodegradation -- 10000hr (%)
		EPI
"""
def parse_totalBiodeg_10000hr_stat(epi_json, index):
	#   only estimation data
	totalBiodeg_epi_est1 = [epi_json[index]["WWTbio  %  10000hr"]]
	totalBiodeg_epi_est1 = floatList(totalBiodeg_epi_est1)
	return getStat(totalBiodeg_epi_est1, "medium", "EPI Suite", "%")


"""
	WWTbio_EPAmethod: WWTP Total Biodegradation -- Biowin/EPA (%)
		EPI
"""
def parse_totalBiodeg_EPAmethod_stat(epi_json, index):
	#   only estimation data
	totalBiodeg_epi_est1 = [epi_json[index]["WWTbio  %  Biowin/EPA"]]
	totalBiodeg_epi_est1 = floatList(totalBiodeg_epi_est1)
	return getStat(totalBiodeg_epi_est1, "medium", "EPI Suite", "%")


"""
	WWTslu_10000hr: WWTP Total Sludge Adsorption -- 10000hr (%)
		EPI
"""
def parse_totalSldAds_10000hr_stat(epi_json, index):
	#   only estimation data
	totalSldAds_epi_est1 = [epi_json[index]["WWTslu  %  10000hr"]]
	totalSldAds_epi_est1 = floatList(totalSldAds_epi_est1)
	return getStat(totalSldAds_epi_est1, "medium", "EPI Suite", "%")


"""
	WWTslu_EPAmethod: WWTP Total Sludge Adsorption -- Biowin/EPA (%)
		EPI
"""
def parse_totalSldAds_EPAmethod_stat(epi_json, index):
	#   only estimation data
	totalSldAds_epi_est2 = [epi_json[index]["WWTslu  %  Biowin/EPA"]]
	totalSldAds_epi_est2 = floatList(totalSldAds_epi_est2)
	return getStat(totalSldAds_epi_est2, "medium", "EPI Suite", "%")


"""
	WWTair_10000hr: WWTP Total to Air -- 10000hr (%)
		EPI
"""
def parse_totalToAir_10000hr_stat(epi_json, index):
	#   only estimation data
	totalToAir_epi_est1 = [epi_json[index]["WWTair  %  10000hr"]]
	totalToAir_epi_est1 = floatList(totalToAir_epi_est1)
	return getStat(totalToAir_epi_est1, "medium", "EPI Suite", "%")


"""
	WWTair_EPAmethod: WWTP Total to Air -- Biowin/EPA (%)
		EPI
"""
def parse_totalToAir_EPAmethod_stat(epi_json, index):
	#   only estimation data
	totalToAir_epi_est2 = [epi_json[index]["WWTair  %  Biowin/EPA"]]
	totalToAir_epi_est2 = floatList(totalToAir_epi_est2)
	return getStat(totalToAir_epi_est2, "medium", "EPI Suite", "%")


"""
	fishLC50class: Fish Acute LC50 Toxicity Classification (Toxic-1,2,3 level)
		VEGA
"""
def parse_fishLC50class_stat(vega_json, index):
	#  first experiemental data
	fishLC50class_vega_exp = [vega_json[index]["Fish Acute (LC50) Toxicity classification (SarPy/IRFMN) - experimental value"]]
	stat = {}
	if fishLC50class_vega_exp[0] != "N/A":
		stat["average"] = fishLC50class_vega_exp[0]
		stat["minimum"] = fishLC50class_vega_exp[0]
		stat["maximum"] = fishLC50class_vega_exp[0]
		stat["sample_size"] = 1
		stat["standard_deviation"] = 0
		stat["note"] = "exp"
		stat["source"] = "VEGA"
		stat["unit"] = "N/A"
	else:
		fishLC50class_vega_est = vega_json[index]["Fish Acute (LC50) Toxicity classification (SarPy/IRFMN) - assessment"]
		if fishLC50class_vega_est == "N/A":
			stat["average"] = "N/A"
			stat["minimum"] = "N/A"
			stat["maximum"] = "N/A"
			stat["sample_size"] = 1
			stat["standard_deviation"] = 0
			stat["note"] = "medium"
			stat["source"] = "VEGA"
			stat["unit"] = "N/A"
		else:
			fishLC50class_vega_est_v = fishLC50class_vega_est[:fishLC50class_vega_est.rfind("(")].strip()
			fishLC50class_vega_est_r = fishLC50class_vega_est[fishLC50class_vega_est.rfind("(")+1: fishLC50class_vega_est.index("reliability")].strip()
			stat["average"] = fishLC50class_vega_est_v
			stat["minimum"] = fishLC50class_vega_est_v
			stat["maximum"] = fishLC50class_vega_est_v
			stat["sample_size"] = 1
			stat["standard"] = 0

			if "good" in fishLC50class_vega_est_r:
				stat["note"] = "high"
			elif "low" in fishLC50class_vega_est_r:
				stat["note"] = "low"
			else:
				stat["note"] = "medium"			

			stat["source"] = "VEGA"
			stat["unit"] = "N/A"
	return stat


"""
	fishLC50: Fish Acute LC50 (mg/L)
		VEGA
"""
def parse_fishLC50_stat(vega_json, index):
	# first experimental data
	fishLC50_vega_exp = [vega_json[index]["Fish Acute (LC50) Toxicity model (KNN/Read-Across) - experimental value"],
							vega_json[index]["Fish Acute (LC50) Toxicity model (NIC) - experimental value"]]
	if fishLC50_vega_exp[0] != "N/A" or fishLC50_vega_exp[1] != "N/A":
		# Note: ignore the unit transformation, directly use the value in the assessment
		#       which is in mg/L
		fishLC50_vega_exp1 = vega_json[index]["Fish Acute (LC50) Toxicity model (KNN/Read-Across) - assessment"]
		fishLC50_vega_exp1 = fishLC50_vega_exp1[:fishLC50_vega_exp1.index("mg/L")].strip()
		fishLC50_vega_exp2 = vega_json[index]["Fish Acute (LC50) Toxicity model (NIC) - assessment"]
		fishLC50_vega_exp2 = fishLC50_vega_exp2[:fishLC50_vega_exp2.index("mg/L")].strip()
		fishLC50_vega_exp = [fishLC50_vega_exp1, fishLC50_vega_exp2]
		fishLC50_vega_exp = floatList(fishLC50_vega_exp)
		return getgeoStat(fishLC50_vega_exp, "exp", "VEGA", "mg/L")
	else:
		# look at estimation data
		fishLC50_vega_est = [vega_json[index]["Fish Acute (LC50) Toxicity model (KNN/Read-Across) - assessment"],
								vega_json[index]["Fish Acute (LC50) Toxicity model (NIC) - assessment"]]
		if "good" in fishLC50_vega_est[0]:
			if "good" in fishLC50_vega_est[1]:
				fishLC50_vega_est_v = []
				for fishLC50_vega_est_ins in fishLC50_vega_est:
					fishLC50_vega_est_v.append(fishLC50_vega_est_ins[:fishLC50_vega_est_ins.index("mg/L")].strip())
				fishLC50_vega_est_v = floatList(fishLC50_vega_est_v)
				return getgeoStat(fishLC50_vega_est_v, "high", "VEGA", "mg/L")
			else:
				fishLC50_vega_est_ins = fishLC50_vega_est[0]
				fishLC50_vega_est_ins = fishLC50_vega_est_ins[:fishLC50_vega_est_ins.index("mg/L")].strip()
				fishLC50_vega_est_v = [fishLC50_vega_est_ins]
				fishLC50_vega_est_v = floatList(fishLC50_vega_est_v)
				return getgeoStat(fishLC50_vega_est_v, "high", "VEGA", "mg/L")
		elif "moderate" in fishLC50_vega_est[0]:
			if "good" in fishLC50_vega_est[1]:
				fishLC50_vega_est_ins = fishLC50_vega_est[1]
				fishLC50_vega_est_ins = fishLC50_vega_est_ins[:fishLC50_vega_est_ins.index("mg/L")].strip()
				fishLC50_vega_est_v = [fishLC50_vega_est_ins]
				fishLC50_vega_est_v = floatList(fishLC50_vega_est_v)
				return getgeoStat(fishLC50_vega_est_v, "high", "VEGA", "mg/L")
			elif "moderate" in fishLC50_vega_est[1]:
				fishLC50_vega_est_v = []
				for fishLC50_vega_est_ins in fishLC50_vega_est:
					fishLC50_vega_est_v.append(fishLC50_vega_est_ins[:fishLC50_vega_est_ins.index("mg/L")].strip())
				fishLC50_vega_est_v = floatList(fishLC50_vega_est_v)
				return getgeoStat(fishLC50_vega_est_v, "medium", "VEGA", "mg/L")
			else:
				fishLC50_vega_est_ins = fishLC50_vega_est[0]
				fishLC50_vega_est_ins = fishLC50_vega_est_ins[:fishLC50_vega_est_ins.index("mg/L")].strip()
				fishLC50_vega_est_v = [fishLC50_vega_est_ins]
				fishLC50_vega_est_v = floatList(fishLC50_vega_est_v)
				return getgeoStat(fishLC50_vega_est_v, "medium", "VEGA", "mg/L")
		elif "low" in fishLC50_vega_est[0]:
			if "good" in fishLC50_vega_est[1]:
				fishLC50_vega_est_ins = fishLC50_vega_est[1]
				fishLC50_vega_est_ins = fishLC50_vega_est_ins[:fishLC50_vega_est_ins.index("mg/L")].strip()
				fishLC50_vega_est_v = [fishLC50_vega_est_ins]
				fishLC50_vega_est_v = floatList(fishLC50_vega_est_v)
				return getgeoStat(fishLC50_vega_est_v, "high", "VEGA", "mg/L")
			elif "moderate" in fishLC50_vega_est[1]:
				fishLC50_vega_est_ins = fishLC50_vega_est[1]
				fishLC50_vega_est_ins = fishLC50_vega_est_ins[:fishLC50_vega_est_ins.index("mg/L")].strip()
				fishLC50_vega_est_v = [fishLC50_vega_est_ins]
				fishLC50_vega_est_v = floatList(fishLC50_vega_est_v)
				return getgeoStat(fishLC50_vega_est_v, "medium", "VEGA", "mg/L")
			elif "low" in fishLC50_vega_est[1]:
				fishLC50_vega_est_v = []
				for fishLC50_vega_est_ins in fishLC50_vega_est:
					fishLC50_vega_est_v.append(fishLC50_vega_est_ins[:fishLC50_vega_est_ins.index("mg/L")].strip())
				fishLC50_vega_est_v = floatList(fishLC50_vega_est_v)
				return getgeoStat(fishLC50_vega_est_v, "low", "VEGA", "mg/L")
			else:
				fishLC50_vega_est_ins = fishLC50_vega_est[0]
				fishLC50_vega_est_ins = fishLC50_vega_est_ins[:fishLC50_vega_est_ins.index("mg/L")].strip()
				fishLC50_vega_est_v = [fishLC50_vega_est_ins]
				fishLC50_vega_est_v = floatList(fishLC50_vega_est_v)
				return getgeoStat(fishLC50_vega_est_v, "low", "VEGA", "mg/L")
		else:	#"N/A" for the fishLC50_vega_est[0]
			if "good" in fishLC50_vega_est[1]:
				fishLC50_vega_est_ins = fishLC50_vega_est[1]
				fishLC50_vega_est_ins = fishLC50_vega_est_ins[:fishLC50_vega_est_ins.index("mg/L")].strip()
				fishLC50_vega_est_v = [fishLC50_vega_est_ins]
				fishLC50_vega_est_v = floatList(fishLC50_vega_est_v)
				return getgeoStat(fishLC50_vega_est_v, "high", "VEGA", "mg/L")
			elif "moderate" in fishLC50_vega_est[1]:
				fishLC50_vega_est_ins = fishLC50_vega_est[1]
				fishLC50_vega_est_ins = fishLC50_vega_est_ins[:fishLC50_vega_est_ins.index("mg/L")].strip()
				fishLC50_vega_est_v = [fishLC50_vega_est_ins]
				fishLC50_vega_est_v = floatList(fishLC50_vega_est_v)
				return getgeoStat(fishLC50_vega_est_v, "medium", "VEGA", "mg/L")
			elif "low" in fishLC50_vega_est[1]:
				fishLC50_vega_est_ins = fishLC50_vega_est[1]
				fishLC50_vega_est_ins = fishLC50_vega_est_ins[:fishLC50_vega_est_ins.index("mg/L")].strip()
				fishLC50_vega_est_v = [fishLC50_vega_est_ins]
				fishLC50_vega_est_v = floatList(fishLC50_vega_est_v)
				return getgeoStat(fishLC50_vega_est_v, "low", "VEGA", "mg/L")
			else:
				fishLC50_vega_est_v = ["N/A", "N/A"]
				return getgeoStat(fishLC50_vega_est_v, "N/A", "VEGA", "mg/L")


"""
	fmLC50: fathead minnow LC50 96h (mg/L)
		TEST & VEGA
"""
def parse_fmLC50_stat(vega_json, test_json, index):
	# experimental data first
	fmlc_test_exp = [test_json[index]["Fathead minnow LC50 (96 hr)  Exp_Value:mg/L"]]
	fmlc_test_exp = floatList(fmlc_test_exp)
	fmlc_vega_exp = [vega_json[index]["Fathead Minnow LC50 96h (EPA) - experimental value"]]
	fmlc_vega_exp = floatList(fmlc_vega_exp)
	if fmlc_test_exp[0] != "N/A" and fmlc_vega_exp[0] != "N/A":
		# Note: ignore the unit transformation, directly use the value in the assessment
		#       which is in mg/L
		fmlc_vega_exp1 = vega_json[index]["Fathead Minnow LC50 96h (EPA) - assessment"]
		fmlc_vega_exp1 = fmlc_vega_exp1[:fmlc_vega_exp1.index("mg/L")].strip()
		fmlc_exp = [fmlc_test_exp[0], fmlc_vega_exp1]
		fmlc_exp = floatList(fmlc_exp)
		return getgeoStat(fmlc_exp, "exp", "TEST & VEGA", "mg/L")
	elif fmlc_test_exp[0] != "N/A":
		fmlc_exp = [fmlc_test_exp[0]]
		return getgeoStat(fmlc_exp, "exp", "TEST", "mg/L")
	elif fmlc_vega_exp[0] != "N/A":
		# Note: ignore the unit transformation, directly use the value in the assessment
		#       which is in mg/L
		fmlc_vega_exp1 = vega_json[index]["Fathead Minnow LC50 96h (EPA) - assessment"]
		fmlc_vega_exp1 = fmlc_vega_exp1[:fmlc_vega_exp1.index("mg/L")].strip()
		fmlc_exp = [fmlc_vega_exp1]
		fmlc_exp = floatList(fmlc_exp)
		return getgeoStat(fmlc_exp, "exp", "VEGA", "mg/L")
	else:
		# look at estimation data
		fmlc_test_est = [test_json[index]["Fathead minnow LC50 (96 hr)  Pred_Value:mg/L"]]
		fmlc_test_est = floatList(fmlc_test_est)
		fmlc_vega_est = [vega_json[index]["Fathead Minnow LC50 96h (EPA) - assessment"]]
		if "good" in fmlc_vega_est[0]:
			if fmlc_test_est[0] != "N/A":
				fmlc_vega_est_v = fmlc_vega_est[0]
				fmlc_vega_est_v = fmlc_vega_est_v[:fmlc_vega_est_v.index("mg/L")].strip()
				fmlc_est = [fmlc_vega_est_v, fmlc_test_est[0]]
				fmlc_est = floatList(fmlc_est)
				return getgeoStat(fmlc_est, "high", "TEST & VEGA", "mg/L")
			else:
				fmlc_vega_est_v = fmlc_vega_est[0]
				fmlc_vega_est_v = fmlc_vega_est_v[:fmlc_vega_est_v.index("mg/L")].strip()
				fmlc_est = [fmlc_vega_est_v]
				fmlc_est = floatList(fmlc_est)
				return getgeoStat(fmlc_est, "high", "VEGA", "mg/L")
		elif "moderate" in fmlc_vega_est[0]:
			if fmlc_test_est[0] != "N/A":
				fmlc_vega_est_v = fmlc_vega_est[0]
				fmlc_vega_est_v = fmlc_vega_est_v[:fmlc_vega_est_v.index("mg/L")].strip()
				fmlc_est = [fmlc_vega_est_v, fmlc_test_est[0]]
				fmlc_est = floatList(fmlc_est)
				return getgeoStat(fmlc_est, "medium", "TEST & VEGA", "mg/L")
			else:
				fmlc_vega_est_v = fmlc_vega_est[0]
				fmlc_vega_est_v = fmlc_vega_est_v[:fmlc_vega_est_v.index("mg/L")].strip()
				fmlc_est = [fmlc_vega_est_v]
				fmlc_est = floatList(fmlc_est)
				return getgeoStat(fmlc_est, "medium", "VEGA", "mg/L")
		elif "low" in fmlc_vega_est[0]:
			if fmlc_test_est[0] != "N/A":
				fmlc_est = [fmlc_test_est[0]]
				fmlc_est = floatList(fmlc_est)
				return getgeoStat(fmlc_est, "medium", "TEST", "mg/L")
			else:
				fmlc_vega_est_v = fmlc_vega_est[0]
				fmlc_vega_est_v = fmlc_vega_est_v[:fmlc_vega_est_v.index("mg/L")].strip()
				fmlc_est = [fmlc_vega_est_v]
				fmlc_est = floatList(fmlc_est)
				return getgeoStat(fmlc_est, "low", "VEGA", "mg/L")
		else:	# fmlc_vega_est[0] == "N/A"
			if fmlc_test_est[0] != "N/A":
				fmlc_est = [fmlc_test_est[0]]
				fmlc_est = floatList(fmlc_est)
				return getgeoStat(fmlc_est, "medium", "TEST", "mg/L")
			else:
				fmlc_est = ["N/A", "N/A"]
				fmlc_est = floatList(fmlc_est)
				return getgeoStat(fmlc_est, "N/A", "TEST & VEGA", "mg/L")


"""
	dmLC50: Daphnia Magna LC50 48h (mg/L)
		TEST & VEGA
"""
def parse_dmLC50_stat(vega_json, test_json,epi_json, index):
	# experimental data first

	dmlconeexp=vega_json[index]["Daphnia Magna LC50 48h (DEMETRA) - assessment"]
	dmlctwoexp=vega_json[index]["Daphnia Magna LC50 48h (EPA) - assessment"]
	if "EXPERIMENTAL" in dmlconeexp:
		dmlcone=dmlconeexp[:dmlconeexp.index("mg/L")].strip()
	else:
		dmlcone="N/A"
	
	if "EXPERIMENTAL" in dmlctwoexp:
		dmlctwo=dmlctwoexp[:dmlctwoexp.index("mg/L")].strip()
	else:
		dmlctwo="N/A"	
		


	dmlc_test_exp = [test_json[index]["Daphnia magna LC50 (48 hr)  Exp_Value:mg/L"]]
	dmlc_test_exp = floatList(dmlc_test_exp)
	#dmlc_vega_exp = [vega_json[index]["Daphnia Magna LC50 48h (DEMETRA) - experimental value"],vega_json[index]["Daphnia Magna LC50 48h (EPA) - experimental value"]]
	dmlc_vega_exp = [dmlcone,dmlctwo]	
	dmlc_vega_exp = floatList(dmlc_vega_exp)
	

	if dmlc_test_exp[0] != "N/A" and (dmlc_vega_exp[0] != "N/A" or dmlc_vega_exp[1] != "N/A" ):
		# Note: ignore the unit transformation, directly use the value in the assessment
		#       which is in mg/L
		#dmlc_vega_exp1 = vega_json[index]["Daphnia Magna LC50 48h (DEMETRA) - experimental value"]
		#dmlc_vega_exp2 = vega_json[index]["Daphnia Magna LC50 48h (EPA) - experimental value"]
		#dmlc_vega_exp1 = dmlc_vega_exp1[:dmlc_vega_exp1.index("mg/L")].strip()
		#dmlc_vega_exp2 = dmlc_vega_exp2[:dmlc_vega_exp2.index("mg/L")].strip()
		dmlc_exp = [dmlc_test_exp[0], dmlcone, dmlctwo]
		dmlc_exp = floatList(dmlc_exp)
		return getgeoStat(dmlc_exp, "exp", "TEST & VEGA", "mg/L")
	elif dmlc_test_exp[0] != "N/A" and dmlc_vega_exp[0] == "N/A" and dmlc_vega_exp[1] == "N/A":
		dmlc_exp = [dmlc_test_exp[0]]
		return getgeoStat(dmlc_exp, "exp", "TEST", "mg/L")
	elif dmlc_vega_exp[0] != "N/A" or dmlc_vega_exp[1] != "N/A":
		# Note: ignore the unit transformation, directly use the value in the assessment
		#       which is in mg/L
		#dmlc_vega_exp1 = vega_json[index]["Daphnia Magna LC50 48h (DEMETRA) - experimental value"]
		#dmlc_vega_exp2 = vega_json[index]["Daphnia Magna LC50 48h (EPA) - experimental value"]
		#dmlc_vega_exp1 = dmlc_vega_exp1[:dmlc_vega_exp1.index("mg/L")].strip()
		#dmlc_vega_exp2 = dmlc_vega_exp2[:dmlc_vega_exp2.index("mg/L")].strip()
		dmlc_exp = [dmlcone, dmlctwo]
		dmlc_exp = floatList(dmlc_exp)
		return getgeoStat(dmlc_exp, "exp", "VEGA", "mg/L")
	else:
		# look at estimation data
		dmlc_test_est = [test_json[index]["Daphnia magna LC50 (48 hr)  Pred_Value:mg/L"]]
		dmlc_test_est = floatList(dmlc_test_est)
		dmlc_vega_est = [vega_json[index]["Daphnia Magna LC50 48h (DEMETRA) - assessment"],
							vega_json[index]["Daphnia Magna LC50 48h (EPA) - assessment"]]
		dmlc_epi_est=epi_json[index]["dmLC50_48hr_ecosar  mg/L"]

		if "good" in dmlc_vega_est[0] or "good" in dmlc_vega_est[1]:
			if dmlc_test_est[0] != "N/A":
				if "good" in dmlc_vega_est[0] and "good" in dmlc_vega_est[1]:
					dmlc_vega_est_v1 = dmlc_vega_est[0]
					dmlc_vega_est_v1 = dmlc_vega_est_v1[:dmlc_vega_est_v1.index("mg/L")].strip()
					dmlc_vega_est_v2 = dmlc_vega_est[1]
					dmlc_vega_est_v2 = dmlc_vega_est_v2[:dmlc_vega_est_v2.index("mg/L")].strip()
					dmlc_est = [dmlc_vega_est_v1, dmlc_vega_est_v2, dmlc_test_est[0]]
					dmlc_est = floatList(dmlc_est)
					return getgeoStat(dmlc_est, "high", "TEST & VEGA", "mg/L")
				elif "good" in dmlc_vega_est[0]:
					dmlc_vega_est_v1 = dmlc_vega_est[0]
					dmlc_vega_est_v1 = dmlc_vega_est_v1[:dmlc_vega_est_v1.index("mg/L")].strip()
					dmlc_est = [dmlc_vega_est_v1, dmlc_test_est[0]]
					dmlc_est = floatList(dmlc_est)
					return getgeoStat(dmlc_est, "high", "TEST & VEGA", "mg/L")
				else:
					dmlc_vega_est_v2 = dmlc_vega_est[1]
					dmlc_vega_est_v2 = dmlc_vega_est_v2[:dmlc_vega_est_v2.index("mg/L")].strip()
					dmlc_est = [dmlc_vega_est_v2, dmlc_test_est[0]]
					dmlc_est = floatList(dmlc_est)
					return getgeoStat(dmlc_est, "high", "TEST & VEGA", "mg/L")
			else:
				if "good" in dmlc_vega_est[0] and "good" in dmlc_vega_est[1]:
					dmlc_vega_est_v1 = dmlc_vega_est[0]
					dmlc_vega_est_v1 = dmlc_vega_est_v1[:dmlc_vega_est_v1.index("mg/L")].strip()
					dmlc_vega_est_v2 = dmlc_vega_est[1]
					dmlc_vega_est_v2 = dmlc_vega_est_v2[:dmlc_vega_est_v2.index("mg/L")].strip()
					dmlc_est = [dmlc_vega_est_v1, dmlc_vega_est_v2]
					dmlc_est = floatList(dmlc_est)
					return getgeoStat(dmlc_est, "high", "VEGA", "mg/L")
				elif "good" in dmlc_vega_est[0]:
					dmlc_vega_est_v1 = dmlc_vega_est[0]
					dmlc_vega_est_v1 = dmlc_vega_est_v1[:dmlc_vega_est_v1.index("mg/L")].strip()
					dmlc_est = [dmlc_vega_est_v1]
					dmlc_est = floatList(dmlc_est)
					return getgeoStat(dmlc_est, "high", "VEGA", "mg/L")
				else:
					dmlc_vega_est_v2 = dmlc_vega_est[1]
					dmlc_vega_est_v2 = dmlc_vega_est_v2[:dmlc_vega_est_v2.index("mg/L")].strip()
					dmlc_est = [dmlc_vega_est_v2]
					dmlc_est = floatList(dmlc_est)
					return getgeoStat(dmlc_est, "high", "VEGA", "mg/L")

		elif "moderate" in dmlc_vega_est[0] or "moderate" in dmlc_vega_est[1]:

			if dmlc_test_est[0] != "N/A":

				if dmlc_epi_est!="N/A":
					dmlc_est = [dmlc_test_est[0],dmlc_epi_est]
					dmlc_est = floatList(dmlc_est)
					return getgeoStat(dmlc_est, "medium", "TEST & EPI", "mg/L")
				else:
					dmlc_est=[dmlc_test_est[0]]
					return getgeoStat(dmlc_est, "medium", "TEST", "mg/L")
			else:
				if "moderate" in dmlc_vega_est[0] and "moderate" in dmlc_vega_est[1]:
					dmlc_vega_est_v1 = dmlc_vega_est[0]
					dmlc_vega_est_v1 = dmlc_vega_est_v1[:dmlc_vega_est_v1.index("mg/L")].strip()
					dmlc_vega_est_v2 = dmlc_vega_est[1]
					dmlc_vega_est_v2 = dmlc_vega_est_v2[:dmlc_vega_est_v2.index("mg/L")].strip()

					if dmlc_epi_est!="N/A":
						dmlc_est = [dmlc_vega_est_v1, dmlc_vega_est_v2,dmlc_epi_est]
						dmlc_est = floatList(dmlc_est)
						return getgeoStat(dmlc_est, "medium", "VEGA & EPI Suite", "mg/L")						
					else:
						dmlc_est = [dmlc_vega_est_v1, dmlc_vega_est_v2]
						dmlc_est = floatList(dmlc_est)
						return getgeoStat(dmlc_est, "medium", "VEGA", "mg/L")
				elif "moderate" in dmlc_vega_est[0]:
					dmlc_vega_est_v1 = dmlc_vega_est[0]
					dmlc_vega_est_v1 = dmlc_vega_est_v1[:dmlc_vega_est_v1.index("mg/L")].strip()

					if dmlc_epi_est!="N/A":
						dmlc_est = [dmlc_vega_est_v1,dmlc_epi_est]
						dmlc_est = floatList(dmlc_est)
						return getgeoStat(dmlc_est, "medium", "VEGA", "mg/L")						
					else:
						dmlc_est = [dmlc_vega_est_v1]
						dmlc_est = floatList(dmlc_est)
						return getgeoStat(dmlc_est, "medium", "VEGA", "mg/L")
				else:
					dmlc_vega_est_v2 = dmlc_vega_est[1]
					dmlc_vega_est_v2 = dmlc_vega_est_v2[:dmlc_vega_est_v2.index("mg/L")].strip()

					if dmlc_epi_est!="N/A":
						dmlc_est = [dmlc_vega_est_v2,dmlc_epi_est]
						dmlc_est = floatList(dmlc_est)
						return getgeoStat(dmlc_est, "medium", "VEGA", "mg/L")						
					else:
						dmlc_est = [dmlc_vega_est_v2]
						dmlc_est = floatList(dmlc_est)
						return getgeoStat(dmlc_est, "medium", "VEGA", "mg/L")

		elif dmlc_epi_est!="N/A":
			dmlc_est = [dmlc_epi_est]
			dmlc_est = floatList(dmlc_est)
			return getgeoStat(dmlc_est, "medium", "EPI Suite", "mg/L")			
		elif "low" in dmlc_vega_est[0] or "low" in dmlc_vega_est[1]:
			if dmlc_test_est[0] != "N/A":
				dmlc_est = [dmlc_test_est[0]]
				dmlc_est = floatList(dmlc_est)
				return getgeoStat(dmlc_est, "medium", "TEST", "mg/L")
			elif dmlc_vega_est[0]!="N/A" and dmlc_vega_est[1]!="N/A":
				dmlc_vega_est_v1 = dmlc_vega_est[0]
				dmlc_vega_est_v1 = dmlc_vega_est_v1[:dmlc_vega_est_v1.index("mg/L")].strip()
				dmlc_vega_est_v2 = dmlc_vega_est[1]
				dmlc_vega_est_v2 = dmlc_vega_est_v2[:dmlc_vega_est_v2.index("mg/L")].strip()
				dmlc_est = [dmlc_vega_est_v1, dmlc_vega_est_v2]
				dmlc_est = floatList(dmlc_est)
				return getgeoStat(dmlc_est, "low", "VEGA", "mg/L")
		elif dmlc_vega_est[0] == "N/A" and dmlc_vega_est[1] == "N/A":
			if dmlc_test_est[0] != "N/A":
				dmlc_est = [dmlc_test_est[0]]
				dmlc_est = floatList(dmlc_est)
				return getgeoStat(dmlc_est, "medium", "TEST", "mg/L")
			else:
				dmlc_est = ["N/A", "N/A", "N/A"]
				return getgeoStat(dmlc_est, "N/A", "TEST & VEGA", "mg/L")
		else:
			dmlc_est = ["N/A", "N/A", "N/A"]
			return getgeoStat(dmlc_est, "N/A", "TEST & VEGA", "mg/L")


"""
	mutaTox: Mutagenicity (yes/no)
		TEST & VEGA
"""
def parse_mutaTox_stat(vega_json, test_json, index):
	# experimental data first
	stat = {}
	mutaTox_test_exp = [test_json[index]["Mutagenicity  Exp_Result"]]
	mutaTox_vega_exp = [vega_json[index]["Mutagenicity (Ames test) model (CAESAR) - experimental value"],
						vega_json[index]["Mutagenicity (Ames test) model (ISS) - experimental value"],
						vega_json[index]["Mutagenicity (Ames test) model (KNN/Read-Across) - experimental value"],
						vega_json[index]["Mutagenicity (Ames test) model (SarPy/IRFMN) - experimental value"]]
	mutaTox_test_exp_pos = 0;
	mutaTox_test_exp_neg = 0;
	mutaTox_test_exp_nonclass = 0;
	# note: Only see positive...
	if mutaTox_test_exp[0] == "Mutagenicity Negative":
		mutaTox_test_exp_neg += 1
	elif mutaTox_test_exp[0] != "N/A":
		mutaTox_test_exp_pos += 1
	mutaTox_test_exp_total = mutaTox_test_exp_pos + mutaTox_test_exp_neg + mutaTox_test_exp_nonclass 
	mutaTox_vega_exp_pos = 0;
	mutaTox_vega_exp_neg = 0;
	mutaTox_vega_exp_nonclass = 0;	
	for mutaTox_vega_exp_ins in mutaTox_vega_exp:
		if mutaTox_vega_exp_ins != "N/A":
			if "Possible" in mutaTox_vega_exp_ins:
				mutaTox_vega_exp_nonclass += 1
			elif "NON" in mutaTox_vega_exp_ins:
				mutaTox_vega_exp_neg += 1
			else:
				mutaTox_vega_exp_pos += 1
	mutaTox_vega_exp_total = mutaTox_vega_exp_pos + mutaTox_vega_exp_neg + mutaTox_vega_exp_nonclass 
	mutaTox_exp_pos = mutaTox_test_exp_pos + mutaTox_vega_exp_pos
	mutaTox_exp_neg = mutaTox_test_exp_neg + mutaTox_vega_exp_neg
	mutaTox_exp_nonclass = mutaTox_test_exp_nonclass + mutaTox_vega_exp_nonclass
	if (mutaTox_vega_exp_total + mutaTox_test_exp_total) > 0:
		if mutaTox_test_exp_total > 0 and mutaTox_vega_exp_total > 0:
				stat["source"] = "VEGA & TEST"
		elif mutaTox_test_exp_total > 0:
			stat["source"] = "TEST"
		else:
			stat["source"] = "VEGA"
		stat["count_positive"] = mutaTox_exp_pos
		stat["count_negative"] = mutaTox_exp_neg
		stat["count_not_classified"] = mutaTox_exp_nonclass
		stat["sample_size"] = mutaTox_vega_exp_total + mutaTox_test_exp_total
		stat["note"] = "exp"
		stat["unit"] = "N/A"
		if mutaTox_exp_pos >= mutaTox_exp_neg and mutaTox_exp_pos >= mutaTox_exp_nonclass:
			stat["average"] = "positive"			
			return stat
		elif mutaTox_exp_nonclass >= mutaTox_exp_pos and mutaTox_exp_nonclass >= mutaTox_exp_neg:
			stat["average"] = "not classifiable"
			return stat
		else:
			stat["average"] = "negative"
			return stat
	else:
		# look at estimation data
		mutaTox_test_est = [test_json[index]["Mutagenicity  Pred_Result"]]
		mutaTox_vega_est = [vega_json[index]["Mutagenicity (Ames test) model (CAESAR) - assessment"],
							vega_json[index]["Mutagenicity (Ames test) model (ISS) - assessment"],
							vega_json[index]["Mutagenicity (Ames test) model (KNN/Read-Across) - assessment"],
							vega_json[index]["Mutagenicity (Ames test) model (SarPy/IRFMN) - assessment"]]
		mutaTox_test_est_pos = 0;
		mutaTox_test_est_neg = 0;
		mutaTox_test_est_nonclass = 0;
		if mutaTox_test_est[0] == "Mutagenicity Negative":
			mutaTox_test_est_neg += 1
		elif mutaTox_test_est[0] != "N/A":
			mutaTox_test_est_pos += 1
		mutaTox_test_est_total = mutaTox_test_est_pos + mutaTox_test_est_neg + mutaTox_test_est_nonclass 
		mutaTox_vega_est_pos = 0;
		mutaTox_vega_est_neg = 0;
		mutaTox_vega_est_nonclass = 0;
		mutaTox_vega_est_good = []
		mutaTox_vega_est_moderate = []
		mutaTox_vega_est_low = []
		for mutaTox_vega_est_ins in mutaTox_vega_est:
			if "good" in mutaTox_vega_est_ins:
				mutaTox_vega_est_good.append(mutaTox_vega_est_ins)
			elif "moderate" in mutaTox_vega_est_ins:
				mutaTox_vega_est_moderate.append(mutaTox_vega_est_ins)
			elif "low" in mutaTox_vega_est_ins:
				mutaTox_vega_est_low.append(mutaTox_vega_est_ins)
		if len(mutaTox_vega_est_good) >= 1:
			for mutaTox_vega_est_good_ins in mutaTox_vega_est_good:
				if "Possible" in mutaTox_vega_est_good_ins or "NON" in mutaTox_vega_est_good_ins:
					mutaTox_vega_est_neg += 1
				else:
					mutaTox_vega_est_pos += 1
			mutaTox_vega_est_total = mutaTox_vega_est_neg + mutaTox_vega_est_pos
			mutaTox_est_pos = mutaTox_vega_est_pos + mutaTox_test_est_pos
			mutaTox_est_neg = mutaTox_vega_est_neg + mutaTox_test_est_neg
			if mutaTox_test_est_total >= 1:
				stat["source"] = "VEGA & TEST"
			else:
				stat["source"] = "VEGA"
			stat["count_positive"] = mutaTox_est_pos
			stat["count_negative"] = mutaTox_est_neg
			stat["count_not_classified"] = mutaTox_test_est_nonclass + mutaTox_vega_est_nonclass
			stat["sample_size"] = mutaTox_vega_est_total + mutaTox_test_est_total
			stat["note"] = "high"
			stat["unit"] = "N/A"
			if mutaTox_est_pos >= mutaTox_est_neg:
				stat["average"] = "positive"
			else:
				stat["average"] = "negative"
			return stat
		elif len(mutaTox_vega_est_moderate) >= 1:
			for mutaTox_vega_est_moderate_ins in mutaTox_vega_est_moderate:
				if "Possible" in mutaTox_vega_est_moderate_ins:
					mutaTox_vega_est_nonclass += 1
				elif "NON" in mutaTox_vega_est_moderate_ins:
					mutaTox_vega_est_neg += 1
				else:
					mutaTox_vega_est_pos += 1
			mutaTox_vega_est_total = mutaTox_vega_est_nonclass + mutaTox_vega_est_neg + mutaTox_vega_est_pos
			mutaTox_est_pos = mutaTox_vega_est_pos + mutaTox_test_est_pos
			mutaTox_est_neg = mutaTox_vega_est_neg + mutaTox_test_est_neg
			mutaTox_est_nonclass = mutaTox_test_est_nonclass + mutaTox_vega_est_nonclass
			if mutaTox_test_est_total >= 1:
				stat["source"] = "VEGA & TEST"
			else:
				stat["source"] = "VEGA"
			stat["count_positive"] = mutaTox_est_pos
			stat["count_negative"] = mutaTox_est_neg
			stat["count_not_classified"] = mutaTox_est_nonclass
			stat["sample_size"] = mutaTox_vega_est_total + mutaTox_test_est_total
			stat["note"] = "medium"
			stat["unit"] = "N/A"
			if mutaTox_est_pos >= mutaTox_est_neg and mutaTox_est_pos >= mutaTox_est_nonclass:
				stat["average"] = "positive"
			elif mutaTox_est_nonclass >= mutaTox_est_neg and mutaTox_est_nonclass >= mutaTox_est_pos:
				stat["average"] = "not classifiable"
			else:
				stat["average"] = "negative"
			return stat
		elif len(mutaTox_vega_est_low) >= 1 and mutaTox_test_est_total == 0:
			for mutaTox_vega_est_low_ins in mutaTox_vega_est_low:
				if "Possible" in mutaTox_vega_est_low_ins:
					mutaTox_vega_est_nonclass += 1
				elif "NON" in mutaTox_vega_est_low_ins:
					mutaTox_vega_est_neg += 1
				else:
					mutaTox_vega_est_pos += 1
			mutaTox_vega_est_total = mutaTox_vega_est_nonclass + mutaTox_vega_est_neg + mutaTox_vega_est_pos
			mutaTox_est_pos = mutaTox_vega_est_pos + mutaTox_test_est_pos
			mutaTox_est_neg = mutaTox_vega_est_neg + mutaTox_test_est_neg
			mutaTox_est_nonclass = mutaTox_test_est_nonclass + mutaTox_vega_est_nonclass
			if mutaTox_test_est_total >= 1:
				stat["source"] = "VEGA & TEST"
			else:
				stat["source"] = "VEGA"
			stat["count_positive"] = mutaTox_est_pos
			stat["count_negative"] = mutaTox_est_neg
			stat["count_not_classified"] = mutaTox_est_nonclass
			stat["sample_size"] = mutaTox_vega_est_total + mutaTox_test_est_total
			stat["note"] = "low"
			stat["unit"] = "N/A"
			if mutaTox_est_pos >= mutaTox_est_neg and mutaTox_est_pos >= mutaTox_est_nonclass:
				stat["average"] = "positive"
			elif mutaTox_est_nonclass >= mutaTox_est_neg and mutaTox_est_nonclass >= mutaTox_est_pos:
				stat["average"] = "not classifiable"
			else:
				stat["average"] = "negative"
			return stat
		elif mutaTox_test_est_total != 0:
			stat["source"] = "TEST"
			stat["count_positive"] = mutaTox_test_est_pos
			stat["count_negative"] = mutaTox_test_est_neg
			stat["count_not_classified"] = mutaTox_test_est_nonclass
			stat["sample_size"] = mutaTox_test_est_total
			stat["note"] = "medium"
			stat["unit"] = "N/A"
			if mutaTox_test_est_pos >= mutaTox_test_est_neg:
				stat["average"] = "positive"
			else:
				stat["average"] = "negative"
			return stat
		else:	# all N/A
			stat["source"] = "VEGA & TEST"
			stat["count_positive"] = 0
			stat["count_negative"] = 0
			stat["count_not_classified"] = 0
			stat["ss"] = 0
			stat["note"] = "N/A"
			stat["unit"] = "N/A"
			stat["average"] = "N/A"
			return stat


"""
	carciTox: Carcinogenicity (yes/no)
		VEGA
"""
def parse_carciTox_stat(vega_json, index):
	num_p="count_positive"
	num_n="count_negative"
	num_nc="count_not_classified"
	ss="sample_size"
	avg="average"	
	
	# experimental data first
	stat = {}
	carciTox_vega_exp = [vega_json[index]["Carcinogenicity model (CAESAR) - experimental value"],
							vega_json[index]["Carcinogenicity model (IRFMN/Antares) - experimental value"],
							vega_json[index]["Carcinogenicity model (IRFMN/ISSCAN-CGX) - experimental value"],
							vega_json[index]["Carcinogenicity model (ISS) - experimental value"]]
	carciTox_vega_exp_pos = 0;
	carciTox_vega_exp_neg = 0;
	carciTox_vega_exp_nonclass = 0;	
	for carciTox_vega_exp_ins in carciTox_vega_exp:
		if carciTox_vega_exp_ins != "N/A":
			if "Possible" in carciTox_vega_exp_ins:
				carciTox_vega_exp_nonclass += 1
			elif "NON" in carciTox_vega_exp_ins:
				carciTox_vega_exp_neg += 1
			else:
				carciTox_vega_exp_pos += 1
	carciTox_vega_exp_total = carciTox_vega_exp_pos + carciTox_vega_exp_neg + carciTox_vega_exp_nonclass 
	if carciTox_vega_exp_total > 0:
		stat["source"] = "VEGA"
		stat[num_p] = carciTox_vega_exp_pos
		stat[num_n] = carciTox_vega_exp_neg
		stat[num_nc] = carciTox_vega_exp_nonclass
		stat[ss] = carciTox_vega_exp_total
		stat["note"] = "exp"
		stat["unit"] = "N/A"
		if carciTox_vega_exp_pos >= carciTox_vega_exp_neg and carciTox_vega_exp_pos >= carciTox_vega_exp_nonclass:
			stat[avg] = "positive"			
			return stat
		elif carciTox_vega_exp_nonclass >= carciTox_vega_exp_pos and carciTox_vega_exp_nonclass >= carciTox_vega_exp_neg:
			stat[avg] = "not classifiable"
			return stat
		else:
			stat[avg] = "negative"
			return stat
	else:
		# look at estimation data
		carciTox_vega_est = [vega_json[index]["Carcinogenicity model (CAESAR) - assessment"],
								vega_json[index]["Carcinogenicity model (IRFMN/Antares) - assessment"],
								vega_json[index]["Carcinogenicity model (IRFMN/ISSCAN-CGX) - assessment"],
								vega_json[index]["Carcinogenicity model (ISS) - experimental value"]]
		carciTox_vega_est_pos = 0;
		carciTox_vega_est_neg = 0;
		carciTox_vega_est_nonclass = 0;
		carciTox_vega_est_good = []
		carciTox_vega_est_moderate = []
		carciTox_vega_est_low = []
		for carciTox_vega_est_ins in carciTox_vega_est:
			if "good" in carciTox_vega_est_ins:
				carciTox_vega_est_good.append(carciTox_vega_est_ins)
			elif "moderate" in carciTox_vega_est_ins:
				carciTox_vega_est_moderate.append(carciTox_vega_est_ins)
			elif "low" in carciTox_vega_est_ins:
				carciTox_vega_est_low.append(carciTox_vega_est_ins)
		if len(carciTox_vega_est_good) >= 1:
			for carciTox_vega_est_good_ins in carciTox_vega_est_good:
				if "Possible" in carciTox_vega_est_good_ins or "NON" in carciTox_vega_est_good_ins:
					carciTox_vega_est_neg += 1
				else:
					carciTox_vega_est_pos += 1
			carciTox_vega_est_total = carciTox_vega_est_neg + carciTox_vega_est_pos
			carciTox_est_pos = carciTox_vega_est_pos
			carciTox_est_neg = carciTox_vega_est_neg
			stat["source"] = "VEGA"
			stat[num_p] = carciTox_est_pos
			stat[num_n] = carciTox_est_neg
			stat[num_nc] = carciTox_vega_est_nonclass
			stat[ss] = carciTox_vega_est_total
			stat["note"] = "high"
			stat["unit"] = "N/A"
			if carciTox_est_pos >= carciTox_est_neg:
				stat[avg] = "positive"
			else:
				stat[avg] = "negative"
			return stat
		elif len(carciTox_vega_est_moderate) >= 1:
			for carciTox_vega_est_moderate_ins in carciTox_vega_est_moderate:
				if "Possible" in carciTox_vega_est_moderate_ins:
					carciTox_vega_est_nonclass += 1
				elif "NON" in carciTox_vega_est_moderate_ins:
					carciTox_vega_est_neg += 1
				else:
					carciTox_vega_est_pos += 1
			carciTox_vega_est_total = carciTox_vega_est_nonclass + carciTox_vega_est_neg + carciTox_vega_est_pos
			carciTox_est_pos = carciTox_vega_est_pos
			carciTox_est_neg = carciTox_vega_est_neg
			carciTox_est_nonclass = carciTox_vega_est_nonclass
			stat["source"] = "VEGA"
			stat[num_p] = carciTox_est_pos
			stat[num_n] = carciTox_est_neg
			stat[num_nc] = carciTox_est_nonclass
			stat[ss] = carciTox_vega_est_total
			stat["note"] = "medium"
			stat["unit"] = "N/A"
			if carciTox_est_pos >= carciTox_est_neg and carciTox_est_pos >= carciTox_est_nonclass:
				stat[avg] = "positive"
			elif carciTox_est_nonclass >= carciTox_est_neg and carciTox_est_nonclass >= carciTox_est_pos:
				stat[avg] = "not classifiable"
			else:
				stat[avg] = "negative"
			return stat
		elif len(carciTox_vega_est_low) >= 1:
			for carciTox_vega_est_low_ins in carciTox_vega_est_low:
				if "Possible" in carciTox_vega_est_low_ins:
					carciTox_vega_est_nonclass += 1
				elif "NON" in carciTox_vega_est_low_ins:
					carciTox_vega_est_neg += 1
				else:
					carciTox_vega_est_pos += 1
			carciTox_vega_est_total = carciTox_vega_est_nonclass + carciTox_vega_est_neg + carciTox_vega_est_pos
			carciTox_est_pos = carciTox_vega_est_pos
			carciTox_est_neg = carciTox_vega_est_neg
			carciTox_est_nonclass = carciTox_vega_est_nonclass
			stat["source"] = "VEGA"
			stat[num_p] = carciTox_est_pos
			stat[num_n] = carciTox_est_neg
			stat[num_nc] = carciTox_est_nonclass
			stat[ss] = carciTox_vega_est_total
			stat["note"] = "low"
			stat["unit"] = "N/A"
			if carciTox_est_pos >= carciTox_est_neg and carciTox_est_pos >= carciTox_est_nonclass:
				stat[avg] = "positive"
			elif carciTox_est_nonclass >= carciTox_est_neg and carciTox_est_nonclass >= carciTox_est_pos:
				stat[avg] = "not classifiable"
			else:
				stat[avg] = "negative"
			return stat
		else:	# all N/A
			stat["source"] = "VEGA"
			stat[num_p] = 0
			stat[num_n] = 0
			stat[num_nc] = 0
			stat[ss] = 0
			stat["note"] = "N/A"
			stat["unit"] = "N/A"
			stat[avg] = "N/A"
			return stat


"""
	deveTox: Developmental Toxicity (yes/no)
		TEST & VEGA
"""
def parse_deveTox_stat(vega_json, test_json, index):
	num_p="count_positive"
	num_n="count_negative"
	num_nc="count_not_classified"
	ss="sample_size"
	avg="average"	


	# experimental data first
	stat = {}
	deveTox_test_exp = [test_json[index]["Developmental Toxicity  Exp_Value"]]
	deveTox_vega_exp = [vega_json[index]["Developmental Toxicity model (CAESAR) - experimental value"],
						vega_json[index]["Developmental/Reproductive Toxicity library (PG) - experimental value"]]
	deveTox_test_exp_pos = 0;
	deveTox_test_exp_neg = 0;
	deveTox_test_exp_nonclass = 0;
	# note: Only see positive...
	if "NON" in deveTox_test_exp[0]:
		deveTox_test_exp_neg += 1
	elif deveTox_test_exp[0] != "N/A":
		deveTox_test_exp_pos += 1
	deveTox_test_exp_total = deveTox_test_exp_pos + deveTox_test_exp_neg + deveTox_test_exp_nonclass 
	deveTox_vega_exp_pos = 0;
	deveTox_vega_exp_neg = 0;
	deveTox_vega_exp_nonclass = 0;	
	for deveTox_vega_exp_ins in deveTox_vega_exp:
		if deveTox_vega_exp_ins != "N/A":
			if "Possible" in deveTox_vega_exp_ins:
				deveTox_vega_exp_nonclass += 1
			elif "NON" in deveTox_vega_exp_ins:
				deveTox_vega_exp_neg += 1
			else:
				deveTox_vega_exp_pos += 1
	deveTox_vega_exp_total = deveTox_vega_exp_pos + deveTox_vega_exp_neg + deveTox_vega_exp_nonclass 
	deveTox_exp_pos = deveTox_test_exp_pos + deveTox_vega_exp_pos
	deveTox_exp_neg = deveTox_test_exp_neg + deveTox_vega_exp_neg
	deveTox_exp_nonclass = deveTox_test_exp_nonclass + deveTox_vega_exp_nonclass
	if (deveTox_vega_exp_total + deveTox_test_exp_total) > 0:
		if deveTox_test_exp_total > 0 and deveTox_vega_exp_total > 0:
				stat["source"] = "VEGA & TEST"
		elif deveTox_test_exp_total > 0:
			stat["source"] = "TEST"
		else:
			stat["source"] = "VEGA"
		stat[num_p] = deveTox_exp_pos
		stat[num_n] = deveTox_exp_neg
		stat[num_nc] = deveTox_exp_nonclass
		stat[ss] = deveTox_vega_exp_total + deveTox_test_exp_total
		stat["note"] = "exp"
		stat["unit"] = "N/A"
		if deveTox_exp_pos >= deveTox_exp_neg and deveTox_exp_pos >= deveTox_exp_nonclass:
			stat[avg] = "positive"			
			return stat
		elif deveTox_exp_nonclass >= deveTox_exp_pos and deveTox_exp_nonclass >= deveTox_exp_neg:
			stat[avg] = "not classifiable"
			return stat
		else:
			stat[avg] = "negative"
			return stat
	else:
		# look at estimation data
		deveTox_test_est = [test_json[index]["Developmental Toxicity  Pred_Result"]]
		deveTox_vega_est = [vega_json[index]["Developmental Toxicity model (CAESAR) - assessment"],
							vega_json[index]["Developmental/Reproductive Toxicity library (PG) - assessment"]]
		deveTox_test_est_pos = 0;
		deveTox_test_est_neg = 0;
		deveTox_test_est_nonclass = 0;
		if "NON" in deveTox_test_est[0]:
			deveTox_test_est_neg += 1
		elif deveTox_test_est[0] != "N/A":
			deveTox_test_est_pos += 1
		deveTox_test_est_total = deveTox_test_est_pos + deveTox_test_est_neg + deveTox_test_est_nonclass 
		deveTox_vega_est_pos = 0;
		deveTox_vega_est_neg = 0;
		deveTox_vega_est_nonclass = 0;
		deveTox_vega_est_good = []
		deveTox_vega_est_moderate = []
		deveTox_vega_est_low = []
		for deveTox_vega_est_ins in deveTox_vega_est:
			if "good" in deveTox_vega_est_ins:
				deveTox_vega_est_good.append(deveTox_vega_est_ins)
			elif "moderate" in deveTox_vega_est_ins:
				deveTox_vega_est_moderate.append(deveTox_vega_est_ins)
			elif "low" in deveTox_vega_est_ins:
				deveTox_vega_est_low.append(deveTox_vega_est_ins)
		if len(deveTox_vega_est_good) >= 1:
			for deveTox_vega_est_good_ins in deveTox_vega_est_good:
				if "Possible" in deveTox_vega_est_good_ins or "NON" in deveTox_vega_est_good_ins:
					deveTox_vega_est_neg += 1
				else:
					deveTox_vega_est_pos += 1
			deveTox_vega_est_total = deveTox_vega_est_neg + deveTox_vega_est_pos
			deveTox_est_pos = deveTox_vega_est_pos + deveTox_test_est_pos
			deveTox_est_neg = deveTox_vega_est_neg + deveTox_test_est_neg
			if deveTox_test_est_total >= 1:
				stat["source"] = "VEGA & TEST"
			else:
				stat["source"] = "VEGA"
			stat[num_p] = deveTox_est_pos
			stat[num_n] = deveTox_est_neg
			stat[num_nc] = deveTox_test_est_nonclass + deveTox_vega_est_nonclass
			stat[ss] = deveTox_vega_est_total + deveTox_test_est_total
			stat["note"] = "high"
			stat["unit"] = "N/A"
			if deveTox_est_pos >= deveTox_est_neg:
				stat[avg] = "positive"
			else:
				stat[avg] = "negative"
			return stat
		elif len(deveTox_vega_est_moderate) >= 1:
			for deveTox_vega_est_moderate_ins in deveTox_vega_est_moderate:
				if "Possible" in deveTox_vega_est_moderate_ins:
					deveTox_vega_est_nonclass += 1
				elif "NON" in deveTox_vega_est_moderate_ins:
					deveTox_vega_est_neg += 1
				else:
					deveTox_vega_est_pos += 1
			deveTox_vega_est_total = deveTox_vega_est_nonclass + deveTox_vega_est_neg + deveTox_vega_est_pos
			deveTox_est_pos = deveTox_vega_est_pos + deveTox_test_est_pos
			deveTox_est_neg = deveTox_vega_est_neg + deveTox_test_est_neg
			deveTox_est_nonclass = deveTox_test_est_nonclass + deveTox_vega_est_nonclass
			if deveTox_test_est_total >= 1:
				stat["source"] = "VEGA & TEST"
			else:
				stat["source"] = "VEGA"
			stat[num_p] = deveTox_est_pos
			stat[num_n] = deveTox_est_neg
			stat[num_nc] = deveTox_est_nonclass
			stat[ss] = deveTox_vega_est_total + deveTox_test_est_total
			stat["note"] = "medium"
			stat["unit"] = "N/A"
			if deveTox_est_pos >= deveTox_est_neg and deveTox_est_pos >= deveTox_est_nonclass:
				stat[avg] = "positive"
			elif deveTox_est_nonclass >= deveTox_est_neg and deveTox_est_nonclass >= deveTox_est_pos:
				stat[avg] = "not classifiable"
			else:
				stat[avg] = "negative"
			return stat
		elif len(deveTox_vega_est_low) >= 1 and deveTox_test_est_total == 0:
			for deveTox_vega_est_low_ins in deveTox_vega_est_low:
				if "Possible" in deveTox_vega_est_low_ins:
					deveToxvega_est_nonclass += 1
				elif "NON" in deveTox_vega_est_low_ins:
					deveTox_vega_est_neg += 1
				else:
					deveTox_vega_est_pos += 1
			deveTox_vega_est_total = deveTox_vega_est_nonclass + deveTox_vega_est_neg + deveTox_vega_est_pos
			deveTox_est_pos = deveTox_vega_est_pos + deveTox_test_est_pos
			deveTox_est_neg = deveTox_vega_est_neg + deveTox_test_est_neg
			deveTox_est_nonclass = deveTox_test_est_nonclass + deveTox_vega_est_nonclass
			if deveTox_test_est_total >= 1:
				stat["source"] = "VEGA & TEST"
			else:
				stat["source"] = "VEGA"
			stat[num_p] = deveTox_est_pos
			stat[num_n] = deveTox_est_neg
			stat[num_nc] = deveTox_est_nonclass
			stat[ss] = deveTox_vega_est_total + deveTox_test_est_total
			stat["note"] = "low"
			stat["unit"] = "N/A"
			if deveTox_est_pos >= deveTox_est_neg and deveTox_est_pos >= deveTox_est_nonclass:
				stat[avg] = "positive"
			elif deveTox_est_nonclass >= deveTox_est_neg and deveTox_est_nonclass >= deveTox_est_pos:
				stat[avg] = "not classifiable"
			else:
				stat[avg] = "negative"
			return stat
		elif deveTox_test_est_total != 0:
			stat["source"] = "TEST"
			stat[num_p] = deveTox_test_est_pos
			stat[num_n] = deveTox_test_est_neg
			stat[num_nc] = deveTox_test_est_nonclass
			stat[ss] = deveTox_test_est_total
			stat["note"] = "medium"
			stat["unit"] = "N/A"
			if deveTox_test_est_pos >= deveTox_test_est_neg:
				stat[avg] = "positive"
			else:
				stat[avg] = "negative"
			return stat
		else:	# all N/A
			stat["source"] = "VEGA & TEST"
			stat[num_p] = 0
			stat[num_n] = 0
			stat[num_nc] = 0
			stat[ss] = 0
			stat["note"] = "N/A"
			stat["unit"] = "N/A"
			stat[avg] = "N/A"
			return stat


"""
	ER: Estogen Receptor (yes/no)
		VEGA
"""
def parse_ER_stat(vega_json, index):
	num_p="count_positive"
	num_n="count_negative"
	num_nc="count_not_classified"
	ss="sample_size"
	avg="average"	


	# experimental data first
	stat = {}
	ER_vega_exp = [vega_json[index]["Estrogen Receptor Relative Binding Affinity model (IRFMN) - experimental value"],
							vega_json[index]["Estrogen Receptor-mediated effect (IRFMN/CERAPP) - experimental value"]]
	ER_vega_exp_pos = 0;
	ER_vega_exp_neg = 0;
	ER_vega_exp_nonclass = 0;	
	for ER_vega_exp_ins in ER_vega_exp:
		if ER_vega_exp_ins != "N/A":
			if "Possible" in ER_vega_exp_ins or "Not predicted" in ER_vega_exp_ins:
				ER_vega_exp_nonclass += 1
			elif "NON" in ER_vega_exp_ins or "Inactive" in ER_vega_exp_ins:
				ER_vega_exp_neg += 1
			else:
				ER_vega_exp_pos += 1
	ER_vega_exp_total = ER_vega_exp_pos + ER_vega_exp_neg + ER_vega_exp_nonclass 
	if ER_vega_exp_total > 0:
		stat["source"] = "VEGA"
		stat[num_p] = ER_vega_exp_pos
		stat[num_n] = ER_vega_exp_neg
		stat[num_nc] = ER_vega_exp_nonclass
		stat[ss] = ER_vega_exp_total
		stat["note"] = "exp"
		stat["unit"] = "N/A"
		if ER_vega_exp_pos >= ER_vega_exp_neg and ER_vega_exp_pos >= ER_vega_exp_nonclass:
			stat[avg] = "positive"			
			return stat
		elif ER_vega_exp_nonclass >= ER_vega_exp_pos and ER_vega_exp_nonclass >= ER_vega_exp_neg:
			stat[avg] = "not classifiable"
			return stat
		else:
			stat[avg] = "negative"
			return stat
	else:
		# look at estimation data
		ER_vega_est = [vega_json[index]["Estrogen Receptor Relative Binding Affinity model (IRFMN) - assessment"],
								vega_json[index]["Estrogen Receptor-mediated effect (IRFMN/CERAPP) - assessment"]]
		ER_vega_est_pos = 0;
		ER_vega_est_neg = 0;
		ER_vega_est_nonclass = 0;
		ER_vega_est_good = []
		ER_vega_est_moderate = []
		ER_vega_est_low = []
		for ER_vega_est_ins in ER_vega_est:
			if "good" in ER_vega_est_ins:
				ER_vega_est_good.append(ER_vega_est_ins)
			elif "moderate" in ER_vega_est_ins:
				ER_vega_est_moderate.append(ER_vega_est_ins)
			elif "low" in ER_vega_est_ins:
				ER_vega_est_low.append(ER_vega_est_ins)
		if len(ER_vega_est_good) >= 1:
			for ER_vega_est_good_ins in ER_vega_est_good:
				if "Possible" in ER_vega_est_good_ins or "NON" in ER_vega_est_good_ins or "Inactive" in ER_vega_est_good_ins:
					ER_vega_est_neg += 1
				else:
					ER_vega_est_pos += 1
			ER_vega_est_total = ER_vega_est_neg + ER_vega_est_pos
			ER_est_pos = ER_vega_est_pos
			ER_est_neg = ER_vega_est_neg
			stat["source"] = "VEGA"
			stat[num_p] = ER_est_pos
			stat[num_n] = ER_est_neg
			stat[num_nc] = ER_vega_est_nonclass
			stat[ss] = ER_vega_est_total
			stat["note"] = "high"
			stat["unit"] = "N/A"
			if ER_est_pos >= ER_est_neg:
				stat[avg] = "positive"
			else:
				stat[avg] = "negative"
			return stat
		elif len(ER_vega_est_moderate) >= 1:
			for ER_vega_est_moderate_ins in ER_vega_est_moderate:
				if "Possible" in ER_vega_est_moderate_ins or "Not predicted" in ER_vega_est_moderate_ins:
					ER_vega_est_nonclass += 1
				elif "NON" in ER_vega_est_moderate_ins or "Inactive" in ER_vega_est_moderate_ins:
					ER_vega_est_neg += 1
				else:
					ER_vega_est_pos += 1
			ER_vega_est_total = ER_vega_est_nonclass + ER_vega_est_neg + ER_vega_est_pos
			ER_est_pos = ER_vega_est_pos
			ER_est_neg = ER_vega_est_neg
			ER_est_nonclass = ER_vega_est_nonclass
			stat["source"] = "VEGA"
			stat[num_p] = ER_est_pos
			stat[num_n] = ER_est_neg
			stat[num_nc] = ER_est_nonclass
			stat[ss] = ER_vega_est_total
			stat["note"] = "medium"
			stat["unit"] = "N/A"
			if ER_est_pos >= ER_est_neg and ER_est_pos >= ER_est_nonclass:
				stat[avg] = "positive"
			elif ER_est_nonclass >= ER_est_neg and ER_est_nonclass >= ER_est_pos:
				stat[avg] = "not classifiable"
			else:
				stat[avg] = "negative"
			return stat
		elif len(ER_vega_est_low) >= 1:
			for ER_vega_est_low_ins in ER_vega_est_low:
				if "Possible" in ER_vega_est_low_ins or "Not predicted" in ER_vega_est_low_ins:
					ER_vega_est_nonclass += 1
				elif "NON" in ER_vega_est_low_ins or "Inactive" in ER_vega_est_low_ins:
					ER_vega_est_neg += 1
				else:
					ER_vega_est_pos += 1
			ER_vega_est_total = ER_vega_est_nonclass + ER_vega_est_neg + ER_vega_est_pos
			ER_est_pos = ER_vega_est_pos
			ER_est_neg = ER_vega_est_neg
			ER_est_nonclass = ER_vega_est_nonclass
			stat["source"] = "VEGA"
			stat[num_p] = ER_est_pos
			stat[num_n] = ER_est_neg
			stat[num_nc] = ER_est_nonclass
			stat[ss] = ER_vega_est_total
			stat["note"] = "low"
			stat["unit"] = "N/A"
			if ER_est_pos >= ER_est_neg and ER_est_pos >= ER_est_nonclass:
				stat[avg] = "positive"
			elif ER_est_nonclass >= ER_est_neg and ER_est_nonclass >= ER_est_pos:
				stat[avg] = "not classifiable"
			else:
				stat[avg] = "negative"
			return stat
		else:	# all N/A
			stat["source"] = "VEGA"
			stat[num_p] = 0
			stat[num_n] = 0
			stat[num_nc] = 0
			stat[ss] = 0
			stat["note"] = "N/A"
			stat["unit"] = "N/A"
			stat[avg] = "N/A"
			return stat


"""
	skinSensi: Skin Sensitization (yes/no)
		VEGA
"""
def parse_skinSensi_stat(vega_json, index):
	num_p="count_positive"
	num_n="count_negative"
	num_nc="count_not_classified"
	ss="sample_size"
	avg="average"	



	# experimental data first
	stat = {}
	skinSensi_vega_exp = [vega_json[index]["Skin Sensitization model (CAESAR) - experimental value"]]
	skinSensi_vega_exp_pos = 0;
	skinSensi_vega_exp_neg = 0;
	skinSensi_vega_exp_nonclass = 0;	
	for skinSensi_vega_exp_ins in skinSensi_vega_exp:
		if skinSensi_vega_exp_ins != "N/A":
			if "Possible" in skinSensi_vega_exp_ins:
				skinSensi_vega_exp_nonclass += 1
			elif "NON" in skinSensi_vega_exp_ins:
				skinSensi_vega_exp_neg += 1
			else:
				skinSensi_vega_exp_pos += 1
	skinSensi_vega_exp_total = skinSensi_vega_exp_pos + skinSensi_vega_exp_neg + skinSensi_vega_exp_nonclass 
	if skinSensi_vega_exp_total > 0:
		stat["source"] = "VEGA"
		stat[num_p] = skinSensi_vega_exp_pos
		stat[num_n] = skinSensi_vega_exp_neg
		stat[num_nc] = skinSensi_vega_exp_nonclass
		stat[ss] = skinSensi_vega_exp_total
		stat["note"] = "exp"
		stat["unit"] = "N/A"
		if skinSensi_vega_exp_pos >= skinSensi_vega_exp_neg and skinSensi_vega_exp_pos >= skinSensi_vega_exp_nonclass:
			stat[avg] = "positive"			
			return stat
		elif skinSensi_vega_exp_nonclass >= skinSensi_vega_exp_pos and skinSensi_vega_exp_nonclass >= skinSensi_vega_exp_neg:
			stat[avg] = "not classifiable"
			return stat
		else:
			stat[avg] = "negative"
			return stat
	else:
		# look at estimation data
		skinSensi_vega_est = [vega_json[index]["Skin Sensitization model (CAESAR) - assessment"]]
		skinSensi_vega_est_pos = 0;
		skinSensi_vega_est_neg = 0;
		skinSensi_vega_est_nonclass = 0;
		skinSensi_vega_est_good = []
		skinSensi_vega_est_moderate = []
		skinSensi_vega_est_low = []
		for skinSensi_vega_est_ins in skinSensi_vega_est:
			if "good" in skinSensi_vega_est_ins:
				skinSensi_vega_est_good.append(skinSensi_vega_est_ins)
			elif "moderate" in skinSensi_vega_est_ins:
				skinSensi_vega_est_moderate.append(skinSensi_vega_est_ins)
			elif "low" in skinSensi_vega_est_ins:
				skinSensi_vega_est_low.append(skinSensi_vega_est_ins)
		if len(skinSensi_vega_est_good) >= 1:
			for skinSensi_vega_est_good_ins in skinSensi_vega_est_good:
				if "Possible" in skinSensi_vega_est_good_ins or "NON" in skinSensi_vega_est_good_ins:
					skinSensi_vega_est_neg += 1
				else:
					skinSensi_vega_est_pos += 1
			skinSensi_vega_est_total = skinSensi_vega_est_neg + skinSensi_vega_est_pos
			skinSensi_est_pos = skinSensi_vega_est_pos
			skinSensi_est_neg = skinSensi_vega_est_neg
			stat["source"] = "VEGA"
			stat[num_p] = skinSensi_est_pos
			stat[num_n] = skinSensi_est_neg
			stat[num_nc] = skinSensi_vega_est_nonclass
			stat[ss] = skinSensi_vega_est_total
			stat["note"] = "high"
			stat["unit"] = "N/A"
			if skinSensi_est_pos >= skinSensi_est_neg:
				stat[avg] = "positive"
			else:
				stat[avg] = "negative"
			return stat
		elif len(skinSensi_vega_est_moderate) >= 1:
			for skinSensi_vega_est_moderate_ins in skinSensi_vega_est_moderate:
				if "Possible" in skinSensi_vega_est_moderate_ins:
					skinSensi_vega_est_nonclass += 1
				elif "NON" in skinSensi_vega_est_moderate_ins:
					skinSensi_vega_est_neg += 1
				else:
					skinSensi_vega_est_pos += 1
			skinSensi_vega_est_total = skinSensi_vega_est_nonclass + skinSensi_vega_est_neg + skinSensi_vega_est_pos
			skinSensi_est_pos = skinSensi_vega_est_pos
			skinSensi_est_neg = skinSensi_vega_est_neg
			skinSensi_est_nonclass = skinSensi_vega_est_nonclass
			stat["source"] = "VEGA"
			stat[num_p] = skinSensi_est_pos
			stat[num_n] = skinSensi_est_neg
			stat[num_nc] = skinSensi_est_nonclass
			stat[ss] = skinSensi_vega_est_total
			stat["note"] = "medium"
			stat["unit"] = "N/A"
			if skinSensi_est_pos >= skinSensi_est_neg and skinSensi_est_pos >= skinSensi_est_nonclass:
				stat[avg] = "positive"
			elif skinSensi_est_nonclass >= skinSensi_est_neg and skinSensi_est_nonclass >= skinSensi_est_pos:
				stat[avg] = "not classifiable"
			else:
				stat[avg] = "negative"
			return stat
		elif len(skinSensi_vega_est_low) >= 1:
			for skinSensi_vega_est_low_ins in skinSensi_vega_est_low:
				if "Possible" in skinSensi_vega_est_low_ins:
					skinSensi_vega_est_nonclass += 1
				elif "NON" in skinSensi_vega_est_low_ins:
					skinSensi_vega_est_neg += 1
				else:
					skinSensi_vega_est_pos += 1
			skinSensi_vega_est_total = skinSensi_vega_est_nonclass + skinSensi_vega_est_neg + skinSensi_vega_est_pos
			skinSensi_est_pos = skinSensi_vega_est_pos
			skinSensi_est_neg = skinSensi_vega_est_neg
			skinSensi_est_nonclass = skinSensi_vega_est_nonclass
			stat["source"] = "VEGA"
			stat[num_p] = skinSensi_est_pos
			stat[num_n] = skinSensi_est_neg
			stat[num_nc] = skinSensi_est_nonclass
			stat[ss] = skinSensi_vega_est_total
			stat["note"] = "low"
			stat["unit"] = "N/A"
			if skinSensi_est_pos >= skinSensi_est_neg and skinSensi_est_pos >= skinSensi_est_nonclass:
				stat[avg] = "positive"
			elif skinSensi_est_nonclass >= skinSensi_est_neg and skinSensi_est_nonclass >= skinSensi_est_pos:
				stat[avg] = "not classifiable"
			else:
				stat[avg] = "negative"
			return stat
		else:	# all N/A
			stat["source"] = "VEGA"
			stat[num_p] = 0
			stat[num_n] = 0
			stat[num_nc] = 0
			stat[ss] = 0
			stat["note"] = "N/A"
			stat["unit"] = "N/A"
			stat[avg] = "N/A"
			return stat


"""
	OratLD50: Oral Rat LD 50 (mg/kg)
	  TEST
"""
def parse_OratLD50_stat(test_json, index):
	OratLD50_exp = [test_json[index][u"Oral rat LD50  Exp_Value:mg/kg  C"]]
	OratLD50_exp = floatList(OratLD50_exp)
	OratLD50_exp_stat = getgeoStat(OratLD50_exp, "exp", "TEST", u"mg/kg")
	if OratLD50_exp_stat["average"] == "N/A":
		OratLD50_est = [test_json[index][u"Oral rat LD50  Pred_Value:mg/kg  C"]]
		OratLD50_est = floatList(OratLD50_est)
		OratLD50_est_stat = getgeoStat(OratLD50_est, "medium", "TEST", u"mg/kg")
		return OratLD50_est_stat
	else:
		return OratLD50_exp_stat




#Below functions are all helper functions#
##



def getStat(valueList, note, source, unit):
	# remove N/A
	if "N/A" in valueList or valueList == []:
		if valueList.count("N/A") == len(valueList):	# only has "N/A"
			return {"average":"N/A", 
						"minimum":"N/A",
						"maximum":"N/A",
						"sample_size":len(valueList),
						"standard_deviation":"N/A",
						"note":note,
						"source":source,
						"unit": unit}
		# remove all "N/A"
		# note: if any valid value avaialbe, we do not take into account of "N/A"
		valueList = filter(lambda lbd: lbd != "N/A", valueList)
	stat = {}
	#print ",,,", valueList
	stat["average"] = np.mean(valueList)
	stat["minimum"] = min(valueList)
	stat["maximum"] = max(valueList)
	stat["sample_size"] = len(valueList)
	stat["standard_deviation"] = np.std(valueList)
	stat["note"] = note
	stat["source"] = source
	stat["unit"] = unit

	if stat["sample_size"]==1:
		stat["standard_deviation"]="N/A"
	return stat


def getgeoStat(valueList, note, source, unit):
	# remove N/A
	if "N/A" in valueList or valueList == []:
		if valueList.count("N/A") == len(valueList):	# only has "N/A"
			return {"average":"N/A", 
						"minimum":"N/A",
						"maximum":"N/A",
						"sample_size":len(valueList),
						"standard_deviation":"na",
						"note":note,
						"source":source,
						"unit": unit}
		# remove all "N/A"
		# note: if any valid value avaialbe, we do not take into account of "N/A"
		valueList = filter(lambda lbd: lbd != "N/A", valueList)
	stat = {}
	print ",,,", valueList
	U = reduce(lambda x, y: x*y, valueList)**(1.0/len(valueList))
	stat["average"] = U
	stat["minimum"] = min(valueList)
	stat["maximum"] = max(valueList)
	stat["sample_size"] = len(valueList)

	sumofc=0
	for i in valueList:
		sumofc=sumofc+np.log(i/U)*np.log(i/U)

	O=np.exp(np.sqrt(sumofc/len(valueList)))

	stat["standard_deviation"] = O
	stat["note"] = note
	stat["source"] = source
	stat["unit"] = unit

	if stat["sample_size"]==1:
		stat["standard_deviation"]="N/A"
	return stat




def floatList(list1):
	floatList = []
	for entry in list1:
		if entry == "N/A":
			floatList.append(entry)
		else:
			floatList.append(float(entry))
	return floatList
 

def unLogList(list):
	unLogList = []
	for entry in list:
		if entry == "N/A":
			unLogList.append(entry)
		else:
			unLogList.append(math.pow(10, float(entry)))
	return unLogList


def mmHgToAtm(list):
	atmList = []
	for entry in list:
		if entry == "N/A":
			atmList.append(entry)
		else:
			atmList.append(float(entry)/760)
	return atmList


def mmHgToPa(list):
	paList = []
	for entry in list:
		if entry == "N/A":
			paList.append(entry)
		else:
			paList.append(float(entry) * 133.322365)
	return paList


def readJSON(jsonFilePath):
	with open(jsonFilePath) as jsonFile:
		jsonData = json.load(jsonFile)
		# pprint(jsonData)
	return jsonData





"""
	Ensure that all json file have the same number of chemicals
"""
def ensureSameLength(epi_json, vega_json, test_json):
	# print len(epi_json)
	# print len(vega_json)
	# print len(test_json)
	if len(epi_json) != len(vega_json):
		return False
	if len(epi_json) != len(test_json):
		return False
	return True





if __name__ == '__main__':
	epiJSON = readJSON(EPI_SUITE_SAMPLE_RESULTS_JSON_FILEPATH)
	vegaJSON = readJSON(VEGA_SAMPLE_RESULTS_JSON_FILEPATH)
	testJSON = readJSON(TEST_SAMPLE_RESULTS_JSON_FILEPATH)
	outputFilePath = DEFAULT_JSON_OUTPUT_FILEPATH
	parse(epiJSON, vegaJSON, testJSON, outputFilePath)

#parse(readJSON("/home/yiting/CLiCC/CLiCC_tool_code/modules/qsar/process/1474929739/epi_results.json"), readJSON("/home/yiting/CLiCC/CLiCC_tool_code/modules/qsar/process/1474929739/vega_result/vega_results.json"), readJSON("/home/yiting/CLiCC/CLiCC_tool_code/modules/qsar/process/1474929739/test_result/test_results.json"), "/home/yiting/CLiCC/CLiCC_tool_code/modules/qsar/results/1474929739/qsar_summary.json")
