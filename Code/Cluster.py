import subprocess
import os
import sys
import PyUtils
import socket
import chemfarm_job_submission as cjob
class Cluster:
	def __init__(self):
		#self.getServer()
		self.typ = "CHEM"
	def runSingle(self, command):
		if(self.typ == "WEXAC"):
			subprocess.call(["bsub", "-u", "/dev/null", "-R", "rusage[mem=1024]", "-q", "new-all.q", "-o", "out", "-e", "err", command])
		if(self.typ == "CHEM"):
			job_file = "job_submission.sh"
			cur_job = open(job_file, 'w')
			for line in cjob.sendjob_text[:7]:
				cur_job.write(line)
			cur_job.write(cjob.sendjob_text[7] + '\'' + command + '\'')
			for line in cjob.sendjob_text[8:]:
				cur_job.write(line)
			cur_job.close()
			subprocess.call(["/gpopt/altair/pbs/default/bin/qsub", job_file])
	def runCommands(self, commands):
		for command in commands:
			self.runSingle(command)
	def runDirSingle(self, dirname, command):
		PyUtils.create_folder(dirname[:-1])
		curr = os.getcwd()
		os.chdir(dirname[:-1])
		self.runSingle(command)
		os.chdir(curr)
	def runDirCommands(self, dirlist, commands):
		self.checkList(dirlist, commands)
		f = open(dirlist, 'r')
		lines = f.readlines()
		for dirname, command in zip(lines, commands):
			self.runDirSingle(dirname, command)
		f.close()
	def runJobs(self, dirlist, command):
		f = open(dirlist, 'r')
		lines = f.readlines()
		commands = [command] * len(lines)
		f.close()
		self.runDirCommands(dirlist, commands)
		
        def runJobsArgs(self, dirlist, command, arglist):
		self.checkList(dirlist, arglist)
		commands = []
		for arg in arglist:
			commands += [command + ' ' + str(arg)]
		self.runDirCommands(dirlist, commands)
	
	def runCommandsArgs(self, command, arglist):
		commands = []
		for arg in arglist:
			commands.append(command + ' ' + str(arg))
		self.runCommands(commands)
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
	def checkList(self, dirlist, l):
		f = open(dirlist, 'r')
		if not len(f.readlines()) == len(l):
			print 'length of list does not match dirlist length'
			sys.exit()
		f.close()
