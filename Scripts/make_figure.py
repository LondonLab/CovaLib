import sys,os
sys.path.append(os.environ["COVALIB"])
from Code import *

def main(name, argv):
        if not len(argv) == 2:
                print_usage(name)
                return

        PYMOLUtils.publication_figure(argv[0], argv[1])

def print_usage(name):
        print "Usage : <Session> <Picture_file_name>"
if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
