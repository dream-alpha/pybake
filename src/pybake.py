#!/usr/bin/python
# encoding: utf-8
#
# Copyright (C) 2018 by dream-alpha
#
# In case of reuse of this source code please do not remove this copyright.
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	For more information on the GNU General Public License see:
#	<http://www.gnu.org/licenses/>.
#

import os, sys, getopt
LIBDIR = "/usr/lib"

def readFile(filename):
	file = open(filename)
	data = file.read().strip()
	file.close()
	return data

def process(gitdir, debdir):
	print("=====> process: " + gitdir)
	installdir = ""
	install_PYTHON = ""
	install_DATA = ""
	domain = ""

	lines = readFile(gitdir + "/Makefile.am").splitlines()

	if os.path.basename(gitdir) == "po":
		for line in lines:
			if line.find("installdir = ") == 0:
				installdir = line.split(" ")[2]
				installdir = installdir.replace("$(libdir)", LIBDIR)
				print(gitdir + " >>> " + "installdir = " + installdir)
			if line.find("DOMAIN = ") == 0:
				domain = line.split(" ")[2]
				print(gitdir + " >>> " + "domain = " + domain)
			if line.find("LANGS := ") == 0:
				langs = list(set(line.split(" ")) - set(["LANGS", ":="]))
				print(gitdir + " >>> " + "LANGS = " + str(langs))

		installdir = installdir.replace("$(DOMAIN)", domain)

		if installdir and domain and langs:
			for lang in langs:
				destdir = debdir + installdir + "/locale/" + lang + "/LC_MESSAGES"
				os.system("mkdir -p " + destdir)
				os.system("cp " + os.path.dirname(gitdir) + "/src/locale/" + lang + "/LC_MESSAGES/*.mo " + destdir)
	else:
		for line in lines:
			if line.find("SUBDIRS = ") == 0:
				subdirs = list(set(line.split(" ")) - set(["SUBDIRS", "="]))
				print(gitdir + " >>> " + "SUBDIRS = " + str(subdirs))
				for subdir in subdirs:
					process(gitdir + "/" + subdir, debdir)

			if line.find("installdir = ") == 0:
				installdir = line.split(" ")[2]
				installdir = installdir.replace("$(libdir)", LIBDIR)
				print(gitdir + " >>> " + "installdir = " + installdir)

			if line.find("install_PYTHON") == 0:
				install_PYTHON = list(set(line.split(" ")) - set(["install_PYTHON", "="]))
				print(gitdir + " >>> " + "install_PYTHON = " + str(install_PYTHON))

			if line.find("install_DATA") == 0:
				install_DATA = list(set(line.split(" ")) - set(["install_DATA", "="]))
				print(gitdir + " >>> " + "install_DATA = " + str(install_DATA))

		if installdir and install_PYTHON:
			os.system("mkdir -p " + debdir + installdir)
			for file in install_PYTHON:
				os.system("cp " + gitdir + "/" + file + " " + debdir + installdir)
		if installdir and install_DATA:
			os.system("mkdir -p " + debdir + installdir)
			for file in install_DATA:
				os.system("cp " + gitdir + "/" + file + " " + debdir + installdir)
		
	print("<===== process: " + gitdir)

def main(argv):
	print("Hello World!")
	gitdir = ''
	debdir = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["gitdir=","debdir="])
	except getopt.GetoptError:
		print 'plugbake.py -i <gitdir> -o <debdir>'
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print 'plugbake.py -i <gitdir> -o <debdir>'
			sys.exit()
		elif opt in ("-i", "--gitdir"):
			gitdir = arg
		elif opt in ("-o", "--debdir"):
			debdir = arg
			print('Git dir is: ' + gitdir)
			print('Deb dir is: ' + debdir)

	os.system("rm -rf " + debdir)
	os.system("mkdir " + debdir)
	os.system("mkdir " + debdir + "/DEBIAN")
	os.system("cp " + gitdir + "/CONTROL/control " + debdir + "/DEBIAN")

	process(gitdir, debdir)
	
	print("Goodbye World!")

if __name__ == "__main__":
	main(sys.argv[1:])
