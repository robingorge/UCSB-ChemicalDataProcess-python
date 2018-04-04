from __future__ import with_statement
import os
import inspect


script_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe()))
)

def get_locations():
    path_array = script_dir.split(os.sep)
    del path_array[-1]
    qsar_dir = (os.sep).join(path_array)
    process_dir = os.path.join(qsar_dir, 'process')
    config_file = os.path.join(process_dir, 'epi_config.txt')

    with open(config_file) as f:
        configTxt = f.readlines()

    configTxt1 = configTxt[0]
    configTxt2 = configTxt[1]

    smiles_location = configTxt1[configTxt1.index(":")+1:].strip()
    results_dir = configTxt2[configTxt2.index(":")+1:].strip()
    log_file = os.path.join(qsar_dir, 'logging', 'logging.txt')

    smiles_location = convertPathLinuxToWindows(smiles_location)
    results_dir = convertPathLinuxToWindows(results_dir)
    log_file = convertPathLinuxToWindows(log_file)

    return {
        'smiles': smiles_location,
        'results': results_dir,
        'log': log_file
    }


# "/home/yiting/Dropbox/Spring2016/CLiCC/ModuleIntegration/clicc-flask-master/modules/qsar/smiles.txt"
# "Z:\home\yiting\Dropbox\Spring2016\CLiCC\ModuleIntegration\clicc-flask-master\modules\qsar\smiles.txt"
def convertPathLinuxToWindows(linuxPath):
    windowsPath = linuxPath
    windowsPath = windowsPath.replace("/","\\")
    windowsPath = "Z:" + windowsPath
    return windowsPath


