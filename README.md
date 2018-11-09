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

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b2c0376956f340f1b5532dec6f4abb73)](https://www.codacy.com/app/swmaniacster/pybake?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=dream-alpha/pybake&amp;utm_campaign=Badge_Grade)
