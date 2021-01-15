#!/bin/bash
set -x
# Make app bundle
pyinstaller hamlog-agent.spec --clean -y || exit
