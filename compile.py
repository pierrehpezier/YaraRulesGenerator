#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
import sys
import subprocess
import tempfile

if os.name == 'nt':
    TEMPDIR = os.getenv('TEMP')
else:
    TEMPDIR = '/dev/shm/'

class Yarasm(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

def securedelete(filename):
    if os.path.isfile(filename):
        os.unlink(filename)

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
        securedelete(sourcefile)
        if os.path.isfile(binfile):
            securedelete(binfile)
        raise Yarasm('Unable to find nasm. Please install nasm')
    securedelete(sourcefile)
    if process.stderr:
        securedelete(binfile)
        raise Yarasm(process.stderr)
    retval = open(binfile, 'rb').read()
    securedelete(binfile)
    return retval

def decompile(data, arch=64):
    binfile = tempfile.NamedTemporaryFile(prefix=TEMPDIR, suffix='.bin').name
    open(binfile, 'wb').write(data)
    try:
        process = subprocess.run(['ndisasm', '-b', str(arch), binfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        securedelete(binfile)
        raise Yarasm('Unable to find ndisasm. Please install ndisasm')
    if process.stderr:
        securedelete(binfile)
        raise Yarasm(process.stderr)
    securedelete(binfile)
    return str(process.stdout, 'UTF-8').strip('\n')

if __name__ == '__main__':
    print(decompile(compile('nop')))
