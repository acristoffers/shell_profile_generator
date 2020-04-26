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

from .utils import Function, Variable
import locale


class Common:
    def generate_functions(self):
        return [
            Function('txz',
                     ['$f'],
                     'tar -c "$(basename "$f")" | xz -9 -T 0 > "$(basename "$f").txz"',
                     ['bash', 'zsh']),
            Function('txz',
                     ['$f'],
                     'tar -c (basename $f) | xz -9 -T 0 > (basename $f).txz',
                     ['fish']),
            Function('tgz',
                     ['$f'],
                     'tar -c "$(basename "$f")" | gzip -9 > "$(basename "$f").txz"',
                     ['bash', 'zsh']),
            Function('tgz',
                     ['$f'],
                     'tar -c (basename $f) | gzip -9 > (basename $f).txz',
                     ['fish']),
            Function('tbz',
                     ['$f'],
                     'tar -c "$(basename "$f")" | bzip2 -9 > "$(basename "$f").txz"',
                     ['bash', 'zsh']),
            Function('tbz',
                     ['$f'],
                     'tar -c (basename $f) | bzip2 -9 > (basename $f).txz',
                     ['fish']),
            Function('zipup',
                     ['$f'],
                     'zip -9 -r "$(basename "$1")" "$(basename "$1")"',
                     ['bash', 'zsh']),
            Function('zipup',
                     ['$f'],
                     'zip -9 -r (basename $argv[1]) (basename $argv[1])',
                     ['fish']),
            Function('add_to_path_if_exists',
                     ['f'],
                     'if [[ -d "$f" ]]\nthen\n\texport PATH=$f:$PATH\nfi',
                     ['bash', 'zsh']),
            Function('add_to_path_if_exists',
                     ['f'],
                     'if test -d $f\n\tset -x PATH $PATH $f\nend',
                     ['fish']),
            Function('ccat',
                     ['f'],
                     'pygmentize -g $f')
        ]

    def generate_variables(self):
        return [
            Variable('HOME', '~'),
            Variable('LC_ALL', '.'.join(locale.getdefaultlocale())),
            Variable('LANG', '$LC_ALL'),
            Variable('DISPLAY', '""'),
            Variable('EDITOR', 'code'),
            Variable('PYTHON', '$(which python3)')
        ]
