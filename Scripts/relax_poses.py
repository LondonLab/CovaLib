import subprocess
import sys
import os
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *
import shutil

def main(name, argv):
        if(not len(argv) == 1):
                print_usage(name)
                return
        subprocess.call(['python', Paths.SCRIPTS + 'relax_pipeline.py', argv[0]])
        '''os.chdir('poses')
        for f in os.listdir(os.getcwd()):
            pyUtils.create_folder(f)
            shutil.move(f, f + '/' + f)'''

def print_usage(name):
        print "Usage : " + name + " <poses file name>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
