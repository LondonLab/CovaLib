import subprocess
import os
import sys
import PyUtils
class Cluster:
	def __init__(self, typ):
		self.typ = typ
	def runJobs(self, dirlist, command):
		f = open(dirlist, 'r')
		for job in f:
			PyUtils.create_folder(job[:-1])
			os.chdir(job[:-1])
			if(self.typ == "CHEM"):
				subprocess.call(["bsub", "-u", "/dev/null", "-R", "rusage[mem=1024]", "-q", "new-all.q", "-o", "out", "-e", "err", command])
			os.chdir("../")
		f.close()
        def runJobsArgs(self, dirlist, command, arglist):
                f = open(dirlist, 'r')
                i = 0
                for job in f:
                        PyUtils.create_folder(job[:-1])
                        os.chdir(job[:-1])
                        if(len(arglist) < i + 1):
                                print "arglist is not the same length as dirlist"
                                sys.exit()
                        if(self.typ == "CHEM"):
                                subprocess.call(["bsub", "-u", "/dev/null", "-R", "rusage[mem=1024]", "-q", "new-all.q", "-o", "out", "-e", "err", command, str(arglist[i])])
                        os.chdir("../")
                        i += 1
                f.close()
        def runJobsName(self, dirlist, command):
                with open(dirlist) as f:
                        lines = f.read().splitlines()
                self.runJobsArgs(dirlist, command, lines)
