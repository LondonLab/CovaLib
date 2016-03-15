#!/usr/bin/python
import os, string, sys, math

""" help """
""" usage: ./filter.py rec.crg topdock.pdb """

def dist (a1,a2):
  return math.sqrt((a1[0]-a2[0])*(a1[0]-a2[0])+(a1[1]-a2[1])*(a1[1]-a2[1])+(a1[2]-a2[2])*(a1[2]-a2[2]))

def perLig (liglines,out):
  """ init functional groups arrays """
  ligdonors = []
  ligacceptors = []
  ligH = [] 
  ligC = []
  ligN = []
  ligO = []
  ligS = []
  ligP = []
  ligHalo = []
  ligUNK = []
  clean = 0
  hb = 0

  """ categorize ligand atoms by element """
  for line in liglines:
    if line[0:4] == "ATOM":
      if (line[13]=="C"):
        ligC.append([float(line[30:38]),float(line[38:47]),float(line[47:56])])
    elif (line[13]=="O"):
        ligO.append([float(line[30:38]),float(line[38:47]),float(line[47:56])])
    elif (line[13]=="N"):
        ligN.append([float(line[30:38]),float(line[38:47]),float(line[47:56])])
    elif (line[13]=="H"):
        ligH.append([float(line[30:38]),float(line[38:47]),float(line[47:56])])
    elif (line[13]=="S"):
        ligS.append([float(line[30:38]),float(line[38:47]),float(line[47:56])])
    elif (line[13]=="P"):
        ligP.append([float(line[30:38]),float(line[38:47]),float(line[47:56])])
    elif ((line[13]=="F") or (line[13]=="I") or (line[12:14]=="BR") or (line[12:14]=="CL")):
        ligHalo.append([float(line[30:38]),float(line[38:47]),float(line[47:56])])
    else:
        ligUNK.append([float(line[30:38]),float(line[38:47]),float(line[47:56])])

  """ find ligand acceptors - currently - any O, and any N that is hydrogenless """
  for o in ligO:
    ligacceptors.append(o)

  """ find polar ligand hydrogens """
  for n in ligN:
    nhs = 0
    for h in ligH:
      if dist(h,n) < 1.2:
        ligdonors.append(h)
        nhs = nhs+1
    if (nhs==0):
      ligacceptors.append(n)

  for o in ligO:
    for h in ligH:
      if dist(h,o) < 1.2:
        ligdonors.append(h)

  #number of weird ligand atoms
  print >> out, "REMARK      UNK-lig-atoms   : ", len(ligUNK)
  if len(ligUNK)>0:
    clean=1

  #locate internal ligand clashes
  ligclash=0
  allLig = ligH + ligC + ligN + ligO + ligS + ligP + ligHalo + ligUNK
  allLigButH = ligC + ligN + ligO + ligS + ligP + ligHalo + ligUNK
  for i in allLigButH:
    neighbours=-1 #(accounting for self)
    for j in allLigButH:
      if dist(i,j) < 1.75:
        neighbours=neighbours+1
    if neighbours > 4:
      ligclash=ligclash+1

  for i in ligH:
    neighbours=-1 #(accounting for self)
    for j in allLig:
      if dist(i,j) < 1.75:
        neighbours=neighbours+1
    if neighbours > 2:
      ligclash=ligclash+1

  print >> out, "REMARK      lig-clashes   : ", ligclash
  if ligclash>0:
    clean=1

  #locate donor donor clashes and lig un-sat donors
  unsatdonors=0
  donclash=0
  for l in ligdonors:
    na=0
    for rd in recdonors:
      if dist(l,rd) < 1.75:
        donclash=donclash+1
    for ra in recacceptors:
      if dist(l,ra) < 2.0:      
        hb=hb+1
        na=na+1
    if na==0:
      unsatdonors=unsatdonors+1

  print >> out, "REMARK      Unsat-donors    : ", unsatdonors
  print >> out, "REMARK      Donor clashes   : ", donclash
  if donclash>0:
    clean=1

  #locate acceptor ^2 clashes
  unsataccptors=0
  accclash=0
  for l in ligacceptors:
    na=0
    for ra in recacceptors:
      if dist(l,ra) < 1.75:
        accclash=accclash+1      
    for rd in recdonors:
      if dist(l,rd) < 2.0:
        hb=hb+1
        na=na+1
    if na==0:
      unsataccptors=unsataccptors+1

  print >> out, "REMARK      Unsat-acceptors   : ", unsataccptors
  print >> out, "REMARK      Acceptor clashes   : ", accclash
  if accclash>0:
    clean=1
  
  print >> out, "REMARK      HB    : ", hb
  print hb
  print >> out, "REMARK      Clean : ", clean
  for line in liglines:
    print >> out, line,

recdonors = []
recacceptors = []
recothers = []

""" first store the rec pdb file """
recfile = sys.argv[1] 
f = open(recfile)
reclines = f.readlines()
f.close()

""" identify rec donors and store their coordinates """
for line in reclines:
  if line[0:4] == "ATOM":
    if ((line[12:16]==" HN ") and (line[17:20]=="TYS")): 
      recdonors.append([float(line[30:38]),float(line[38:47]),float(line[47:56])])
    #elif ((line[12:16]==" O  ") and ((line[17:20]=="LEV") or (line[17:20]=="GLV"))): 
    #  recacceptors.append([float(line[30:38]),float(line[38:47]),float(line[47:56])])
else:
      recothers.append([float(line[30:38]),float(line[38:47]),float(line[47:56])])


""" read in topdock """
topdock = sys.argv[2]
f = open(topdock)
topdocklines = f.readlines()
f.close()

out = open("outdock-new.pdb","w")
coordsflag = 0
liglines = []
for line in topdocklines:
  if line[0:4] == "ATOM":
    coordsflag=1
    liglines.append(line)
  else:
    if coordsflag==1:
      #we just finished reading this lig's coords
      #notice this code assumes there's at least one line after
      #the last lig coord (e.g. TER, END, ENDMDL...)
      perLig(liglines,out)
      liglines = []
      coordsflag=0
      print >> out, line,
    else:
      print >> out, line,
      if (line[10:14]=="Name"):
        print line[31:40]

#for d in ligdonors:
#  for a in recacceptors:
#    if dist(a,d) < 2.0:
#      print 'found'

