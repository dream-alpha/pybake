#!/usr/bin/python
# encoding: utf-8
#
# Copyright (C) 2018-2021 by dream-alpha
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


import os
import sys
import getopt
from Version import VERSION

LIBDIR = "/usr/lib"


def readFile(filename):
	afile = open(filename)
	data = afile.read().strip()
	afile.close()
	return data


def produce_deb_pkg(debdir, pkgdir):
	#print("Producing deb package...")
	pkg = ""
	version = ""
	arch = ""
	lines = readFile(debdir + "/DEBIAN/control").splitlines()
	for line in lines:
		if line.find("Package:") == 0:
			pkg = line.split(" ")[1]
		if line.find("Version:") == 0:
			version = line.split(" ")[1]
		if line.find("Architecture:") == 0:
			arch = line.split(" ")[1]

	if pkg and version and arch:
		pkg_name = pkg + "_" + version + "_" + arch + ".deb"
		#print(pkg_name)

		os.system("dpkg-deb -b -z2 " + debdir)
		print("Deb package created: " + pkgdir + "/" + pkg_name)
		os.system("mv " + debdir + ".deb " + pkgdir + "/" + pkg_name)

	return pkgdir + "/" + pkg_name


def process_maks(gitdir, debdir):
	#print("=====> process_maks: " + gitdir)
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
				#print(gitdir + " >>> " + "installdir = " + installdir)
			if line.find("DOMAIN = ") == 0:
				domain = line.split(" ")[2]
				#print(gitdir + " >>> " + "domain = " + domain)
			if line.find("LANGS := ") == 0:
				langs = list(set(line.split(" ")) - set(["LANGS", ":="]))
				#print(gitdir + " >>> " + "LANGS = " + str(langs))

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
				#print(gitdir + " >>> " + "SUBDIRS = " + str(subdirs))
				for subdir in subdirs:
					process_maks(gitdir + "/" + subdir, debdir)

			if line.find("installdir = ") == 0:
				installdir = line.split(" ")[2]
				installdir = installdir.replace("$(libdir)", LIBDIR)
				#print(gitdir + " >>> " + "installdir = " + installdir)

			if line.find("install_PYTHON") == 0:
				install_PYTHON = list(set(line.split(" ")) - set(["install_PYTHON", "="]))
				#print(gitdir + " >>> " + "install_PYTHON = " + str(install_PYTHON))

			if line.find("install_DATA") == 0:
				install_DATA = list(set(line.split(" ")) - set(["install_DATA", "="]))
				#print(gitdir + " >>> " + "install_DATA = " + str(install_DATA))

		if installdir and install_PYTHON:
			os.system("mkdir -p " + debdir + installdir)
			for afile in install_PYTHON:
				os.system("cp " + gitdir + "/" + afile + " " + debdir + installdir)
		if installdir and install_DATA:
			os.system("mkdir -p " + debdir + installdir)
			for afile in install_DATA:
				os.system("cp " + gitdir + "/" + afile + " " + debdir + installdir)

	#print("<===== process_maks: " + gitdir)


def pybake(argv):
	print("pybake version %s" % VERSION)
	gitdir = ''
	debdir = ''
	pkgdir = ''

	try:
		opts, _args = getopt.getopt(argv, "hi:o:", ["gitdir=", "pkgdir="])
	except getopt.GetoptError as e:
		print("Error: " + str(e))

	if len(opts) < 2:
		print('Usage: python pybake.py -i <gitdir> -o <pkgdir>')
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-i", "--gitdir"):
			gitdir = os.path.normpath(arg)
		elif opt in ("-o", "--pkgdir"):
			pkgdir = os.path.normpath(arg)

	print('git dir is: ' + gitdir)
	print('pkg dir is: ' + pkgdir)
	debdir = pkgdir + "/debroot"

	if not os.path.isfile(gitdir + "/CONTROL/control"):
		print(gitdir + "/CONTROL/control file does not exist, exiting...")
		sys.exit(2)

	os.system("rm -rf " + debdir)
	os.system("mkdir " + debdir)
	os.system("mkdir " + debdir + "/DEBIAN")
	os.system("cp " + gitdir + "/CONTROL/* " + debdir + "/DEBIAN")
	os.system("echo \"2.0\" > " + debdir + "/DEBIAN/debian-binary")

	print("processing MAKs...")
	process_maks(gitdir, debdir)
	pkgfile = produce_deb_pkg(debdir, pkgdir)

	print("pybake done.")
	return pkgfile


if __name__ == "__main__":
	pkg_file = pybake(sys.argv[1:])
	print("pkg_file: %s" % pkg_file)
	exit(pkg_file)
