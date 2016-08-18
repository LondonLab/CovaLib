#Written by Daniel Zaidman
#Code review by 
import shutil
import subprocess
import os
import Paths
import PyUtils
import tarfile

class RosettaScore:
    def __init__(self, runs):
        self.scores = []
        for run in range(runs):
            with open(str(run) + 'score.sc', 'r') as f:
                lines = f.readlines()
            for model, line in enumerate(lines[2:]):
                self.scores.append((float(line.split()[1]), run, model + 1))
    def getScores(self):
        return self.scores
    def getBest(self, k):
        return sorted(self.scores)[:k]
    def tarBest(self, k, name, tar_file):
        tar = tarfile.open(tar_file, "w")
        best = self.getBest(k)
        with open('fbest', 'w') as fbest:
            for b in best:
                fbest.write(str(b) + '\n')
                bfile = str(b[1]) + name + '_%04d.pdb' % b[2]
                tar.add(bfile)
        tar.add('fbest')
        os.remove('fbest')
        tar.close()
