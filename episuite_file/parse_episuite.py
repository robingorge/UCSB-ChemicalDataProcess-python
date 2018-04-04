import csv, json, pprint, math


# Not used in this file...
# epi_Endpoints =[
# 	'BCF  L/kg wet-wt  Arnot-Gobas',
# 	'BCF  L/kg wet-wt  Regression',
# 	'MW  g/mol',
# 	'Mol Formula',
# 	'SMILES',
# 	'VP  mmHg  est',
# 	'VP  mmHg  exp',
# 	'WS  mg/L  est',
# 	'WS  mg/L  exp',
# 	'WWTP Biodegradation  10000hr',
# 	'WWTP Biodegradation  Biowin/EPA',
# 	'WWTP Removal  10000hr',
# 	'WWTP Removal  Biowin/EPA',
# 	'WWTP Sludge Adsorption  10000hr',
# 	'WWTP Sludge Adsorption  Biowin/EPA',
# 	'WWTP To Air  10000hr',
# 	'WWTP To Air  Biowin/EPA',
# 	'kAerAir  est',
# 	'kAerAir  exp',
# 	'kOrgWater  Kow',
# 	'kOrgWater  MCI',
# 	'kOrgWater  exp',
# 	'DegAir',
# 	'DegSed',
# 	'DegSoil',
# 	'DegWater',
# 	'DegAero',
# 	'DegSSed',
# 	'kOctWater  est',
# 	'kOctWater  exp'
# ]

epi_Endpoints =[
	'BCF  L/kg wet-wt  Arnot-Gobas',
	'BCF  L/kg wet-wt  Regression',
	'MW  g/mol',
	'Mol Formula',
	'SMILES',
	'VP  mmHg  est',
	'VP  mmHg  exp',
	'WS  mg/L  est',
	'WS  mg/L  exp',
	'WWTP Biodegradation  10000hr',
	'WWTP Biodegradation  Biowin/EPA',
	'WWTP Removal  10000hr',
	'WWTP Removal  Biowin/EPA',
	'WWTP Sludge Adsorption  10000hr',
	'WWTP Sludge Adsorption  Biowin/EPA',
	'WWTP To Air  10000hr',
	'WWTP To Air  Biowin/EPA',
	'kAerAir  est',
	'kAerAir  exp',
	'kOrgWater  Kow',
	'kOrgWater  MCI',
	'kOrgWater  exp',
	'DegAir',
	'DegSed',
	'DegSoil',
	'DegWater',
	'DegAero',
	'DegSSed',
	'kOctWater  est',
	'kOctWater  exp',#############change201705
	'BP  C  est',
	'BP  C  exp',
	'MP  C  est',
	'MP  C  exp',
	'Kp  m3/ug  Mackay',
	'kOH_1  cm3/molecule-sec',#299
	'OH_HL  days',#230
	'HLC Bond Pa-m3/mole', #257  
	'HLC Group Pa-m3/mole',
	'biodeg_linear',#################change201706
	'biodeg_nonlinear',
	'biodeg_ultimate',
	'biodeg_primary',
	'biodeg_MITIlinear',
	'biodeg_MITInonlinear',
	'biodeg_anaerobic',
	'biodeg_ready',
	'BioHC_HL  days',
	'Kb_rateC  L/mol-sec',
	'Kb_HL_pH8  days',
	'Kb_HL_pH7  years',
	'biotrans_HL  days',
	'fishLC50_ecosar  mg/L',#################ecostar file
	'dmLC50_ecosar  mg/L',
	'algaeEC50_ecosar  mg/L',
	'fishChV_ecosar  mg/L',
	'dmChV_ecosar  mg/L',
	'algaeChV_ecosar  mg/L',
	'fishLC50SW_ecosar  mg/L',
	'fishChVSW_ecosar  mg/L',
	'mysidSWLC50_ecosar  mg/L',
	'mysidSWChV_ecosar  mg/L',
	'earthworm_ecosar  mg/L'
]


"""
	read the EPI-Suite result file, parse it, and reformat it into JSON format.

	[
		{
 			"SMILES": "c1ccccc1",
 			"Mol Formula": "C18 H32 O16",
 			...
 			...
		},
		{
 			"SMILES": "CC",
 			"Mol Formula": "O10 P3 Na5",
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
def read_epi_result_toJson(resultFilePath, jsonOutputPath="default"):
	# read line by line and store in a list
	ccccc=0
	smilebyline=[]
	smilethere=[]


	fileByLine = []
	with open(resultFilePath) as f:
		fileByLine = f.read().splitlines()
	# split the file by records(chemicals)
	indexesOfRecords = splitTheListByRecords(fileByLine)
	# get rid of the first one which is a placeholder
	indexesOfRecords = indexesOfRecords[0:]
	# read by each record block
	chemicals = []
	for i in range(len(indexesOfRecords)-1):
		# check records one by one
        # record the line count to match each endpoint with the values in output file
		linesForOneRecord = fileByLine[indexesOfRecords[i]:indexesOfRecords[i+1]-1]
		currentChemical = {}
		lineCounter = 0
		for line in linesForOneRecord:
			if "INCOMPATIBLE SMILES" in line:
				tempsmile=line[line.index(":")+1:].strip()
				currentChemical["SMILES"] = tempsmile
			elif "SMILES NOTATION PROBLEM" in line:
				tempsmile=line[line.index(":")+1:].strip()
				print("-------------")
				print(tempsmile)
				currentChemical["SMILES"] = tempsmile
			elif "SMILES :" in line:
				if "SMILES" not in currentChemical:		
					tempSmiles = line[line.index(":")+1:].strip()
					currentChemical["SMILES"] = tempSmiles
			elif "MOL WT :" in line:
				if "MW  g/mol" not in currentChemical:	
					currentChemical["MW  g/mol"] = line[line.index(":")+1:].strip()			
			elif "MOL FOR:" in line:
				if "Mol Formula" not in currentChemical:
					currentChemical["Mol Formula"] = line[line.index(":")+1:].strip()
			elif "CAS Num  :" in line:
				if "CAS" not in currentChemical:
					currentChemical["CAS"] = line[line.index(":")+1:].strip()
			elif "KOWWIN Program (v1.68) Results:" in line:    ###kowin part: dk if i need pow(10,f)
				#print(linesForOneRecord[lineCounter+1])
				i=lineCounter+2
				thisline=linesForOneRecord[i]
				while "==============================="	not in thisline:
					try:
						if "Exp Log P:" in thisline:
							currentChemical["kOctWater  unitless  exp"] = math.pow(10, float(thisline[thisline.index(":")+1:].strip()))
						elif "Log Kow(version 1.68 estimate):" in thisline:
							currentChemical["kOctWater  unitless  est"] = math.pow(10, float(thisline[thisline.index(":")+1:].strip()))
					except Exception:
						pass
					i=i+1
					thisline=linesForOneRecord[i]
			elif "MPBPWIN (v1.43) Program Results:"	in line:
				i=lineCounter+2
				thisline=linesForOneRecord[i]
				while "------------------------ SUMMARY MPBPWIN v1.43 --------------------"	not in thisline:
					try:
						if "Exp MP (deg C):" in thisline:
							if "---" in thisline:
								currentChemical["MP  C  exp"] = "N/A"
							elif "dec" in thisline:
								currentChemical["MP  C  exp"] = str(float(thisline[thisline.index(":")+1:thisline.index("dec")].strip()))
							else:
								currentChemical["MP  C  exp"] = str(float(thisline[thisline.index(":")+1:].strip()))
						elif "Exp BP (deg C):" in thisline:
							if "---" in thisline:
								currentChemical["BP  C  exp"] = "N/A"
							elif "@" in thisline:
								currentChemical["BP  C  exp"] = str(float(thisline[thisline.index(":")+1:thisline.index("@")].strip()))
							else:
								currentChemical["BP  C  exp"] = str(float(thisline[thisline.index(":")+1:].strip()))
						elif "Exp VP (mm Hg):" in thisline:
							if "---" in thisline:
								currentChemical["VP  mmHg  exp"] = "N/A"
							elif "(e" in thisline:
								currentChemical["VP  mmHg  exp"] = str(float(thisline[thisline.index(":")+1:thisline.index("(e")].strip()))
							else:
								currentChemical["VP  mmHg  exp"] = str(float(thisline[thisline.index(":")+1:].strip()))
					except Exception:
						pass
					i=i+1
					thisline=linesForOneRecord[i]

				while "========================================" not in thisline:
					try:
						if "Selected MP:" in thisline:
							currentChemical["MP  C  est"] = str(float(thisline[thisline.index(":")+1:thisline.index("deg")].strip()))
						elif "Boiling Point:" in thisline:
							currentChemical["BP  C  est"] = str(float(thisline[thisline.index(":")+1:thisline.index("deg")].strip()))
						elif "Selected VP:" in thisline:
							currentChemical["VP  mmHg  est"] = str(float(thisline[thisline.index(":")+1:thisline.index("mm")].strip()))
					except Exception:
						pass
					i=i+1
					thisline=linesForOneRecord[i]		
			elif "Water Sol from Kow (WSKOW v1.42) Results:" in line:
				i=lineCounter+2
				thisline=linesForOneRecord[i]
				while "------ WSKOW v1.42 Results -------"	not in thisline:
					try:
					# print("ws")
						if "Water Sol:" in thisline:
							currentChemical["WS  mg/L  WSKOW  est"] = thisline[thisline.index(":")+1:thisline.index("mg/L")].strip()
						# print(currentChemical["WS  mg/L  est"])
						elif "Exp WSol :" in thisline:
							currentChemical["WS  mg/L  WSKOW  exp"] = thisline[thisline.index(":")+1:thisline.index("mg/L")].strip()
						# print(currentChemical["WS  mg/L  exp"])
					except Exception:
						pass
					i=i+1
					thisline=linesForOneRecord[i]
			elif "WATERNT Program (v1.01) Results:" in line:
				i=lineCounter+2
				thisline=linesForOneRecord[i]
				while "========================="  not in thisline:
					try:
						if "Water Sol (v1.01 est):" in thisline:
							currentChemical["WS  mg/L  WATERNT  est"] = thisline[thisline.index(":")+1:thisline.index("mg/L")].strip()
							# print(currentChemical["WS  mg/L  est"])
						elif "Exp WSol :" in thisline:
							currentChemical["WS  mg/L  WATERNT  exp"] = thisline[thisline.index(":")+1:thisline.index("mg/L")].strip()
							# print(currentChemical["WS  mg/L  exp"])
					except Exception:
						pass
					i=i+1
					thisline=linesForOneRecord[i]
			elif "ECOSAR v1.11 Class-specific Estimations" in line:
				i=lineCounter+2
				ttline=linesForOneRecord[i]
				e1=-1
				e2=-1
				e3=-1
				e4=-1
				e5=-1
				e6=-1

				while "----------------------------"  not in ttline:
					try:
						if "Daphnid" in ttline:
							if "LC50" in ttline and "48-hr" in ttline:
								currentChemical["dmLC50_48hr_ecosar  mg/L"]=ttline[66:77].strip()
								e2=float(ttline[66:77].strip())
							if "ChV" in ttline and "-hr" not in ttline:
								currentChemical["dmChV_ecosar  mg/L"]=ttline[66:77].strip()
								e5=float(ttline[66:77].strip())

						if "Green Algae" in ttline:
							if "EC50" in ttline and "96-hr" in ttline:
								currentChemical["algaeEC50_96hr_ecosar  mg/L"]=ttline[66:77].strip()
								e3=float(ttline[66:77].strip())

						if "Fish" in ttline:
							if "(SW)" in ttline:
								if "LC50" in ttline and "96-hr" in ttline:
									currentChemical["fishLC50SW_96hr_ecosar  mg/L"]=ttline[66:77].strip()
								if "ChV" in ttline and "-hr" not in ttline:
									currentChemical["fishChVSW_ecosar  mg/L"]=ttline[66:77].strip()##############should be??
							else:
								if "ChV" in ttline and "-hr" not in ttline:
									currentChemical["fishChV_ecosar  mg/L"]=ttline[66:77].strip()
									e4=float(ttline[66:77].strip())
								if "LC50" in ttline and "96-hr" in ttline:
									currentChemical["fishLC50_96hr_ecosar  mg/L"]=ttline[66:77].strip()
									e1=float(ttline[66:77].strip())

						if "Green Algae" in ttline:
							if "ChV" in ttline and "-hr" not in ttline:
								currentChemical["algaeChV_ecosar  mg/L"]=ttline[66:77].strip()
								e6=float(ttline[66:77].strip())

						if "Mysid (SW)" in ttline:
							if "ChV" in ttline and "-hr" not in ttline:
								currentChemical["shrimpSWChV_ecosar  mg/L"]=ttline[66:77].strip()
						elif "Mysid" in ttline:
							if "LC50" in ttline and "96-hr" in ttline:
								currentChemical["shrimpLC50_96hr_ecosar  mg/L"]=ttline[66:77].strip()

						if "Earthworm" in ttline:
							if "LC50" in ttline and "14-day" in ttline:
								currentChemical["earthworm_14day_ecosar  mg/L"]=ttline[66:77].strip()
								# print(currentChemical["earthworm_ecosar  mg/L"])
					except Exception:
						pass

					i=i+1
					ttline=linesForOneRecord[i]
				#aquaTox_acute
				if e1!=-1 and e2!=-1 and e3!=-1 and e4!=-1 and e5!=-1 and e6!=-1:
					if e1>100 and e2>100 and e3>100 and e4>10 and e5>10 and e6>10:
						currentChemical["aquaTox_acute  unitless"]="low"
					elif (e1<1 and e2<1 and e3<1) or (e4<0.10 and e5<0.10 and e6<0.10):
						currentChemical["aquaTox_acute  unitless"]="high"
					elif (e1>1 and e2>1 and e3>1) or (e4>0.10 and e5>0.10 and e6>0.10):
						currentChemical["aquaTox_acute  unitless"]="medium"


			elif "HENRY (v3.20) Program Results:" in line:
				i=lineCounter+2
				thisline=linesForOneRecord[i]
				while "========================="  not in thisline:
					try:
						# print("ws")
						if "Bond Est :" in thisline:
							currentChemical["HLC  Pa-m3/mole  Bond"] = str(float(thisline[thisline.index("(")+1:thisline.index("Pa")-1].strip()))
						elif "Group Est:" in thisline:
							if "Incomplete" in thisline:
								currentChemical["HLC  Pa-m3/mole  Group"] = "N/A"
							else:
								currentChemical["HLC  Pa-m3/mole  Group"] = str(float(thisline[thisline.index("(")+1:thisline.index("Pa")-1].strip()))
						elif "Exp HLC  :" in thisline:
							currentChemical["HLC  Pa-m3/mole  exp"] = str(float(thisline[thisline.index("(")+1:thisline.index("Pa")-1].strip()))
					except Exception:
						pass
					i=i+1
					thisline=linesForOneRecord[i]
			elif "Log Octanol-Air (KOAWIN v1.10) Results:" in line:################
				i=lineCounter+2
				thisline=linesForOneRecord[i]
				while "========================"  not in thisline:
					# print("ws")
					try:
						if "Log Koa:" in thisline:
							currentChemical["kOctAir  unitless  est"] = math.pow(10,float(thisline[thisline.index(":")+1:].strip()))
						elif "Exp LogKoa:" in thisline:
							currentChemical["kOctAir  unitless  exp"] = math.pow(10,float(thisline[thisline.index(":")+1:].strip()))
						elif "Log Kaw:" in thisline:
							currentChemical["kAirWater  unitless"] = math.pow(10,float(thisline[thisline.index(":")+1:thisline.index("(")].strip()))
					except Exception:
						pass
					i=i+1
					thisline=linesForOneRecord[i]					
			elif "BIOWIN (v4.10) Program Results:" in line:
				i=lineCounter+2
				thisline=linesForOneRecord[i]
				while "-----+-----+--------"  not in thisline:
					try:
						if "Biowin1" in thisline:
							blinear=thisline[(thisline.index(":")+1):].strip()
							if "Not" in blinear:
								currentChemical["biodeg_linear  unitless"]="No"
							else:
								currentChemical["biodeg_linear  unitless"]="Yes"
						elif "Biowin2" in thisline:
							bnonlinear=thisline[(thisline.index(":")+1):].strip()
							if "Not" in blinear:
								currentChemical["biodeg_nonlinear  unitless"]="No"
							else:
								currentChemical["biodeg_nonlinear  unitless"]="Yes"
						elif "Biowin3" in thisline:
							currentChemical["biodeg_ultimate  unitless"]=thisline[(thisline.index(":")+1):].strip()
						elif "Biowin4" in thisline:
							currentChemical["biodeg_primary  unitless"]=thisline[(thisline.index(":")+1):].strip()
						elif "Biowin5" in thisline:
							bMITIlinear=thisline[(thisline.index(":")+1):].strip()
							if "Not" in bMITIlinear:
								currentChemical["biodeg_MITIlinear  unitless"]="No"
							else:
								currentChemical["biodeg_MITIlinear  unitless"]="Yes"
						elif "Biowin6" in thisline:
							bMITInonlinear=thisline[(thisline.index(":")+1):].strip()
							if "Not" in bMITInonlinear:
								currentChemical["biodeg_MITInonlinear  unitless"]="No"
							else:
								currentChemical["biodeg_MITInonlinear  unitless"]="Yes"
						elif "Biowin7" in thisline:
							banaerobic=thisline[(thisline.index(":")+1):].strip()
							if "Not" in banaerobic:
								currentChemical["biodeg_anaerobic  unitless"]="No"
							else:
								currentChemical["biodeg_anaerobic  unitless"]="Yes"
						elif "Ready Biodegradability Prediction" in thisline:
							bready=thisline[(thisline.index(":")+1):].strip()
							if "Not" in bready:
								currentChemical["biodeg_ready  unitless"]="No"
							else:
								currentChemical["biodeg_ready  unitless"]="Yes"
					except Exception:
						pass

					i=i+1
					thisline=linesForOneRecord[i]

				# if "Not" in blinear or "Not" in bnonlinear or "Not" in bMITIlinear or "Not" in bMITInonlinear or "Not" in banaerobic or "No" in bready:
				# 	currentChemical["biodeg_ready_combine  unitless"]="No"
				# else:
				# 	currentChemical["biodeg_ready_combine  unitless"]="Yes"

			elif "BioHCwin (v1.01) Program Results:" in line:
				i=lineCounter+2
				thisline=linesForOneRecord[i]
				while "AEROWIN Program"  not in thisline:
					# print("ws")
					try:
						if "BioHC Half-Life (days)" in thisline:
							if "LOG" not in thisline:
								currentChemical["bioHC_HL  days"]=str(float(thisline[70:].strip()))
					except Exception:
						pass

					i=i+1
					thisline=linesForOneRecord[i]
			elif "AEROWIN Program (v1.00) Results:" in line:
				i=lineCounter+2
				thisline=linesForOneRecord[i]
				while "================="  not in thisline:
					# print("ws")
					try:
						if "Kp (particle/gas partition coef. (m3/ug)):" in thisline:
							nextlinee=linesForOneRecord[i+1]						
							if "Mackay model" in nextlinee:
								if "not" in nextlinee:
									currentChemical["kAerAir  m3/ug  Mackay"]="N/A"
								else:
									currentChemical["kAerAir  m3/ug  Mackay"]=str(float(nextlinee[(nextlinee.index(":")+1):].strip()))
							nextlinee=linesForOneRecord[i+2]
							if "Koa" in nextlinee:
								if "not" in nextlinee or "#" in nextlinee:
									currentChemical["kAerAir  m3/ug  Koa"]="N/A"
								else:
									tempvalue=nextlinee[(nextlinee.index(":")+1):].strip()
									currentChemical["kAerAir  m3/ug  Koa"]=	str(float(tempvalue))
					except Exception:
						pass					
					
					i=i+1
					thisline=linesForOneRecord[i]
			elif "AOP Program (v1.92) Results:" in line:
				i=lineCounter+2
				thisline=linesForOneRecord[i]
				while "OZONE REACTION"  not in thisline:
					# print("ws")
					try:
						if "OVERALL OH Rate Constant" in thisline:
							ohrc=thisline
							tempword=ohrc[ohrc.index("=")+1:ohrc.index("cm3")-1].strip()
							tempword=tempword.replace(" ","")
							currentChemical["kOH  cm3/molecule-sec"]=str(float(tempword))
						elif "HALF-LIFE" in thisline:
							if "Days" in thisline:
								hloh=thisline
								currentChemical["OH_HL  days"]=str(float(hloh[hloh.index("=")+1:hloh.index("Days")-1].strip()))
					except Exception:
						pass
					i=i+1
					thisline=linesForOneRecord[i]
			elif "--- HYDROWIN v2.00 Results ---" in line:####################
				i=lineCounter+2
				thisline=linesForOneRecord[i]
				while "========================"  not in thisline:
					# Kb_HL_pH8 Kb_HL_pH7
					try:
						if "Currently, this program can NOT estimate" in thisline:
							currentChemical["Kb_HL_pH8  days"]="N/A"
							currentChemical["Kb_HL_pH7  days"]="N/A"
							currentChemical["Kb_rateC  L/mol-sec"]="N/A"
							break
						else:
							if "Kb Half-Life at pH 8"  in thisline:
								try:
									if "year" in thisline:
										currentChemical["Kb_HL_pH8  days"]=str(float(thisline[thisline.index(":")+1:thisline.index("year")-1].strip())*365)
									elif "hour" in thisline:
										currentChemical["Kb_HL_pH8  days"]=str(float(thisline[thisline.index(":")+1:thisline.index("hour")-1].strip())/24)
									elif "day" in thisline:
										currentChemical["Kb_HL_pH7  days"]=str(float(thisline[thisline.index(":")+1:thisline.index("day")-1].strip()))								
								except Exception:
									pass
								# else:
								# 	currentChemical["Kb_HL_pH8  days"]="N/A"
							elif "Kb Half-Life at pH 7" in thisline:
								try:
									if "year" in thisline:
										currentChemical["Kb_HL_pH7  days"]=str(float(thisline[thisline.index(":")+1:thisline.index("year")-1].strip())*365)
									elif "hour" in thisline:
										currentChemical["Kb_HL_pH7  days"]=str(float(thisline[thisline.index(":")+1:thisline.index("hour")-1].strip())/24)
									elif "day" in thisline:
										currentChemical["Kb_HL_pH7  days"]=str(float(thisline[thisline.index(":")+1:thisline.index("day")-1].strip()))
								except Exception:
									pass
							elif "Total Kb for pH > 8 at 25 deg C" in thisline and "L/" in thisline:
								currentChemical["Kb_rateC  L/mol-sec"]=str(float(thisline[thisline.index(":")+1:thisline.index("L/")-1].strip()))
					except Exception:
						pass

					i=i+1
					thisline=linesForOneRecord[i]
			elif "KOCWIN Program (v2.00) Results:" in line:
				i=lineCounter+2
				thisline=linesForOneRecord[i]
				while "KOCWIN v2.00 Results"  not in thisline:
					# print("ws")
					try:
						if "Exp LogKoc:" in thisline:
							currentChemical["kOrgWater  L/kg  exp"] = math.pow(10, float(thisline[thisline.index(":")+1:].strip()))
					except Exception:
						pass

					i=i+1
					thisline=linesForOneRecord[i]
			elif "Koc Estimate from MCI:" in line:
				i=lineCounter+2
				thisline=linesForOneRecord[i]
				while "<==========="  not in thisline:
					# print("ws")
					try:
						if "Corrected Log Koc" in thisline:
							currentChemical["kOrgWater  L/kg  MCI"] = math.pow(10,float(thisline[thisline.index(":")+1:].strip()))
					except Exception:
						pass

					i=i+1
					thisline=linesForOneRecord[i]
			elif "Koc Estimate from Log Kow:" in line:
				i=lineCounter+2
				thisline=linesForOneRecord[i]
				while "<==========="  not in thisline:
					# print("ws")
					try:
						if "Corrected Log Koc" in thisline:
							currentChemical["kOrgWater  L/kg  Kow"] = math.pow(10,float(thisline[thisline.index(":")+1:].strip()))
					except Exception:
						pass

					i=i+1
					thisline=linesForOneRecord[i]
			elif "SUMMARY (AOP v1.91): OZONE REACTION (25 deg C)" in line:########################--- HYDROWIN v2.00 Results ---
			## will have > <
				i=lineCounter+2
				thisline=linesForOneRecord[i]
				while "========================"  not in thisline:
					# print("ws")
					try:
						if "Exper Ozone rate constant:" in thisline:
							kor = thisline[thisline.index(":")+1:thisline.index("cm3")-1].strip()
							if kor=="---":
								currentChemical["kO3  cm3/molecule-sec"] = "N/A"
							else:
								currentChemical["kO3  cm3/molecule-sec"] = kor
						elif "Exper NO3 rate constant" in thisline:
							kor = thisline[thisline.index(":")+1:thisline.index("cm3")-1].strip()
							if kor=="---":
								currentChemical["kNO3  cm3/molecule-sec"] = "N/A"
							else:
								currentChemical["kNO3  cm3/molecule-sec"] = kor					
					except Exception:
						pass
					i=i+1
					thisline=linesForOneRecord[i]
			elif "BCFBAF Program (v3.01) Results:" in line:
				i=lineCounter+2
				thisline=linesForOneRecord[i]
				while "======================================="  not in thisline:
					# print("ws")
					try:
						if "Log BCF (regression-based estimate):" in thisline:
							currentChemical["LogBCF  L/kg wet-wt  Regression"] = thisline[thisline.rfind("=")+1:thisline.rfind("L")-1].strip()
						elif "Log BAF (Arnot-Gobas upper trophic):" in thisline:
							currentChemical["LogBCF  L/kg wet-wt  Arnot-Gobas"] = thisline[thisline.rfind("=")+1:thisline.rfind("L")-1].strip()
						elif "Biotransformation Half-Life (days)" in thisline:
							currentChemical["biotrans_HL  days"] = thisline[thisline.rfind(":")+1:thisline.rfind("(")-1].strip()
						elif "Bio Half-life" in thisline:
							currentChemical["bio_HL  days"]= thisline[thisline.rfind("=")+1:thisline.rfind("days")].strip()
					except Exception:
						pass

					i=i+1
					thisline=linesForOneRecord[i]
			elif "Biotransformation Rate Constant:" in line:#########finish
				i=lineCounter+1
				thisline=linesForOneRecord[i]
				while "============"  not in thisline:
					# print("ws")
					try:
						if "kM (Rate Constant)" in thisline:
							if "(10 gram fish)" in thisline:
								aaaaa=thisline[thisline.rfind(":")+1:thisline.rfind("/day")-1].strip()
								if "---" in aaaaa or "n" in aaaaa:
									currentChemical["Km_10  /day"] = "N/A"
								else:
									currentChemical["Km_10  /day"] = aaaaa
					except Exception:
						pass	

					i=i+1
					thisline=linesForOneRecord[i]
			elif "(using 10000 hr Bio P,A,S)" in line:
				i=lineCounter+2
				thisline=linesForOneRecord[i]
				asludge=0
				while "============"  not in thisline:
					try:
						if "Total removal" in thisline:
							removalLine=thisline
							thisspot=removalLine[62:].strip()
							if thisspot!="":
								currentChemical["WWTremoval  %  10000hr"] = thisspot
						elif "Total biodegradation" in thisline:
							biodegLine=thisline
							thisspot=biodegLine[62:].strip()
							if thisspot!="":
								currentChemical["WWTbio  %  10000hr"] = thisspot
						elif "Primary sludge" in thisline:
							asludge=float(thisline[62:].strip())
						elif "Waste sludge" in thisline:	
							sludgeAdsLine=thisline
							thisspot=sludgeAdsLine[62:].strip()
							if thisspot!="":
								currentChemical["WWTslu  %  10000hr"] = str(float(thisspot)+asludge)
						elif "Aeration off gas" in thisline:
							toAirLine=thisline
							thisspot=toAirLine[62:].strip()
							if thisspot!="":
								currentChemical["WWTair  %  10000hr"] = thisspot
					except Exception:
						pass

					i=i+1
					thisline=linesForOneRecord[i]
			elif "(using Biowin/EPA draft method)" in line:
				i=lineCounter+2
				thisline=linesForOneRecord[i]
				asludge=0
				while "============"  not in thisline:
					try:
						if "Total removal" in thisline:
							removalLine=thisline
							thisspot=removalLine[62:].strip()
							if thisspot!="":
								currentChemical["WWTremoval  %  Biowin/EPA"] = thisspot
						elif "Total biodegradation" in thisline:
							biodegLine=thisline
							thisspot=biodegLine[62:].strip()
							if thisspot!="":
								currentChemical["WWTbio  %  Biowin/EPA"] = thisspot
						elif "Primary sludge" in thisline:
							thisspot=thisline[62:].strip()
							if thisspot!="":
								asludge=float(thisspot)
						elif "Waste sludge" in thisline:	
							sludgeAdsLine=thisline
							thisspot=sludgeAdsLine[62:].strip()
							if thisspot!="":
								currentChemical["WWTslu  %  Biowin/EPA"] = str(float(thisspot)+asludge)
						elif "Aeration off gas" in thisline:
							toAirLine=thisline
							thisspot=toAirLine[62:].strip()
							if thisspot!="":
								currentChemical["WWTair  %  Biowin/EPA"] = thisspot
					except Exception:
						pass

					i=i+1
					thisline=linesForOneRecord[i]
			elif "Level III Fugacity Model (Full-Output):" in line:
				i=lineCounter+2
				thisline=linesForOneRecord[i]
				while "Mass Amount    Half-Life    Emissions" not in thisline:
					i=i+1
					thisline=linesForOneRecord[i]

				while "Fugacity    Reaction    Advection   Reaction    Advection"  not in thisline:
					# print("ws")
					try:
						if "Air" in thisline:
							currentChemical["HLDegAir  hour"] = thisline[29:41].strip()
						elif "Water" in thisline:
							currentChemical["HLDegWater  hour"] = thisline[29:41].strip()
						elif "Soil" in thisline:
							currentChemical["HLDegSoil  hour"] = thisline[29:41].strip()
						elif "Sediment" in thisline:
							currentChemical["HLDegSed  hour"] = thisline[29:41].strip()
					except Exception:
						pass

					i=i+1
					thisline=linesForOneRecord[i]

			lineCounter += 1


		# in case some values are not available; also for error smiles
		#   MORE SHALL BE ADDED!
		if "Mol Formula" not in currentChemical:
			currentChemical["Mol Formula"] = "N/A"
		if "MW  g/mol" not in currentChemical:
			currentChemical["MW  g/mol"] = "N/A"

		if "LogBCF  L/kg wet-wt  Regression" not in currentChemical:
			currentChemical["LogBCF  L/kg wet-wt  Regression"] = "N/A"
		if "LogBCF  L/kg wet-wt  Arnot-Gobas" not in currentChemical:
			currentChemical["LogBCF  L/kg wet-wt  Arnot-Gobas"] = "N/A"

		if "kOctWater  unitless  est" not in currentChemical:
			currentChemical["kOctWater  unitless  est"] = "N/A"
		if "kOctWater  unitless  exp" not in currentChemical:
			currentChemical["kOctWater  unitless  exp"] = "N/A"

		if "kOrgWater  L/kg  exp" not in currentChemical:
			currentChemical["kOrgWater  L/kg  exp"] = "N/A"
		if "kOrgWater  L/kg  MCI" not in currentChemical:
			currentChemical["kOrgWater  L/kg  MCI"] = "N/A"
		if "kOrgWater  L/kg  Kow" not in currentChemical:
			currentChemical["kOrgWater  L/kg  Kow"] = "N/A"

		if "kAirWater  unitless" not in currentChemical:
			currentChemical["kAirWater  unitless"] = "N/A"

		if "kOctAir  unitless  exp" not in currentChemical:
			currentChemical["kOctAir  unitless  exp"] = "N/A"
		if "kOctAir  unitless  est" not in currentChemical:
			currentChemical["kOctAir  unitless  est"] = "N/A"

		if "HLDegAir  hour" not in currentChemical:
			currentChemical["HLDegAir  hour"] = "N/A"
		if "HLDegWater  hour" not in currentChemical:
			currentChemical["HLDegWater  hour"] = "N/A"
		if "HLDegSoil  hour" not in currentChemical:
			currentChemical["HLDegSoil  hour"] = "N/A"
		if "HLDegSed  hour" not in currentChemical:
			currentChemical["HLDegSed  hour"] = "N/A"
		if "VP  mmHg  est" not in currentChemical:
			currentChemical["VP  mmHg  est"] = "N/A"
		if "VP  mmHg  exp" not in currentChemical:
			currentChemical["VP  mmHg  exp"] = "N/A"
		if "WS  mg/L  WATERNT  est" not in currentChemical:
			currentChemical["WS  mg/L  WATERNT  est"] = "N/A"
		if "WS  mg/L  WATERNT  exp" not in currentChemical:
			currentChemical["WS  mg/L  WATERNT  exp"] = "N/A"
		if "WS  mg/L  WSKOW  est" not in currentChemical:
			currentChemical["WS  mg/L  WSKOW  est"] = "N/A"
		if "WS  mg/L  WSKOW  exp" not in currentChemical:
			currentChemical["WS  mg/L  WSKOW  exp"] = "N/A"
			###########
		if "WWTremoval  %  10000hr" not in currentChemical:
			currentChemical["WWTremoval  %  10000hr"] = "N/A"
		if "WWTbio  %  10000hr" not in currentChemical:
			currentChemical["WWTbio  %  10000hr"] = "N/A"
		if "WWTslu  %  10000hr" not in currentChemical:
			currentChemical["WWTslu  %  10000hr"] = "N/A"
		if "WWTair  %  10000hr" not in currentChemical:
			currentChemical["WWTair  %  10000hr"] = "N/A"
		if "WWTremoval  %  Biowin/EPA" not in currentChemical:
			currentChemical["WWTremoval  %  Biowin/EPA"] = "N/A"
		if "WWTbio  %  Biowin/EPA" not in currentChemical:
			currentChemical["WWTbio  %  Biowin/EPA"] = "N/A"
		if "WWTslu  %  Biowin/EPA" not in currentChemical:
			currentChemical["WWTslu  %  Biowin/EPA"] = "N/A"
		if "WWTair  %  Biowin/EPA" not in currentChemical:
			currentChemical["WWTair  %  Biowin/EPA"] = "N/A"
			#############change201705
		if "BP  C  est" not in currentChemical:
			currentChemical["BP  C  est"] = "N/A"
		if "BP  C  exp" not in currentChemical:
			currentChemical["BP  C  exp"] = "N/A"
		if "MP  C  est" not in currentChemical:
			currentChemical["MP  C  est"] = "N/A"
		if "MP  C  exp" not in currentChemical:
			currentChemical["MP  C  exp"] = "N/A"
		# if "Kp  m3/ug  Mackay" not in currentChemical:
		# 	currentChemical["Kp  m3/ug  Mackay"] = "N/A"
		if "kAerAir  m3/ug  Mackay" not in currentChemical:
			currentChemical["kAerAir  m3/ug  Mackay"] = "N/A"
		if "kAerAir  m3/ug  Koa" not in currentChemical:
			currentChemical["kAerAir  m3/ug  Koa"] = "N/A"

		if "kOH  cm3/molecule-sec" not in currentChemical:
			currentChemical["kOH  cm3/molecule-sec"] = "N/A"
		if "OH_HL  days" not in currentChemical:
			currentChemical["OH_HL  days"] = "N/A"
		if "HLC  Pa-m3/mole  Bond" not in currentChemical:
			currentChemical["HLC  Pa-m3/mole  Bond"] = "N/A"
		if "HLC  Pa-m3/mole  Group" not in currentChemical:
			currentChemical["HLC  Pa-m3/mole  Group"] = "N/A"
		if "HLC  Pa-m3/mole  exp" not in currentChemical:
			currentChemical["HLC  Pa-m3/mole  exp"] = "N/A"
		# if "HLC Bond Pa-m3/mole" not in currentChemical:
		# 	currentChemical["HLC Bond Pa-m3/mole"] = "N/A"
		# if "HLC Group Pa-m3/mole" not in currentChemical:
		# 	currentChemical["HLC Group Pa-m3/mole"] = "N/A"
		# if "HLC Pa-m3/mole exp" not in currentChemical:
		# 	currentChemical["HLC Pa-m3/mole exp"] = "N/A"
			##############CHANGE201706
		if "biodeg_ultimate  unitless" not in currentChemical:
			currentChemical["biodeg_ultimate  unitless"] = "N/A"			
		if "biodeg_primary  unitless" not in currentChemical:
			currentChemical["biodeg_primary  unitless"] = "N/A"
		if "biodeg_linear  unitless" not in currentChemical:
			currentChemical["biodeg_linear  unitless"] = "N/A"
		if "biodeg_nonlinear  unitless" not in currentChemical:
			currentChemical["biodeg_nonlinear  unitless"] = "N/A"
		if "biodeg_MITIlinear  unitless" not in currentChemical:
			currentChemical["biodeg_MITIlinear  unitless"] = "N/A"
		if "biodeg_MITInonlinear  unitless" not in currentChemical:
			currentChemical["biodeg_MITInonlinear  unitless"] = "N/A"
		if "biodeg_anaerobic  unitless" not in currentChemical:
			currentChemical["biodeg_anaerobic  unitless"] = "N/A"
		if "biodeg_ready  unitless" not in currentChemical:
			currentChemical["biodeg_ready  unitless"] = "N/A"			
		# if "biodeg_ready_combine  unitless" not in currentChemical:
		# 	currentChemical["biodeg_ready_combine  unitless"] = "N/A"
			#################
		if "bioHC_HL  days" not in currentChemical:
			currentChemical["bioHC_HL  days"] = "N/A"
		if "bio_HL  days" not in currentChemical:
			currentChemical["bio_HL  days"] = "N/A"

		if "Kb_rateC  L/mol-sec" not in currentChemical:
			currentChemical["Kb_rateC  L/mol-sec"] = "N/A"
		if "Kb_HL_pH8  days" not in currentChemical:
			currentChemical["Kb_HL_pH8  days"] = "N/A"
		if "Kb_HL_pH7  days" not in currentChemical:
			currentChemical["Kb_HL_pH7  days"] = "N/A"
		if "biotrans_HL  days" not in currentChemical:
			currentChemical["biotrans_HL  days"] = "N/A"
		if "Km_10  /day" not in currentChemical:
			currentChemical["Km_10  /day"] = "N/A"
			##################ecostar
		if "fishLC50_96hr_ecosar  mg/L" not in currentChemical:
			currentChemical["fishLC50_96hr_ecosar  mg/L"] = "N/A"
		if "dmLC50_48hr_ecosar  mg/L" not in currentChemical:
			currentChemical["dmLC50_48hr_ecosar  mg/L"] = "N/A"
		if "algaeEC50_96hr_ecosar  mg/L" not in currentChemical:
			currentChemical["algaeEC50_96hr_ecosar  mg/L"] = "N/A"
		if "fishChV_ecosar  mg/L" not in currentChemical:
			currentChemical["fishChV_ecosar  mg/L"] = "N/A"
		if "dmChV_ecosar  mg/L" not in currentChemical:
			currentChemical["dmChV_ecosar  mg/L"] = "N/A"
		if "algaeChV_ecosar  mg/L" not in currentChemical:
			currentChemical["algaeChV_ecosar  mg/L"] = "N/A"
		if "fishLC50SW_96hr_ecosar  mg/L" not in currentChemical:
			currentChemical["fishLC50SW_96hr_ecosar  mg/L"] = "N/A"
		if "fishChVSW_ecosar  mg/L" not in currentChemical:
			currentChemical["fishChVSW_ecosar  mg/L"] = "N/A"
		if "shrimpLC50_96hr_ecosar  mg/L" not in currentChemical:
			currentChemical["shrimpLC50_96hr_ecosar  mg/L"] = "N/A"
		if "shrimpSWChV_ecosar  mg/L" not in currentChemical:
			currentChemical["shrimpSWChV_ecosar  mg/L"] = "N/A"
		if "earthworm_14day_ecosar  mg/L" not in currentChemical:
			currentChemical["earthworm_14day_ecosar  mg/L"] = "N/A"
			###############
		if "kO3  cm3/molecule-sec" not in currentChemical:
			currentChemical["kO3  cm3/molecule-sec"] = "N/A"
		if "kNO3  cm3/molecule-sec" not in currentChemical:
			currentChemical["kNO3  cm3/molecule-sec"] = "N/A"	
		if "CAS" not in currentChemical:
			currentChemical["CAS"] = "N/A"
		if "aquaTox_acute  unitless" not in currentChemical:
			currentChemical["aquaTox_acute  unitless"] = "N/A"

		currentChemical["HLDegAero  hour"] = currentChemical["HLDegSed  hour"]
		currentChemical["HLDegSsed  hour"] = currentChemical["HLDegSed  hour"]

		chemicals.append(currentChemical)
	# pp = pprint.PrettyPrinter(indent=4)
	# pp.pprint(chemicals)
	# for item in chemicals:
	# 	print len(item)
	# print sorted(chemicals[0].keys())
	# write JSON to file

	#chemicals=add_more_result_toJson(chemicals)
	chemicals.pop(0)

	if jsonOutputPath == "default":
		jsonOutputPath = resultFilePath[:-3]+"json"
	with open(jsonOutputPath, "w") as outputFile:
		json.dump(chemicals, outputFile, sort_keys=True, indent= 4, separators=(',', ': '))




"""
	Split the file(in list) by records(chemicals)
	  return with the indexes of beginning for each record
"""
def splitTheListByRecords(listOfLines):
	indexesOfBeginning = [0]
	index = 0
	for line in listOfLines:
		if line == "========================":
			indexesOfBeginning.append(index+1)
		index += 1

	# indexesOfBeginning.append(index+5)

	return indexesOfBeginning


def readJSON(jsonFilePath):
	with open(jsonFilePath) as jsonFile:
		jsonData = json.load(jsonFile)
		# pprint(jsonData)
	return jsonData

def difference(str1,str2):
	a=filter(str.isalpha, str1.lower())
	b=filter(str.isalpha, str2.lower())
	letterlist=["a","b","c","l","s","i","n","o","h","k","z","g","e","p","r"]
	if len(a)==len(b):
		for u in letterlist:
			if not a.count(u)==b.count(u):
				return False
	else:
		return False

	return True






if __name__ == '__main__':
	import os, inspect
	class_directory = os.path.dirname(os.path.abspath(
		inspect.getfile(inspect.currentframe()))
	)
	read_epi_result_toJson(os.path.join(class_directory, "epibat.out"))
