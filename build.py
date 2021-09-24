#!/usr/bin/env python

import PyInstaller.__main__

PyInstaller.__main__.run([
    'keepout.spec',
    '--onefile',
    '--noconfirm',
    '--clean',
])