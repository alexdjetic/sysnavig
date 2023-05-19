# sysnavig

## about me
this a projeck that i use in my personal server to only see current process, and being use only for terminal  

## description
- this is a alternative to the command `htop`
- ⛔ only work on linux ⛔

## install python3

### debian/debian fork
- install python3: `apt install python python-pip git`
- clone the repository: `git clone https://github.com/alexdjetic/sysnavig.git`
- install the library: `pip install -r requirements.txt`

### → alpine
- install python3: `apk add python python-pip git`
- clone the repository: `git clone https://github.com/alexdjetic/sysnavig.git`
- install the library: `pip install -r requirements.txt`

### → archlinux
- install python3: `pacman -S python python-pip git`
- clone the repository: `git clone https://github.com/alexdjetic/sysnavig.git`
- install the library: `pip install -r requirements.txt`

### → fedora
- install python3: `dnf install python python-pip git`
- clone the repository: `git clone https://github.com/alexdjetic/sysnavig.git`
- install the library: `pip install -r requirements.txt`

## launching
give the execution right to this utility: `chmod +x *.py` ✅

## shortcut
create a shorcut, go to your directory using `cd ~/sysnavig`
use these follow command:
```zsh
#!/bin/sh

sudo cp *.py /bin/
sudo mv main.py sysnavig
sudo chmod +x *.py
```
now you can launch without giving the path ✅

## the next advancement
i want to improve this command to add the feature:
- network access: true graph
- process manupilation: stop, create, interupt
- manual page
- log activity

