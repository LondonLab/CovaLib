import os
import sys
sys.path.append(os.environ["COVALIB"])
from Code import Synthetic_Library as SL

def main(name, argv):
    if len(argv) == 2:
        getDict = []
        getDict = SL.Dict.keys()
        print "\n", getDict

        list_name_reaction = []

        n = raw_input("\nAmount of different Reactions: ")
        n1 = int(n)
        print "This is n: ", n1
        i = 0
        while (i < n1):
            name_reaction_var = raw_input("Reaction No. %d : " %(i+1))
            list_name_reaction.append(name_reaction_var)
            i = i + 1

    if len(argv) > 2:
        list_name_reaction = argv[2:]
        #x = 2
        #for t in range(0,len(argv[2:])):
        #    list_name_reaction.append(argv[x])
        #    x = x + 1

    if len(argv) < 2:
        print_usage(name)                                                                                                                                                                                         
        return


    r = raw_input("\nAmount of repeating Reactions (Iteration number): ")
    r1 = int(r)


    print 'This is the List: ', list_name_reaction
    namefile = sys.argv[0]
    print 'Name File: ', namefile, '\n'
    file1 = argv[0]
    file2 = argv[1]


    
    files = SL.Synthetic_Library(file1, file2)
    if list_name_reaction[0] == 'all':
        files.get_var(r1)
    else:
        files.get_var(r1, list_name_reaction)

    files.Printing()


    sys.exit()

def print_usage(name):
    print "Usage : " + name + " <file1> <file2>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])

'''
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

'''
