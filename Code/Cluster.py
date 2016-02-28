import subprocess
class Cluster:
	def __init__(self, typ):
		self.typ = typ
	def runJobs(self, dirlist, command):
		f = open(dirlist, 'r')
		for job in f:
			if(self.typ == "CHEM"):
				subprocess.call(["bsub", "-u", "/dev/null", "-R", "rusage[mem=1024]", "-q", "new-all.q", "-o", "out", "-e", "err", command])
		f.close()
