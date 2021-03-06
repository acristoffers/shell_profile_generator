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

import locale

from .utils import Alias, Function, Variable


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
            Function('add-to-path-if-exists',
                     ['f'],
                     (
                         'has=$(python3 -c \'import os,sys; print(sys.argv[1] in os.environ["PATH"].split(":"))\' $f)\n'
                         'if [[ -d "$f" ]] && [ "$has" = "False" ]\n'
                         'then\n'
                         '\texport PATH=$f:$PATH\n'
                         'fi'
                     ),
                     ['bash', 'zsh']),
            Function('add-to-path-if-exists',
                     ['f'],
                     'if test -d $f; and not contains $f $PATH\n\tset -x PATH $f $PATH\nend',
                     ['fish']),
            Function('fix-path',
                     [],
                     ('tmp=$PATH\n'
                      'export PATH=$(dirname $(which python3))\n'
                      'ps=(/sbin /usr/sbin /usr/local/sbin /bin /usr/bin /usr/local/bin)\n'
                      'for path in "${ps[@]}"\n'
                      'do\n'
                      '\tadd-to-path-if-exists $path\n'
                      'done\n'
                      'oldIFS=$IFS\n'
                      'IFS=:\n'
                      'ps=($tmp)\n'
                      'IFS=$olsIFS\n'
                      'for path in "${ps[@]}"\n'
                      'do\n'
                      '\tadd-to-path-if-exists $path\n'
                      'done'),
                     ['bash']),
            Function('fix-path',
                     [],
                     ('tmp=$PATH\n'
                      'export PATH=$(dirname $(which python3))\n'
                      'ps=(/sbin /usr/sbin /usr/local/sbin /bin /usr/bin /usr/local/bin)\n'
                      'for p in "${ps[@]}"\ndo\n'
                      '\tadd-to-path-if-exists $p\n'
                      'done\n'
                      'for p in ${(s.:.)tmp}\ndo\n'
                      '\tadd-to-path-if-exists $p\n'
                      'done'),
                     ['zsh']),
            Function('fix-path',
                     [],
                     ('set tmp $PATH\n'
                      'set -x PATH /bin\n'
                      'for path in {,/usr}{,/local}{/sbin,/bin}\n'
                      '\tadd-to-path-if-exists $path\n'
                      'end\n'
                      'for path in $tmp\n'
                      '\tadd-to-path-if-exists $path\n'
                      'end'),
                     ['fish'])
        ]

    def generate_variables(self):
        cod, enc = locale.getdefaultlocale()
        return [
            Variable('HOME', '~'),
            Variable('LC_ALL', '.'.join((cod or 'en_US', enc or 'UTF8'))),
            Variable('LANG', '$LC_ALL'),
            Variable('EDITOR', 'nvim'),
            Variable('PYTHON', '$(which python3)')
        ]

    def generate_aliases(self):
        return [
            Alias('ccat', 'pygmentize -g')
        ]
