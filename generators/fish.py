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
import os
import shutil
from os import path

from .common import Common
from .utils import Function


class FishGenerator:
    def __init__(self, generators):
        self.generators = [Common(), *generators]

    def generate_files(self):
        vs = self.generate_variables()
        fs = self.generate_functions()
        config = 'umask 077\n\n'
        config += '\n'.join(vs)
        config += '\n\nssh-add -A ^/dev/null\n\n'
        config += 'add_to_path_if_exists /usr/local/sbin\n'
        config += 'add_to_path_if_exists $HOME/bin\n'
        config += 'add_to_path_if_exists $HOME/.config/yarn/global/node_modules/.bin\n'
        config += 'add_to_path_if_exists $HOME/.cargo/bin\n'
        os.makedirs(path.expanduser('~/.config/fish/functions'), exist_ok=True)
        config_file_name = path.expanduser('~/.config/fish/config.fish')
        if path.exists(config_file_name):
            shutil.move(config_file_name, f'{config_file_name}.old')
        with open(config_file_name, 'tw') as config_file:
            config_file.write(config)
        for name, body in fs:
            fname = path.expanduser(f'~/.config/fish/functions/{name}.fish')
            if path.exists(fname):
                shutil.move(fname, f'{fname}.old')
            with open(fname, 'tw') as func_file:
                func_file.write(body)

    def generate_variables(self):
        return [self.var_to_string(e)
                for g in self.generators
                for e in g.generate_variables()]

    def generate_functions(self):
        fs = [g.generate_functions() for g in self.generators]
        fs = list(itertools.chain.from_iterable(fs))
        fs += [self.generate_update_function(fs)]
        fs += [self.generate_fish_print()]
        return [(e.name, self.func_to_string(e))
                for e in sorted(fs, key=lambda x: x.name)
                if e.only is None or 'fish' in e.only]

    def func_to_string(self, func):
        args = [a.replace('$', '') for a in func.args]
        args = [f'set {arg} $argv[{i+1}]' for i, arg in enumerate(args)]
        f = f"function {func.name}\n\t"
        f += '\n\t'.join(args) + ('\n\t' if len(args) else '')
        f += func.body.replace('\n', '\n\t')
        f += '\nend'
        return f

    def var_to_string(self, var):
        return f'set -x {var.name} {var.value.replace("$(", "(")}'

    def generate_update_function(self, fs):
        fs = [f.name for f in fs if f.name.startswith('update-')]
        return Function(
            'update',
            [],
            '\n'.join(fs)
        )

    def generate_fish_print(self):
        return Function(
            'fish_print',
            [],
            (
                'set_color cyan\n'
                'echo -n (basename (prompt_pwd))\n'
                'set_color green\n'
                'echo -n " $ "\n'
                'set_color normal'
            )
        )
