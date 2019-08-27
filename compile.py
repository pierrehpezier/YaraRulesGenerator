#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
import sys
import subprocess
import tempfile

TEMPDIR = '/dev/shm/'

class Yarasm(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

def compile(code, arch=64):
    sourcefile = tempfile.NamedTemporaryFile(prefix=TEMPDIR, suffix='.asm').name
    binfile = tempfile.NamedTemporaryFile(prefix=TEMPDIR, suffix='.bin').name
    with open(sourcefile, 'w') as filefd:
        sys.stdout = filefd
        print('[bits {}]'.format(arch))
        print(code)
    sys.stdout = sys.__stdout__
    try:
        process = subprocess.run(['nasm', '-fbin', sourcefile, '-o', binfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        raise Yarasm('Unable to find nasm. Please install nasm')
    if process.stderr:
        raise Yarasm(process.stderr)
    try: os.unlink(sourcefile)
    except FileNotFoundError: pass
    retval = open(binfile, 'rb').read()
    try: os.unlink(binfile)
    except FileNotFoundError: pass
    return retval

def decompile(data, arch=64):
    binfile = tempfile.NamedTemporaryFile(prefix=TEMPDIR, suffix='.bin').name
    open(binfile, 'wb').write(data)
    try:
        process = subprocess.run(['ndisasm', '-b', str(arch), binfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        raise Yarasm('Unable to find ndisasm. Please install ndisasm')
    if process.stderr:
        raise Yarasm(process.stderr)
    try: os.unlink(binfile)
    except FileNotFoundError: pass
    return str(process.stdout, 'UTF-8').strip('\n')

if __name__ == '__main__':
    print(decompile(compile('nop')))
