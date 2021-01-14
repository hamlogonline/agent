#!/bin/bash
set -x
# Make app bundle
pyinstaller\
    --clean\
    --noconfirm\
    --name "HAMLOG Agent"\
    --windowed\
    --osx-bundle-identifier 'com.hamlog.agent'\
    hamlog-agent.py || exit
