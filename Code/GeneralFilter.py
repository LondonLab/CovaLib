#Written by Daniel Zaidman
#Code review by 

import shutil
import subprocess
import os
import sys
import Paths
import PyUtils
import Cluster
import Result_List

class GeneralFilter:
    def __init__(self, folder_name, filter_name):
        self.folder_name = folder_name
        self.extract = folder_name + '/extract_all.sort.uniq.txt'
        self.filter = filter_name
        self.filter_folder = folder_name + '/' + filter_name
        PyUtils.create_folder(self.filter_folder)
        self.out_name = filter_name + '/extract_all.' + filter_name
        self.rlist = Result_List.Result_List(self.extract)

    def listFilter(self, f_list):
        os.chdir(self.folder_name)
        self.rlist.writeIndexListObj(f_list, self.out_name)
        subprocess.call([Paths.DOCKBASE + "analysis/getposes.py", "-f", self.out_name, "--ranks", self.out_name, "-o", self.filter + "/poses.mol2"])
        os.chdir('../')
