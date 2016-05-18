import subprocess
import os
import sys
import PyUtils
import socket
import chemfarm_job_submission as cjob
class Cluster:
	def __init__(self):
		self.getServer()
	def runSingle(self, command):
		if(self.typ == "WEXAC"):
			subprocess.call(["bsub", "-u", "/dev/null", "-R", "rusage[mem=1024]", "-q", "new-all.q", "-o", "out", "-e", "err", command])
		if(self.typ == "CHEM"):
			job_file = "job_submission.sh"
			cur_job = open(job_file, 'w')
			for line in cjob.sendjob_text[:7]:
				cur_job.write(line)
			cur_job.write(cjob.sendjob_text[7] + command)
			for line in cjob.sendjob_text[8:]:
				cur_job.write(line)
			cur_job.close()
			subprocess.call(["qsub", job_file])
	def runCommands(self, commands):
		for command in commands:
			self.runSingle(command)
	def runDirSingle(self, dirname, command):
		PyUtils.create_folder(dirname[:-1])
		os.chdir(dirname[:-1])
		self.runSingle(command)
		os.chdir('../')
	def runDirCommands(self, dirlist, commands):
		self.checkList(dirlist, commands)
		f = open(dirlist, 'r')
		lines = f.readlines()
		for dirname, command in zip(lines, commands):
			self.runDirSingle(dirname, command)
		f.close()
	def runJobs(self, dirlist, command):
		'''f = open(dirlist, 'r')
		for job in f:
			PyUtils.create_folder(job[:-1])
			os.chdir(job[:-1])
			if(self.typ == "WEXAC"):
				subprocess.call(["bsub", "-u", "/dev/null", "-R", "rusage[mem=1024]", "-q", "new-all.q", "-o", "out", "-e", "err", command])
			if(self.typ == "CHEM"):
				job_file = "../job_submission.sh"
				cur_job = open(job_file, 'w')
				for line in cjob.sendjob_text[:7]:
					cur_job.write(line)
				cur_job.write(cjob.sendjob_text[7] + command)
				for line in cjob.sendjob_text[8:]:
					cur_job.write(line)
				cur_job.close()
				subprocess.call(["qsub", job_file])
			self.runSingle()
			os.chdir("../")
		f.close()'''
		f = open(dirlist, 'r')
		lines = f.readlines()
		commands = [command] * len(lines)
		f.close()
		self.runDirCommands(dirlist, commands)
		
        def runJobsArgs(self, dirlist, command, arglist):
                '''f = open(dirlist, 'r')
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
				subprocess.call(["qsub", "-q", "medium", "-l", "select=1:ncpus=1:mem=10gb", "-j", "eo", "--", command])
			os.chdir("../")
                        i += 1
                f.close()'''
		self.checkList(dirlist, arglist)
		commands = []
		for arg in arglist:
			commands += [command + ' ' + str(arg)]
		self.runDirCommands(dirlist, commands)
	
	def runCommandsArgs(self, command, arglist):
		commands = []
		for arg in arglist:
			commands += [command + ' ' + str(arg)]
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
