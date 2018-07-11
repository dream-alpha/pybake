# pybake
## A simple package build tool for python enigma2 plugins

## Usage: 
- python pybake.py -i `git_root_dir` -o `pkg_root_dir` -p `pkg_loc`

## Description: 
Parses the .mak files in `git_root_dir` and generates a deb package.
- `git_root_dir` specifies the directory where the git source files are.
- `pkg_root_dir` specifies the directory where the structure for the package file will be built.
- `pkg_loc` specifies the directory where the package file will be placed.

## Pre-Requisite: 
A `git_root_dir/CONTROL/control` file is required with the following minimum content:
- Package: enigma2-plugin-extensions-`plugin_name`
- Version: `x.x`
- Architecture: `architecture`


