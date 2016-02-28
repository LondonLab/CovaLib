import os
def create_folder(name):
	if (os.path.exists(name) == False):
		os.mkdir(name)
