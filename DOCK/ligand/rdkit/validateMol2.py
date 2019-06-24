import sys

in_file = sys.argv[1]
out_file = sys.argv[2]

with open(in_file) as f:
 data = f.read()
with open(out_file,"w") as f:
 f.write(data.replace("S.O2","S.o2"))
