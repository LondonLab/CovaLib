import subprocess
import sys
import os
import gzip
import re
sys.path.append(os.environ["COVALIB"])
from Code import *

def main(name, argv):
        if not len(argv) == 3:
                print_usage(name)
                return

	with open(argv[1] + '/dirlist', 'r') as f:
		folders = [line[:-1] for line in f.readlines()]
	print "1"
	ranges = []
	for folder in folders:
		with open(argv[1] + '/' + folder + '/range.txt', 'r') as f:
			start = int(f.readline())
			end = int(f.readline())
			ranges.append((folder, start, end))
	print "2"

	with open(argv[0], 'r') as f:
		ids = [line[:-1] for line in f.readlines()]
	for ID in ids:
		for ran in ranges:
			if ID >= ran[1] and ID <= ran[2]:
				print ran

	'''gz_files = os.listdir(argv[1])[1:100]
	print gz_files[-1]
	ID = ["5989943.","1924705."]
	total_num = int(argv[4])
	max_ingz = len(ID) / total_num
	total_counter = 0
	max_counter = 0
	gw = gzip.open(argv[3] + '/' + argv[2] + str(total_counter) + '.db2.gz', 'wb')
	for mol_id in ID:
		max_counter += 1
		if max_counter > max_ingz:
			max_counter = 0
			gw.close()
			total_counter += 1
			gw = gzip.open(argv[3] + '/' + argv[2] + str(total_counter) + '.db2.gz', 'wb')
		is_found = False
		for gz_file in gz_files:
			with gzip.open(argv[1] + '/' + gz_file) as gf:
				while True:
					line = gf.readline()
					if mol_id in line and line[0] == 'M':
						gw.write(line)
						break
				while not line[0] == 'E':
					line = gf.readline()
					gw.write(line)
				is_found = True
			if is_found:
				break'''

def print_usage(name):
        print "Usage : " + name + " <list> <big_library_folder> <prefix>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
