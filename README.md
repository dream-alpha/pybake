# pybake
A simple package build tool for python enigma2 plugins.

Usage: pybake -i <git root dir> -o <pkg root dir> -p <pkg loc>

Descripiton: Parses the .mak file in <git root dir> and generates a deb package.
	<git root dir> is the directory where the git source files are.
	<pkg root dir> is the directory where the structure for the package file will be built.
	<pkg loc> is the directory where the package file will be placed.

Pre-Requ: 
A <git root dir>/CONTORL/control file is required with the following minimum content:
	Package: enigma2-plugin-extensions-<plugin name>
	Version: x.x
	Architecture: <architecture>


