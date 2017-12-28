#!/usr/bin/env python3
"""Brute force well-known ETH addresses, WarGames-style.

Warning: this is utterly futile.  I've only done this to get a feel
for how secure private keys are against brute-force attacks.
"""

import sys
import time

import click
from ecdsa import SigningKey, SECP256k1
import sha3
import yaml

import targets
import trie

keccak = sha3.keccak_256()

@click.option('--skip-frames',
              default=0,
              help='Skip this many guesses when printing intermediate results.')
@click.option('--timeout-secs',
              default=-1,
              help='Stop trying after this many seconds, use -1 for forever.')
@click.command()
def main(skip_frames, timeout_secs):
    target_addresses = trie.EthereumAddressTrie(targets.targets())

    # count, address[:count]
    best_score = (0, '')

    # private key, public key, address
    best_guess = ('', '', '')

    frame_counter = 1
    total_tries = 0
    start_time = time.clock()

    try:
        while (timeout_secs < 0) or (time.clock() - start_time < timeout_secs):
            if best_score[0] >= 40:
                break
            total_tries +=1
            priv = SigningKey.generate(curve=SECP256k1)
            pub = priv.get_verifying_key().to_string()

            keccak.update(pub)
            address = keccak.hexdigest()[24:]

            current = target_addresses.Find(address)
            total_tries += 1
            frame_counter += 1

            if (skip_frames <= 0 or frame_counter > skip_frames):
                sys.stdout.write('\r%012.6f %08x %s %s' % (
                                 time.clock() - start_time,
                                 total_tries,
                                 priv.to_string().hex(),
                                 current))
                frame_counter = 1

            if current >= best_score:
                # always print the best guess
                sys.stdout.write('\r%012.6f %08x %s %s\n' % (
                                 time.clock() - start_time,
                                 total_tries,
                                 priv.to_string().hex(),
                                 current))
                best_score = current
                best_guess = (priv, pub, address)
    except KeyboardInterrupt:
        pass

    elapsed_time = time.clock() - start_time
    priv, pub, address = best_guess
    print('\n')
    print('Total guesses:', total_tries)
    print('Seconds      :', elapsed_time)
    print('Guess / sec  :', float(total_tries) / elapsed_time)
    print('Num targets  :', target_addresses.sizeof)
    print('Private key  :', priv.to_string().hex() if priv else priv)
    print('Public key   :', pub.hex() if pub else pub)
    print('Address      : 0x' + address if address else '???')


if '__main__' == __name__:
    main()
