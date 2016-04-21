import sys,os,math
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *

def main(name, argv):
    if (len(argv) != 2):
        print_usage(name)
        return
    infile =  filters.filter_by(argv[0],argv[1])
    infile.for_sale()

def print_usage(name):
    print "Usage : " + name + "<path> <score_file>"


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])

