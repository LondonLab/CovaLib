import os
def create_folder(name):
	if(os.path.exists(name) == False):
		os.mkdir(name)
def create_softlink(old, new):
        if(os.path.exists(new) == False):
                os.symlink(old, new)
