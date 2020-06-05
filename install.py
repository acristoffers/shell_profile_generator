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

"""
Installs profiles
"""

import platform
import shutil
import sys

from generators import (APT, AUR, DNF, GEM, NPM, PKG, TLMGR, BashGenerator,
                        Brew, FishGenerator, Linux, MacPort, Pacman, RustUp,
                        Yarn, ZSHGenerator, Zypper, macOS)


def print_help():
    """
    Prints usage instructions
    """
    print('Generates profiles to bash, zsh and fish')
    print('Usage: ')
    print(f'\t{sys.argv[0]} [fish] [bash] [zsh]')


def list_generators():
    """
    List the generators needed by this system
    """
    system = platform.system()
    generators = []
    if system == 'Darwin':
        generators += [macOS()]
        cmds = {
            'port': MacPort
        }
        generators += [v() for k, v in cmds.items() if shutil.which(k)]
    else:
        generators += [Linux()]
        cmds = {
            'apt-get': APT,
            'zypper': Zypper,
            'dnf': DNF,
            'pacman': Pacman,
            'aur': AUR,
            'pkg': PKG
        }
        generators += [v() for k, v in cmds.items() if shutil.which(k)]
    cmds = {
        'brew': Brew,
        'gem': GEM,
        'npm': NPM,
        'yarn': Yarn,
        'rustup': RustUp,
        'tlmgr': TLMGR
    }
    generators += [v() for k, v in cmds.items() if shutil.which(k)]
    return generators


if __name__ == '__main__':
    args = sys.argv[1:]
    ss = ['fish', 'bash', 'zsh']
    ss = [s for s in ss if f'--{s}' in args or s in args]
    if not ss or 'help' in args or '--help' in args or '-h' in args:
        print_help()
        sys.exit(0)
    generators = list_generators()
    if 'bash' in ss:
        BashGenerator(generators).generate_files()
    if 'fish' in ss:
        FishGenerator(generators).generate_files()
    if 'zsh' in ss:
        ZSHGenerator(generators).generate_files()
    print('Done. Existing files have been renamed with suffix .old')
