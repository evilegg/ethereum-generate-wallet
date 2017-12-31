# Ethereum Private Key Brute Force Attacker

A simple, pure-python script to generate private keys and compare the
resulting ETH addresses with a list of known values.  Strength of each
guess is measured by the number of leading hexadecimal digits that match
(other digits may match, but we don't count those).

While guessing, the script shows its guesses WarGames-style.

## Usage

```
Usage: brute_force_app.py [OPTIONS]

Options:
  --addresses FILENAME  Filename for yaml file containing target addresses.
  --timeout INTEGER     If set to a positive integer, stop trying after this
                        many seconds.
  --fps INTEGER         Use this many frames per second when showing guesses.
                        Use non-positive number to go as fast as possible.
  --help                Show this message and exit.
```

Thanks to
[@vkobel/ethereum-generate-wallet](https://github.com/vkobel/ethereum-generate-wallet)
for the pure-python implementation of ETH key generation.

## Why?

I wanted a more tangible understanding of how hard it is to guess a
private key before using it to store any non-trivial value.  I mean,
_how hard could it be to guess someone else's key, **right**_?  As this
script tries to show, it's basically impossible to collide with an
already existing key.

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
$ ./brute_force_app.py --timeout 5
Loaded 10000 addresses

duration     attempts private-key                                                      str address
00000.000006 00000001 0d5a730468b5ed565a89b03cf8f6228a4b4d8c75c7fbd1d31b4ef9f003d5660c   3 e0a                                     
00000.277911 00000005 100276e5d5f35d065c9a925b08785c55a8c1497f1dbad970b16d9adbf7e670a0   3 ff1                                     
00000.972975 0000000f c6b40ef08f92ffb8b3b36fa5f65de72daddd0a05da82943deadfa3a63813779f   4 00fb                                    
00001.666908 00000019 911dea430f2b8403f9cbb2f4dcae2e5ea6943b05916d4a3ec9e3ed68927cbc86   4 d301                                    
00004.998683 00000049 8fa41f3e7fb335e0fa6435d2d905eb996c251f2ff98c5fa7719ad88030c59c2c   2 78                                      

Total guesses: 73
Seconds      : 5.068186
Guess / sec  : 14.403575559381602
Num targets  : 10000

Best Guess
Private key  : 911dea430f2b8403f9cbb2f4dcae2e5ea6943b05916d4a3ec9e3ed68927cbc86
Public key   : af71d473026d92073ed27de65b04d523ffa897d59b965ba5aeaa4e29a535f3e3e7dac768a6c3b2ed88d00415472d30fb39ed0a825d54c8070f896fc23d3e67e8
Address      : 0xd301b4bf0ab57e50c2aa5451df29d58e89538ed0
Strength     : 4 of 40 digits (10.00%)

$ deactivate
```

Not recommended: you can skip the `virtualenv` steps and install the
necessary dependencies to your system's python3 distribution:

```bash
$ pip install -r requirements.txt
$ python3 ./brute_force_app.py
...
```
