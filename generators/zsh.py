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

import itertools
import shutil
from os import path

from .common import Common
from .utils import Function


class ZSHGenerator:
    def __init__(self, generators):
        self.generators = [Common(), *generators]

    def generate_files(self):
        vs = self.generate_variables()
        fs = self.generate_functions()
        profile = 'umask 077\n\n'
        profile += 'if [ -f /etc/bash_completion ];\nthen\n\tsource /etc/bash_completion\nfi\n\n'
        profile += 'if [[ $- == *i* ]];\nthen\n\texport PS1="%F{cyan}%1~ %F{green}$ %f"\n'
        profile += '''\tbindkey "^[[A" history-beginning-search-backward\n\tbindkey "^[[B" history-beginning-search-forward\nfi\n\n'''
        profile += '\n\n'.join(fs) + '\n\n'
        profile += '\n'.join(vs) + '\n'
        profile += '\nssh-add -A &> /dev/null\n\n'
        profile += 'add_to_path_if_exists /usr/local/sbin\n'
        profile += 'add_to_path_if_exists $HOME/bin\n'
        profile += 'add_to_path_if_exists $HOME/.config/yarn/global/node_modules/.bin\n'
        profile += 'add_to_path_if_exists $HOME/.cargo/bin\n'
        print(f'Generating ~/.zshrc')
        zshrc_file_name = path.expanduser('~/.zshrc')
        if path.exists(zshrc_file_name):
            shutil.move(zshrc_file_name, f'{zshrc_file_name}.old')
        with open(zshrc_file_name, 'tw') as zshrc_file:
            zshrc_file.write(profile)

    def generate_variables(self):
        return [self.var_to_string(e)
                for g in self.generators
                for e in g.generate_variables()]

    def generate_functions(self):
        fs = [g.generate_functions() for g in self.generators]
        fs = list(itertools.chain.from_iterable(fs))
        fs += [self.generate_update_function(fs)]
        return [self.func_to_string(e)
                for e in sorted(fs, key=lambda x: x.name)
                if e.only is None or 'zsh' in e.only]

    def func_to_string(self, func):
        args = [a.replace('$', '') for a in func.args]
        args = [f'{arg}=${i+1}' for i, arg in enumerate(args)]
        f = f"function {func.name}() {{\n\t"
        f += '\n\t'.join(args) + ('\n\t' if len(args) else '')
        f += func.body.replace('\n', '\n\t')
        f += '\n}'
        return f

    def var_to_string(self, var):
        return f'export {var.name}={var.value}'

    def generate_update_function(self, fs):
        fs = [f.name for f in fs if f.name.startswith('update-')]
        return Function(
            'update',
            [],
            '\n'.join(fs)
        )
