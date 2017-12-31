# Ethereum Private Key Brute Force Attacker

A simple python script to generate public addresses and compare to known
ETH addresses.
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
private key before using it to store any non-trivial value.  I mean, *how
hard could it be to guess someone else's key, right*?  As this script tries to
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
$ ./brute_force_app.py --timeout-secs 5
00000.000001 00000001 c9476bbecf231a3a89cecf24cada81557ac1323f0505c2641bf630f31a223011 00                                         
00000.069983 00000002 b4b7d2df51340ff58f4c576138debb1047a072f94a210b550acc088898cfb8e3 00                                         
00000.137207 00000003 eebc8625e1c646be11a7ddcf97a44cee2a23c895617edf575e816097d6e1c965 00                                         
00000.204091 00000004 bdba8a78e9f19fc36ac01ef58760edf015016bece63f4de60beed97db85410e5 00                                         
00000.269997 00000005 ef6baf284d99ca0818cba813e363ae88d2c984a5092754734ae48c3a47dc0857 00                                         
00000.337298 00000006 413371904a05924c2f769db2e37fbb8e84fe13232c8efb02bbdebfa5d69486a0 00                                         
00000.404130 00000007 f639a976600e1f5f3be2cbe93a50e4705c7aa2792bfeea6ebbb9ddb4547582d9 00                                         
00000.470867 00000008 fdb8e58d66e9de3ba9027a2e012f2e62f8de6981f17f1df21629557c03ebbd00 01 0                                       
00001.456314 00000017 2a628e13085ae1dbfd77910713c9faf4001adcb0befb224f4c032a308f7ba494 01 0                                       
00002.115780 00000021 b7e27d567ae89a8495d1340e728b8e2469fdd4aa4f3c7186316e87263ccd0ead 01 0                                       
00004.161634 00000040 62c44a70a11a63c6088ead6f93da082528115d458a5365cee571ad03e7381138 01 0                                       
00004.294037 00000042 29f566232e8ac6f808c826450036b78dffc9d3f26366dec4560ac3f894cd7ca6 01 0                                       
00004.892894 0000004b e140f05248eea21646d78d652b8a4f27870c88e66d3ec7ee02c4b39cf496bda6 01 0                                       
00004.958686 0000004c d34990ceee36926486b8cee6af24d3b5a7900ea66f60499e22680e843c55ff82 00                                         

Total guesses: 76
Seconds      : 5.025855
Guess / sec  : 15.121805145592143
Num targets  : 100
Private key  : e140f05248eea21646d78d652b8a4f27870c88e66d3ec7ee02c4b39cf496bda6
Public key   : 5c2500440c29a30a49600a40767216757c1fedd50887c13489500a4dc0d8abf1d3c4d9839739ef0a369ebd2aeb2fbbfe2a3c24d7ae9a43f064fab1045e7e02c2
Address      : 0x0c808880e40333d3b4e358cc43d107dfd6196b5d

$ deactivate
```

You can skip the virtualenv and install the necessary dependencies to
your system's python3 distribution:

```bash
pip install -r requirements.txt
```
