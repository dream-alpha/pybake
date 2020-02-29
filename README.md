[![Codacy Badge](https://app.codacy.com/project/badge/Grade/f58e0b6b57544fbaa4f5ec7247071704)](https://www.codacy.com/gh/dream-alpha/pybake/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=dream-alpha/pybake&amp;utm_campaign=Badge_Grade)

# pybake
## A simple package build tool for python enigma2 plugins

## Usage 
- python pybake.py -i `git_root_dir` -o `pkg_dir`

## Description 
Parses the .mak files in `git_root_dir` (and below) and generates a deb package.
- `git_root_dir` specifies the directory where the git source files are.
- `pkg_dir` specifies the directory where the package file will be placed.

## Pre-Requisite 
A `git_root_dir/CONTROL/control` file is required with the following minimum content:
- Package: enigma2-plugin-extensions-`plugin_name`
- Version: `x.x`
- Architecture: `architecture`
