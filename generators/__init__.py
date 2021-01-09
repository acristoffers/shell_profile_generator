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
Generators module.
Reexports everything.
"""

from .apt import APT
from .aur import AUR
from .bash import BashGenerator
from .brew import Brew
from .dnf import DNF
from .fish import FishGenerator
from .gem import GEM
from .linux import Linux
from .macos import macOS
from .macport import MacPort
from .npm import NPM
from .pacman import Pacman
from .pkg import PKG
from .rustup import RustUp
from .tlmgr import TLMGR
from .yarn import Yarn
from .zsh import ZSHGenerator
from .zypper import Zypper
from .yay import Yay
