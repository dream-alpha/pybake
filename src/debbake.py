#!/usr/bin/python
# encoding: utf-8
#
# Copyright (C) 2018-2024 by dream-alpha
#
# In case of reuse of this source code please do not remove this copyright.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# For more information on the GNU General Public License see:
# <http://www.gnu.org/licenses/>.


import os
import sys
import getopt
from Version import VERSION
from FileUtils import readFile, deleteDirectory, createDirectory, copyFiles, moveFile


LIBDIR = "/usr/lib"


def parseControlFile(path):
	# print("Parsing control file...")
	pkg = version = arch = ""
	lines = readFile(path).splitlines()
	for line in lines:
		if line.startswith("Package:"):
			pkg = line.split(" ")[1]
		elif line.startswith("Version:"):
			version = line.split(" ")[1]
		elif line.startswith("Architecture:"):
			arch = line.split(" ")[1]
	return pkg, version, arch


def create_deb_pkg(debdir, pkgpath):
	# print("create_deb_pkg: %s..." % pkgpath)
	os.system("chmod 755 %s" % os.path.join(debdir, "DEBIAN", "*"))
	os.system("dpkg-deb -b -z2 %s" % debdir)
	moveFile(debdir + ".deb", pkgpath)
	print("package created: %s" % pkgpath)


def process_maks(gitdir, debdir):
	# print("=====> process_maks: %s > %s" % (gitdir, debdir))
	installdir = install_PYTHON = install_DATA = domain = ""
	lines = readFile(os.path.join(gitdir, "Makefile.am")).splitlines()
	for line in lines:
		line = line.strip()
		if line.startswith("SUBDIRS = "):
			subdirs = line.split(" ")[2:]
			# print(gitdir + " >>> SUBDIRS = %s" % subdirs)
			for subdir in subdirs:
				# print("subdir: %s" % subdir)
				process_maks(os.path.join(gitdir, subdir), debdir)
		elif line.startswith("installdir = "):
			installdir = line.split(" ")[2].replace("$(libdir)", LIBDIR)
			# print(gitdir + " >>> installdir = %s" % installdir)
		elif line.startswith("DOMAIN = "):
			domain = line.split(" ")[2]
			# print(gitdir + " >>> domain = %s" % domain)
		elif line.startswith("LANGS := "):
			langs = line.split(" ")[2:]
			# print(gitdir + " >>> LANGS = %s" + langs)
		elif line.startswith("install_PYTHON"):
			install_PYTHON = line.split(" ")[2:]
			# print(gitdir + " >>> install_PYTHON = %s" % install_PYTHON)
		elif line.startswith("install_DATA"):
			install_DATA = line.split(" ")[2:]
			# print(gitdir + " >>> install_DATA = %s" %s install_DATA)

	if installdir:
		if domain:
			installdir = installdir.replace("$(DOMAIN)", domain)
			if langs:
				for lang in langs:
					destdir = os.path.join(debdir + installdir, "locale", lang, "LC_MESSAGES")
					createDirectory(destdir)
					copyFiles(os.path.join(os.path.dirname(gitdir), "src/locale", lang, "LC_MESSAGES", "*.mo"), destdir)
		if install_PYTHON:
			createDirectory(debdir + installdir)
			for afile in install_PYTHON:
				copyFiles(os.path.join(gitdir, afile), debdir + installdir)
		if install_DATA:
			createDirectory(debdir + installdir)
			for afile in install_DATA:
				copyFiles(os.path.join(gitdir, afile), debdir + installdir)

	# print("<===== process_maks: %s" % gitdir)


def debbake(argv):
	print("debbake version %s" % VERSION)
	gitdir = debdir = pkgdir = ""

	try:
		opts, _args = getopt.getopt(argv, "hi:o:", [])
	except getopt.GetoptError as e:
		print("Error: " + str(e))

	if len(opts) < 2:
		print('Usage: python debbake.py -i <gitdir> -o <pkgdir>')
		sys.exit(2)

	for opt, arg in opts:
		if opt == "-i":
			gitdir = os.path.normpath(arg)
		elif opt == "-o":
			pkgdir = os.path.normpath(arg)

	print("git dir: %s" % gitdir)
	print("pkg dir: %s" % pkgdir)
	debdir = os.path.join(pkgdir, "debroot")
	print("deb dir: %s" % debdir)

	if not os.path.isfile(os.path.join(gitdir, "CONTROL/control")):
		print("%s file does not exist, exiting..." % os.path.join(gitdir, "CONTROL/control"))
		sys.exit(2)

	deleteDirectory(debdir)
	createDirectory(os.path.join(debdir, "DEBIAN"))
	copyFiles(os.path.join(gitdir, "CONTROL", "*"), os.path.join(debdir, "DEBIAN"))
	os.system("echo \"2.0\" > %s" % os.path.join(debdir, "DEBIAN/debian-binary"))

	print("processing MAKs...")
	process_maks(gitdir, debdir)

	pkgpath = "None"
	pkg, version, arch = parseControlFile(os.path.join(debdir, "DEBIAN/control"))
	if pkg and version and arch:
		pkgpath = os.path.join(pkgdir, "%s_%s_%s.deb" % (pkg, version, arch))
		create_deb_pkg(debdir, pkgpath)
	else:
		print("no package created.")
	print("debbake done.")
	return pkgpath


if __name__ == "__main__":
	pkgfile = debbake(sys.argv[1:])
	print("pkgfile: %s" % pkgfile)
	sys.exit(pkgfile)
