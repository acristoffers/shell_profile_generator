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


class BashGenerator:
    def __init__(self, generators):
        self.generators = [Common(), *generators]

    def generate_files(self):
        ls = self.generate_alises()
        vs = self.generate_variables()
        fs = self.generate_functions()
        profile = 'umask 077\n\n'
        profile += 'if [ -f /etc/bash_completion ];\nthen\n\tsource /etc/bash_completion\nfi\n\n'
        profile += 'if [[ $- == *i* ]];\nthen\n\texport PS1="\\[\\033[38;5;14m\\]\\W\\[$(tput sgr0)\\]\\[\\033[38;5;15m\\] \\[$(tput sgr0)\\]\\[\\033[38;5;2m\\]\\\\$\\[$(tput sgr0)\\]\\[\\033[38;5;15m\\] \\[$(tput sgr0)\\]"\n'
        profile += '''\tbind '"\\e[A": history-search-backward'\n\tbind '"\\e[B": history-search-forward'\nfi\n\n'''
        profile += '\n'.join(ls) + ('\n\n' if len(ls) else '')
        profile += '\n\n'.join(fs) + ('\n\n' if len(fs) else '')
        profile += '\n'.join(vs) + ('\n\n' if len(vs) else '')
        profile += '\nssh-add -A &> /dev/null\n\n'
        profile += 'add_to_path_if_exists /usr/local/sbin\n'
        profile += 'add_to_path_if_exists $HOME/bin\n'
        profile += 'add_to_path_if_exists $HOME/.config/yarn/global/node_modules/.bin\n'
        profile += 'add_to_path_if_exists $HOME/.cargo/bin\n'
        print(f'Generating ~/.profile and ~/.bashrc')
        profile_file_name = path.expanduser('~/.profile')
        if path.exists(profile_file_name):
            shutil.move(profile_file_name, f'{profile_file_name}.old')
        bashrc_file_name = path.expanduser('~/.bashrc')
        if path.exists(bashrc_file_name):
            shutil.move(bashrc_file_name, f'{bashrc_file_name}.old')
        with open(profile_file_name, 'tw') as profile_file:
            profile_file.write(profile)
        with open(bashrc_file_name, 'tw') as bashrc_file:
            bashrc_file.write('source ~/.profile')

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
                if e.only is None or 'bash' in e.only]

    def generate_alises(self):
        return [self.alias_to_string(e)
                for g in self.generators
                for e in g.generate_alises()
                if e.only is None or 'bash' in e.only]

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

    def alias_to_string(self, alias):
        return f'alias {alias.name}="{alias.value}"'

    def generate_update_function(self, fs):
        fs = [f.name for f in fs if f.name.startswith('update-')]
        return Function(
            'update',
            [],
            '\n'.join(fs)
        )
