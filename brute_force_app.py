#!/usr/bin/env python3
"""Brute force well-known ETH addresses, WarGames-style.

Warning: this is utterly futile.  I've only done this to get a feel
for how secure private keys are against brute-force attacks.
"""

import os
import sys
import time

import click
from ecdsa import SigningKey, SECP256k1
import sha3
import yaml

import targets
import trie

keccak = sha3.keccak_256()


try:
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
except:
    DATA_DIR = os.path.join(os.getcwd(), 'data')
ETH_ADDRESS_LENGTH = 40
OUTPUT_FORMAT = '\r%012.6f %08x %s % 3d %-40s'
HEADER_STR = '%-12s %-8s %-64s %-3s %-3s' % ('duration',
                                             'attempts',
                                             'private-key',
                                             'str',
                                             'address')


@click.option('--fps',
              default=60,
              help='Use this many frames per second when showing guesses.  '
                   'Use non-positive number to go as fast as possible.')
@click.option('--timeout',
              default=-1,
              help='If set to a positive integer, stop trying after this many '
                   'seconds.')
@click.option('--addresses',
              type=click.File('r'),
              default=os.path.join(DATA_DIR, 'addresses.yaml'),
              help='Filename for yaml file containing target addresses.')
@click.command()
def main(fps, timeout, addresses):
    target_addresses = trie.EthereumAddressTrie(targets.targets(addresses))
    print('Loaded %d addresses' % (target_addresses.length()))

    # count, address[:count]
    best_score = (0, '')

    # private key, public key, address
    best_guess = ('', '', '')

    num_tries = 0

    # calculate the fps
    fps = 1.0 / float(fps) if fps > 0 else fps
    last_frame = 0

    start_time = time.clock()

    print(HEADER_STR)
    try:
        while best_score[0] < ETH_ADDRESS_LENGTH:
            now = time.clock()
            if (timeout > 0) and (start_time + timeout < now):
                break

            num_tries += 1

            priv = SigningKey.generate(curve=SECP256k1)
            pub = priv.get_verifying_key().to_string()

            keccak.update(pub)
            address = keccak.hexdigest()[24:]

            current = target_addresses.Find(address)

            if last_frame + fps < now:
                sys.stdout.write(OUTPUT_FORMAT % (
                                 now - start_time,
                                 num_tries,
                                 priv.to_string().hex(),
                                 current[0],
                                 current[1]))
                last_frame = now

            # the current guess was as close or closer to a valid ETH address
            # show it and update our best guess counter
            if current >= best_score:
                sys.stdout.write((OUTPUT_FORMAT + '\n') % (
                                 now - start_time,
                                 num_tries,
                                 priv.to_string().hex(),
                                 current[0],
                                 current[1]))
                best_score = current
                best_guess = (priv, pub, address)
    except KeyboardInterrupt:
        pass

    elapsed_time = time.clock() - start_time
    priv, pub, address = best_guess
    print('\n')
    print('Total guesses:', num_tries)
    print('Seconds      :', elapsed_time)
    print('Guess / sec  :', float(num_tries) / elapsed_time)
    print('Num targets  :', target_addresses.length())
    print('Private key  :', priv.to_string().hex() if priv else priv)
    print('Public key   :', pub.hex() if pub else pub)
    print('Address      : 0x' + address if address else '???')


if '__main__' == __name__:
    main()
