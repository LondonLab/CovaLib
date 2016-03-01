import subprocess
import os
class Cluster:
	def __init__(self, typ):
		self.typ = typ
	def runJobs(self, dirlist, command):
		f = open(dirlist, 'r')
		for job in f:
			os.chdir(job[:-1])
			if(self.typ == "CHEM"):
				subprocess.call(["bsub", "-u", "/dev/null", "-R", "rusage[mem=1024]", "-q", "new-all.q", "-o", "out", "-e", "err", command])
			os.chdir("../")
		f.close()
