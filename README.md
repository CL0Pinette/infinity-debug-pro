# infinity-debug-pro

## Setup

### On NixOs or if you have Nix package manager : 
```sh
$ nix-shell
# then jump to Usage within the nix shell
```

### On other distros
```sh
$ python3 -m venv .venv
$ . .venv/bin/activate
(venv)$ pip3 install -r requirements.txt
```

## Usage
```sh
$ ./main.py url login path
```
The url is the complete URL of the subject http://....html

The login is your full login

The path given is a relative path from where you launch the
script to the directory where all the files will be created
