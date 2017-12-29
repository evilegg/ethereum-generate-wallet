# Ethereum Private Key Brute Force Attacker

A simple python script to generate public addresses and compare to known
ETH addresses.

```
Usage: brute_force_app.py [OPTIONS]

Options:
  --target-cache FILENAME  Local yaml file containing target addresses
  --timeout-secs INTEGER   Stop trying after this many seconds, use -1 for
                           forever.
  --fps INTEGER            Use this many frames per second when showing
                           guesses.  Use non-positive number to go as fast as
                           possible.
  --help                   Show this message and exit.
```

Thanks to
[@vkobel/ethereum-generate-wallet](https://github.com/vkobel/ethereum-generate-wallet)
for the pure python implementation of ETH key generation.

## Why?

I wanted a more tangible understanding of how hard it is to guess a
private key before using it to store any non-trivial value.  I mean, how
hard could it be to guess someone else's key?  As this script tries to
show, it's basically impossible to collide with an already existing key.

How many leading digits can you match?  ;)

Note: having a 39 digit match of the address means you're no closer to
unlocking anything.

## Python dependencies

- click
- ECDSA
- pysha3
- pyyaml

This script uses python3.  Its dependencies are listed in
`requirements.txt`.  Use virtualenv to install and execute this script
without affecting your system's python3 distribution:

```bash
$ virtualenv -p python3 venv
$ . ./venv/bin/activate
$ pip install -r requirements.txt
$ ./brute_force_app.py --timeout-secs 10

$ deactivate
```

You can skip the virtualenv and install the necessary dependencies to
your system's python3 distribution:

```bash
pip install -r requirements.txt
```
