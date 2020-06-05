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

import shutil

from .utils import Alias, Function, Variable


class macOS:
    def generate_functions(self):
        gs = []
        if shutil.which('pip'):
            gs += [
                Function(
                    'update-pip',
                    [],
                    'pip install --upgrade pip\n' +
                    "pip list --outdated --no-cache-dir | awk 'FNR>2 {print $1}' | xargs pip install --no-cache-dir --upgrade")
            ]
        if shutil.which('pip2'):
            gs += [
                Function(
                    'update-pip2',
                    [],
                    'pip2 install --upgrade pip\n' +
                    "pip2 list --outdated --no-cache-dir | awk 'FNR>2 {print $1}' | xargs pip2 install --no-cache-dir --upgrade")
            ]
        if shutil.which('pip3'):
            gs += [
                Function(
                    'update-pip3',
                    [],
                    'pip3 install --upgrade pip\n' +
                    "pip3 list --outdated --no-cache-dir | awk 'FNR>2 {print $1}' | xargs pip3 install --no-cache-dir --upgrade")
            ]
        return gs

    def generate_variables(self):
        return [
            Variable('DISPLAY', '""'),
        ]

    def generate_aliases(self):
        return [
            Alias(
                'ls',
                'ls -G',
                ['bash', 'zsh']
            ),
            Alias(
                'rep',
                r"resize -s 24 80 &>/dev/null;printf '\e[3;0;0t';clear"),
            Alias(
                'rep2',
                r"resize -s 24 155 &>/dev/null;printf '\e[3;500;0t';clear"),
            Alias(
                'rep3',
                r"resize -s 34 80 &>/dev/null;printf '\e[3;0;370t';clear"),
            Alias(
                'rep4',
                r"resize -s 34 155 &>/dev/null;printf '\e[3;500;370t';clear"),
            Alias(
                'fv',
                r"resize -s 60 155 &>/dev/null;printf '\e[3;500;0t';clear")
        ]
