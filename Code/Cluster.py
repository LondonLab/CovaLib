import subprocess
import os
import sys
import PyUtils
import socket
import chemfarm_job_submission as cjob
from subprocess import Popen, PIPE
import time

class Cluster:
	def __init__(self):
		#self.getServer()
		self.typ = "CHEM"
        @staticmethod
        def wait(job_ids, timeout = -1):
                jobs_done = False
                i = 0
                while not jobs_done:
                        if i == timeout:
                                break
                        time.sleep(10)
                        all_done = True
                        p = Popen(['/gpopt/altair/pbs/default/bin/qstat'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
                        jobs_running = [line.split()[0] for line in p.stdout.read().split('\n') if 'pbs' in line]
                        for line in job_ids:
                                if line in jobs_running:
                                        all_done = False
                        if all_done:
                                jobs_done = True
                        else:
                                print "Not done yet"
                        i += 1

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
			#subprocess.call(["/gpopt/altair/pbs/default/bin/qsub", job_file])
                        p = Popen(["/gpopt/altair/pbs/default/bin/qsub", job_file], stdout=PIPE, stderr=PIPE, stdin=PIPE)
                        return [line.split()[0] for line in p.stdout.read().split('\n') if 'pbs' in line][0]
        def runSingleDepend(self, command, depend_jobs_file):
                with open(depend_jobs_file, 'r') as f:
                        depend_jobs = [line.split()[0] for line in f]
                if(self.typ == "WEXAC"):
                        subprocess.call(["bsub", "-u", "/dev/null", "-R", "rusage[mem=1024]", "-q", "new-all.q", "-o", "out", "-e", "err", command])
                if(self.typ == "CHEM"):
                        job_file = "job_submission.sh"
                        cur_job = open(job_file, 'w')
                        for line in cjob.sendjob_text[:1]:
                                cur_job.write(line)
                        for line in depend_jobs:
                                cur_job.write('#PBS -W depend=afterany:' + ":".join(depend_jobs))
                        for line in cjob.sendjob_text[1:7]:
                                cur_job.write(line)
                        cur_job.write(cjob.sendjob_text[7] + '\'' + command + '\'')
                        for line in cjob.sendjob_text[8:]:
                                cur_job.write(line)
                        cur_job.close()
                        subprocess.call(["/gpopt/altair/pbs/default/bin/qsub", job_file])

	def runSingleShell(self, command):
		job_file = "job_submission.sh"
		cur_job = open(job_file, 'w')
		for line in cjob.sendjob_text[:7]:
			cur_job.write(line)
		cur_job.write(command + '\n')
		for line in cjob.sendjob_text[9:]:
			cur_job.write(line)
		cur_job.close()
		subprocess.call(["/gpopt/altair/pbs/default/bin/qsub", job_file])
	def runCommands(self, commands):
		jobs = []
                for command in commands:
			jobs.append(self.runSingle(command))
                return jobs
	def runDirSingle(self, dirname, command):
		PyUtils.create_folder(dirname[:-1])
		curr = os.getcwd()
		os.chdir(dirname[:-1])
		job = self.runSingle(command)
		os.chdir(curr)
                return job
	def runDirCommands(self, dirlist, commands):
		self.checkList(dirlist, commands)
		f = open(dirlist, 'r')
		lines = f.readlines()
                jobs = []
		for dirname, command in zip(lines, commands):
			jobs.append(self.runDirSingle(dirname, command))
		f.close()
                return jobs
	def runJobs(self, dirlist, command):
		f = open(dirlist, 'r')
		lines = f.readlines()
		commands = [command] * len(lines)
		f.close()
		return self.runDirCommands(dirlist, commands)
		
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
		return self.runCommands(commands)
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
