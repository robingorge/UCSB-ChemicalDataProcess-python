# -*- coding: utf-8 -*-
'''
Last modified on March 8, 2017

@author: Yiting Ju
'''
import csv
import os
from subprocess import Popen


#default_command = "java -jar ./VEGA_CMD/VEGA-CLI.jar -script ./script_allModule_test"
default_command = "java -jar "+ os.path.dirname(os.path.realpath(__file__)) +"/VEGA_CMD/VEGA-CLI.jar -script ./script_shaoyi"

def construct_script_file(scriptFilePath, smilesSourceFilePath, outputResultFilePath):
	scriptList = ["<vega>", "<input>", "<type>FileSMI</type>"]
	scriptList.append("<source>" + smilesSourceFilePath + "</source>")
	scriptList.append("</input>")
	scriptList.append("<models>")
	scriptList.append("<model>muta_caesar</model>")
	scriptList.append("<model>muta_sarpy</model>")
	scriptList.append("<model>muta_iss</model>")
	scriptList.append("<model>muta_knn</model>")
	scriptList.append("<model>carc_caesar</model>")
	scriptList.append("<model>carc_iss</model>")
	scriptList.append("<model>carc_antares</model>")
	scriptList.append("<model>carc_isscan</model>")
	scriptList.append("<model>devtox_caesar</model>")
	scriptList.append("<model>devtox_pg</model>")
	scriptList.append("<model>rba_irfmn</model>")
	scriptList.append("<model>rba_cerapp</model>")
	scriptList.append("<model>skin_caesar</model>")
	scriptList.append("<model>fish_irfmn</model>")
	scriptList.append("<model>fish_knn</model>")
	scriptList.append("<model>fish_nic</model>")
	scriptList.append("<model>fathead_epa</model>")
	scriptList.append("<model>daphnia_epa</model>")
	scriptList.append("<model>daphnia_demetra</model>")
	scriptList.append("<model>bcf_caesar</model>")
	scriptList.append("<model>bcf_meyla</model>")
	scriptList.append("<model>bcf_knn</model>")
	scriptList.append("<model>rb_irfmn</model>")
	scriptList.append("<model>p_sed_irfmn</model>")
	scriptList.append("<model>p_soil_irfmn</model>")
	scriptList.append("<model>p_water_irfmn</model>")
	scriptList.append("<model>logp_meylan</model>")
	scriptList.append("<model>logp_mlogp</model>")
	scriptList.append("<model>logp_alogp</model>")
	scriptList.append("</models>")
	scriptList.append("<output>")
	scriptList.append("<singleTXT>" + outputResultFilePath + "</singleTXT>")
	scriptList.append("</output>")
	scriptList.append("</vega>")
	scriptFolderPath = os.path.dirname(scriptFilePath)
	if not os.path.exists(scriptFolderPath):
		os.makedirs(scriptFolderPath)
	with open(scriptFilePath, 'wb') as theFile:
		for script in scriptList:
			theFile.write("%s\n" % script)
		



def VEGA_batch_allEndpoints(vegaJarFilePath, scriptFilePath, smilesSourceFilePath, outputResultFilePath):
	construct_script_file(scriptFilePath, smilesSourceFilePath, outputResultFilePath)
	command = "java -jar " + vegaJarFilePath + " -script " + scriptFilePath
	print "Calling", command
	try:
	  	e = Popen(
	      	command,
	      	# cwd="/home/yiting/Downloads/Vega-1.1.1-binaries/vega-cli beta 1_cmd",
	      	cwd = os.path.dirname(vegaJarFilePath),
			shell=True
		)
		stdout, stderr = e.communicate()

	except IOError as (errno,strerror):
		print "I/O error({0}): {1}".format(errno, strerror)
	print "[info] VEGA done >>", outputResultFilePath


if __name__ == "__main__":
	print "VEGA"
    	#VEGA_batch_allEndpoints()
    #construct_script_file("/home/yiting/Downloads/CLiCC/Vega-1.1.1-binaries/vega-cli beta 4/test_ju/#script_test",
    #					"/home/yiting/Downloads/CLiCC/Vega-1.1.1-binaries/vega-cli beta 4/test_ju/source_test.txt",
#					    "/home/yiting/Downloads/CLiCC/Vega-1.1.1-binaries/vega-cli beta 4/test_ju/results/results.txt")
