import subprocess
import os
import sys
import PyUtils
import socket
class Cluster:
	def __init__(self):
		self.getServer()
	def runJobs(self, dirlist, command):
		f = open(dirlist, 'r')
		for job in f:
			PyUtils.create_folder(job[:-1])
			os.chdir(job[:-1])
			if(self.typ == "WEXAC"):
				subprocess.call(["bsub", "-u", "/dev/null", "-R", "rusage[mem=1024]", "-q", "new-all.q", "-o", "out", "-e", "err", command])
			if(self.typ == "CHEM"):
				#print "qsub -q idle " + command
				subprocess.call(["qsub", "-q", "idle", command])
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
                        if(self.typ == "WEXAC"):
                                subprocess.call(["bsub", "-u", "/dev/null", "-R", "rusage[mem=1024]", "-q", "new-all.q", "-o", "out", "-e", "err", command, str(arglist[i])])
                        if(self.typ == "CHEM"):
				subprocess.call(["qsub", "-q", "idle", command])
			os.chdir("../")
                        i += 1
                f.close()
        def runJobsName(self, dirlist, command):
                with open(dirlist) as f:
                        lines = f.read().splitlines()
                self.runJobsArgs(dirlist, command, lines)

	#Inner functions
	def getServer(self):
		server_name = socket.gethostname()
		if 'chemfarm' in server_name:
			self.typ = "CHEM"
		elif 'wexac' in server_name:
			self.typ = "WEXAC"
		else:
			print "This is not a cluster supporting server"
			sys.exit()

