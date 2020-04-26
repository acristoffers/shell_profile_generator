This generator replicates some of the configuration (variables and functions)
that I use on my machine. I made it to make it easier for me to generate those
profiles on Linuxes installed in virtual machines, as well as non-tech friends
who ask for assistance.

It will backup your old files, renaming them with the suffix .old, and then
generate new files.

Variables defined
-----------------

- HOME=~
- LC_ALL=your current locale
- LC_LANG=$LC_ALL
- DISPLAY='' # on macOS
- DISPLAY=current value of $DISPLAY # on Linux
- EDITOR=code
- PYTHON=$(which python3)
- PS1, to make the terminal default message be:
  - \blue{current folder name} \green{$}

Adds to PATH
------------

- /usr/local/sbin
- ~/bin
- ~/.config/yarn/global/node_modules/bin
- ~/.cargo/bin

Executes
--------

- `ssh-add -A &> /dev/null` # to prevent ssh from asking for a password - every time.
- sources bash_completion, if exists # bash only, obviously
- binds up and down keys to make history search MATLAB-like # bash and zsh

Define Functions
----------------

- add_to_path_if_exists # prepend to PATH if folder - exists
- ccat # coloured cat, requires pygmentize
- tbz, tgz, txz # tar and compress a given folder, - best compression
- zipup # zips a given folder, best compression
- update-* # updates the given package manager, for example, update-apt will run 
`sudo apt update; sudo apt-get dist-upgrade -y; sudo apt-get autoremove -y`
- update # runs all update-* functions

macOS only (value might need adjusting):

- rep, rep2, rep3, rep4 # reposition and resize the Terminal window
- fv # makes the Terminal window occupy 1/3 of horizontal space and all vertical
  space (155x60) on my monitor (1440x900, Retina Display, 15" Macbook Pro). "for
  vim".
