# pybake

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/e219eac8afb04551b06a7dfc2465af4a)](https://app.codacy.com/app/swmaniacster/pybake?utm_source=github.com&utm_medium=referral&utm_content=dream-alpha/pybake&utm_campaign=Badge_Grade_Settings)

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
