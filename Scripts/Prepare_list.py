import subprocess
import sys
import os
sys.path.append(os.environ["COVALIB"])
from Code import *

def main(name, argv):
        if not len(argv) == 4:
                print_usage(name)
                return

	num_batches = int(argv[2])
	with open(argv[0], 'r') as f:
		lines = f.readlines()
	if not os.path.exists(argv[1]):
		os.mkdir(argv[1])
	batch_size = len(lines) / num_batches + 1
	batches = []
	for i in range(num_batches):
		batches.append(lines[i * batch_size : (i + 1) * batch_size])
	batches = [batch for batch in batches if len(batch) > 0]
	for i, batch in enumerate(batches):
		if argv[3] == 'True' or argv[3] == 'true':
			os.mkdir(argv[1] + '/' + str(i))
			with open(argv[1] + '/' + str(i) + '/' + str(i) + '.ism', 'w') as f:
				for b in batch:
                                        f.write(b)
		else:
			with open(argv[1] + '/' + str(i) + '.ism', 'w') as f:
				for b in batch:
					f.write(b)

def print_usage(name):
        print "Usage : " + name + " <list> <output_folder> <num_of_batches> <seperate_folders (default = False)>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
