import sys
import os
import shutil

Dict = {'Pictet-Spingler': ('[n;H1:1][c:2][c:3][C:4][C:5][N:6]([H:10])[H].[H:9][C:7](=O)([*:8])>>[n;H1:1][c:2]1[c:3][C:4][C:5][N:6]([H:10])[C:7]([H:9])([*:8])1', True),
        'Phthalamide-to-AcyloidChloride': ('[N;H1:1]([C:2]=O)([C:3]=O)>>[N:1]([C:2]=O)([C:3]=O)[C](=O)[C]=[C]', False),
        'Reduction-of-Cyanide': ('[*:1][C:2]#[N:3]>>[*:1][C;H2:2][N;H2:3]', False),
        'Aldol-reaction-Trans-product': ('[C:1](=[O:2])[C;H3:3].[C:4](=[O:5])[C:6]>>[C:1](=[O:2])[C;H1:3]=[C:4]([H])\[C:6]', True),
        'Aldol-Condensation': ('[C:1](=[O:2])[C;H3:3].[C:4](=[O:5])[C:6]>>[C:1](=[O:2])[C;H2:3][C@@:4]([O:5])([C:6])[H]', True),
        'Claisen-reaction': ('[C:1](=[O:2])([C:3])[O:4][*:5].[C:6](=[O:7])([*:8])[O:9][*:10]>>[C:6](=[O:7])([*:8])[C:3][C:1](=[O:2])[O:4][*:5].[O:9][*:10]', True),
        'Replacement-of-oxygen-to-chloride': ('[C:1](=[O:2])[C:3][C;H2,H1:4]([O:5])([*:6])[*:7]>>[C:1](=[O:2])[C:3][C:4]([Cl:5])([*:6])[*:7]', False),
        'Claisen-reaction-Unimol': ('[C:1](=[O:2])([C:3])[O:4][*:5]>>[C](=[O])([C])[C:3][C:1](=[O:2])[O:4][*:5]', False),
        'Acyloin-Condensation': ('[C:1](=[O:2])([*:3])[O:11].[C:4](=[O:5])([*:6])[O:14]>>[C:1]([O;H:2])([*:3])[C:4](=[O:5])[*:6].[O:11].[O:14]', True),
        'Ketone-to-amine': ('[C:1][C:2](=[O:4])[C:3].[N:5]([H:6])([H:7])[*;!C:8]>>[C:1][C:2]([N:5]([H:6])([*:8]))[C:3]', True),
        'Acylchloride-to-amine': ('[*;!N:1][C:2](=[O:3])[Cl:4].[N:5]([H:6])([*:7])[*:8]>>[*:1][C:2]([H])([H])[N:5]([*:7])[*:8].[O:3]([H])[H:6].[Cl:4][H]', True),
        'Alcohol-to-amine': ('[C;$([C:1]([C:2])([C:3])[H:4]),$([C:1]([C:2])([C:3])[C:4]):1][O:5].[N:6]([H:10])([*:11])[C:7](=[O:8])[N:9]([*:13])[H:12]>>[C;$([C:1]([C:2])([C:3])[H:4]),$([C:1]([C:2])([C:3])[C:4]):1][N:6]([H:10])[*:11].[C:7](=[O:8])(=[O:5]).[N:9]([H:12])[*:13]', True),
        'Chloride-to-amine': ('[C;$([C:1]([C:2])([C:3])[H:4]),$([C:1]([C:2])([C:3])[C:4]):1][Cl:5].[N:6]([H:10])([*:11])[C:7](=[O:8])[N:9]([*:13])[H:12]>>[C;$([C:1]([C:2])([C:3])[H:4]),$([C:1]([C:2])([C:3])[C:4]):1][N:6]([H:10])[*:11].[C:7](=[O:8])(=O).[N:9]([H:12])[*:13].[H][Cl:5]', True),
        'Schmidt-reaction-ketone-to-amide': ('[*;!H;!F;!Cl;!Br;!I;!N;!O:1][C:2](=[O:3])[*;!H;!F;!Cl;!Br;!I;!N;!O:4]>>[*:4][C:2](=[O:3])[N;H][*:1]', False)}


class Synthetic_Library:

#-------------------Getting initial files------------------------
    def __init__(self, buildingBlocks, outPutFile):    
        self.buildingBlocks = buildingBlocks
        self.outPutFile = outPutFile

#---------------------Getting variables for amount and name reactions-----------

    def get_var1(self, iternum, listrxn = [key for key in Dict]):
        
        self.iternum = iternum
        
        self.listrxn = listrxn
        print 'This is the listtt: ', self.listrxn
        self.bool = True

        self.copyfiles()

#--------------------Getting variable for list of reactions---------------

    def get_var(self, iternum, listrxn = [key for key in Dict]):
        print 'list is: ' + str(listrxn)
        self.iternum = iternum
        self.listrxn = listrxn

        self.bool = False

        self.copyfiles()

#---------------------------Creating copies of buildingBlocks and Final results (copyfile2)-----

    def copyfiles(self):

        print '\033[1m' + '\nThis is the input file:\n' + '\033[0m', self.buildingBlocks, '\n'
        with open(self.buildingBlocks, 'r') as f: # Prints the buildingBlocks File
            print f.read()

        f1 = open('copyfile1.txt', 'w')  # Creates a copy of buildingBlocks
        f1.close()

        self.appending(self.buildingBlocks, 'copyfile1.txt')  

        print '\033[1m' + '\nThis is the output file:\n' + '\033[0m', self.outPutFile, '\n'

        f2 = open('copyfile2.txt', 'w')
        f2.close()

        if self.bool:
            
            self.Iterations1()

        else:

            self.Iterations_c()

#------------------------- Two loops: for each iteration, run the reactions in the list consecutive------

    def Iterations1(self):
        x = 0
        for x in (range(0, self.iternum)):
            for t in (self.listrxn):
                print '\033[94m' + 'This is T: ' + '\033[0m', t
                name_reaction = t
                self.apply_reaction(name_reaction)

                self.appending(self.outPutFile, 'copyfile2.txt')

                print '\033[1m' + '\nAfter', t , 'reaction number (loop',x+1,')' + '\033[0m'
                with open(self.outPutFile, 'r') as f:
                    print f.read()

                self.appending(self.outPutFile, self.buildingBlocks)

            self.Syn = Synthetic_Library(self.buildingBlocks, self.outPutFile)

#-----------------------Three loops: for each of the reactions in the list ---------

    def Iterations(self):
        for a in (self.listrxn):

            self.writing('copyfile1.txt', self.buildingBlocks)
            self.apply_reaction(a)
            self.appending(self.outPutFile, self.buildingBlocks)

            self.Syn = Synthetic_Library(self.buildingBlocks, self.outPutFile)

            for b in (self.listrxn):
                self.apply_reaction(b)
                self.appending(self.outPutFile, self.buildingBlocks)

                self.Syn = Synthetic_Library(self.buildingBlocks, self.outPutFile)

                for c in (self.listrxn):
                    self.apply_reaction(c)

                    self.appending(self.outPutFile, 'copyfile2.txt')

                    self.Syn = Synthetic_Library(self.buildingBlocks, self.outPutFile)


    def Iterations_c(self):
        iterations = self.iternum
        for i in range(iterations):
            for a in self.listrxn:
                self.apply_reaction(a)
                self.appending(self.outPutFile, 'copyfile1.txt')
                self.appending(self.outPutFile, 'copyfile2.txt')
            shutil.copy('copyfile1.txt', 'tmpBB.txt')
            self.buildingBlocks = 'tmpBB.txt'

#------------------------------ appending content of one file to another---------


    def appending(self, fileA, fileB):
        with open(fileA, 'r') as input1, open(fileB, "a") as output1:
            for line in input1:
                output1.write(line)
        return


#-------------------- writing content of one file to another -----------------------


    def writing(self, fileA, fileB):
        with open(fileA, 'r') as input1, open(fileB, "w") as output1:
            for line in input1:
                output1.write(line)
        return


#------------------------Printing the files----------------

    def Printing(self):
        list1 = []
        list2 = []
        with open('copyfile2.txt', 'r') as f1:
            for line in f1:
                list1.append(line)

        with open('copyfile2.txt', 'w') as f1:
            f1.truncate()

        list2 = set(list1)

        with open('copyfile2.txt', 'a') as f1:
            for line in list2:
                f1.write(line)

        print '\033[94m' + '\033[1m' + '\n \n This is the results only from the Rxns: ' + '\033[0m'
        with open('copyfile2.txt', 'r') as f1:
            print f1.read()

        print  '\033[91m' + '\033[1m' + 'Number of Products: ', len(list2), '' + '\033[0m'

        print '\033[94m' + '\033[1m' +'\n \n This is the original file with the original reactant: ' + '\033[0m'
        with open('copyfile1.txt', 'r') as f1:
            print f1.read()


        self.writing('copyfile1.txt', self.buildingBlocks)
#        with open("copyfile1.txt", 'r') as input1, open(self.buildingBlocks, "w") as output1:
#            for line in input1:
#                output1.write(line)

        return
#------------------------------ attribute to Bimol or Unimol according to type reaction---------- 

    def apply_reaction(self, name):
        self.reaction = Reaction(name)
        self.reaction.get_name()
        if self.reaction.get_bi():
            from Code import bimolreactS as BMS
            pointer = BMS.Rxn(self.buildingBlocks, self.outPutFile, self.reaction.get_smirks(), True)

        else:
            from Code import unimolereactS as UMS
            pointer2 = UMS.Parameters('UnimolereactS.py', self.buildingBlocks, self.outPutFile, self.reaction.get_smirks())

        return
#------------------Finding if the name reaction is in the Dictionary, and getting its details: True for Bimol, False for Unimol-------

class Reaction:

    def __init__(self, name_reaction):
        self.name = name_reaction
        self.Dict_reaction()

    def Dict_reaction(self):
#        if self.name in Dict:
#            print "** Name reaction: ", self.name, "is in the Dictionary \n"
#            if Dict[self.name][1]:
#                print "Using Bimolecular reaction"
#            else:
#                print "Using Unimolecular reaction"
#        else:
#            print "** Name reaction is NOT in the Dictionary..."
#            print Dict.keys()
#            sys.exit()
        self.smirks = Dict[self.name][0]
        self.bi = Dict[self.name][1]
#        print "** This is the smirks: ", self.smirks

    def get_smirks(self):
        return self.smirks

    def get_bi(self):
        return self.bi

    def get_name(self):
#        print "-------------------------- Self Name : ", self.name
        return self.name
