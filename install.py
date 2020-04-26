#!/usr/bin/env python3
# -*- coding: utf-8; -*-
#
# Copyright (c) 2020 Álan Crístoffer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import platform
import shutil
import sys

from generators import *


def print_help():
    print('Generates profiles to bash, zsh and fish')
    print('Usage: ')
    print(f'\t{sys.argv[0]} [fish] [bash] [zsh]')


def list_generators():
    os = platform.system()
    gs = []
    if os == 'Darwin':
        gs += [macOS()]
    else:
        gs += [Linux()]
    cmds = {
        'brew': Brew,
        'port': MacPort,
        'apt-get': APT,
        'zypper': Zypper,
        'dnf': DNF,
        'pacman': Pacman,
        'aur': AUR,
        'gem': GEM,
        'npm': NPM,
        'yarn': Yarn,
        'rustup': RustUp,
        'tlmgr': TLMGR
    }
    gs += [v() for k, v in cmds.items() if shutil.which(k)]
    return gs


if __name__ == '__main__':
    args = sys.argv[1:]
    ss = ['fish', 'bash', 'zsh']
    ss = [s for s in ss if f'--{s}' in args or s in args]
    if not ss or 'help' in args or '--help' in args or '-h' in args:
        print_help()
        exit(0)
    gs = list_generators()
    if 'bash' in ss:
        BashGenerator(gs).generate_files()
    if 'fish' in ss:
        FishGenerator(gs).generate_files()
    if 'zsh' in ss:
        ZSHGenerator(gs).generate_files()
    print('Done. Existing files have been renamed with suffix .old')
