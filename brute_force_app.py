#!/usr/bin/env python3
"""Brute force well-known ETH addresses, WarGames-style.

Warning: this is utterly futile.  I've only done this to get a feel
for how secure private keys are against brute-force attacks.
"""

import os
import sys
import threading
import time

import click
from ecdsa import SigningKey, SECP256k1
import sha3
import yaml

import monitoring
import targets
import trie

keccak = sha3.keccak_256()


try:
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
except:
    DATA_DIR = os.path.join(os.getcwd(), 'data')


ETH_ADDRESS_LENGTH = 40


def EchoLine(duration, attempts, private_key, strength, address, newline=False):
    """Write a guess to the console."""
    click.secho('\r%012.6f %08x %s % 3d ' % (duration,
                                             attempts,
                                             private_key,
                                             strength),
                nl=False)
    click.secho(address[:strength], nl=False, bold=True)
    click.secho(address[strength:], nl=newline)


def EchoHeader():
    """Write the names of the columns in our output to the console."""
    click.secho('%-12s %-8s %-64s %-3s %-3s' % ('duration',
                                                'attempts',
                                                'private-key',
                                                'str',
                                                'address'))


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
@click.option('--port',
              default=8120,
              help='Monitoring port')
@click.command()
def main(fps, timeout, addresses, port):
    target_addresses = trie.EthereumAddressTrie(targets.targets(addresses))
    click.echo('Loaded %d addresses\n' % (target_addresses.length()))

    httpd = monitoring.Start('', port)
    varz = monitoring.Stats()

    varz.fps = fps
    varz.timeout = timeout if timeout > 0 else 'forever'

    # score is tuple of number of matching leading hex digits and that
    # portion of the resulting public key: (count, address[:count])
    varz.best_score = (0, '')
    varz.difficulty = monitoring.ComputedStat(
        lambda m: '%d of 40 digits (%3.2f%%)' % (m.best_score[0],
                                                 100.0 * m.best_score[0] / 40.0)
    )

    # count the number of private keys generated
    varz.num_tries = 0
    varz.guess_rate = monitoring.ComputedStat(
        lambda m: float(m.num_tries) / m.elapsed_time, units='guesses/sec')

    # keep a histogram of guess strengths
    varz.strength_histogram = {}

    # tuple of private key, public key, address
    varz.best_guess = ('', '', '?' * 40)
    varz.best_guess_human = monitoring.ComputedStat(
        lambda m: dict(zip(('private-key', 'public-key', 'address'), m.best_guess)))

    # calculate the fps
    fps = 1.0 / float(fps) if fps > 0 else fps
    last_frame = 0

    start_time = time.clock()
    varz.start_time = time.asctime(time.localtime(start_time))

    EchoHeader()
    try:
        while varz.best_score[0] < ETH_ADDRESS_LENGTH:
            now = time.clock()
            varz.elapsed_time = now - start_time
            if (timeout > 0) and (start_time + timeout < now):
                break

            varz.num_tries += 1

            priv = SigningKey.generate(curve=SECP256k1)
            pub = priv.get_verifying_key().to_string()

            keccak.update(pub)
            address = keccak.hexdigest()[24:]

            current = target_addresses.Find(address)
            strength, _ = current
            varz.strength_histogram[strength] = varz.strength_histogram.get(strength, 0) + 1

            if last_frame + fps < now:
                EchoLine(now - start_time,
                         varz.num_tries,
                         priv.to_string().hex(),
                         current[0],
                         current[1])
                last_frame = now

            # the current guess was as close or closer to a valid ETH address
            # show it and update our best guess counter
            if current >= varz.best_score:
                EchoLine(now - start_time,
                         varz.num_tries,
                         priv.to_string().hex(),
                         current[0],
                         current[1],
                         newline=True)
                varz.best_score = current
                varz.best_guess = (priv.to_string().hex(), pub.hex(), address)
    except KeyboardInterrupt:
        pass

    monitoring.Stop(httpd)

    varz.elapsed_time = time.clock() - start_time
    private_key, public_key, eth_address = varz.best_guess
    print('\n')
    print('Total guesses:', varz.num_tries)
    print('Seconds      :', varz.elapsed_time)
    print('Guess / sec  :', float(varz.num_tries) / varz.elapsed_time)
    print('Num targets  :', target_addresses.length())
    print('')
    print('Best Guess')
    print('Private key  :', private_key)
    print('Public key   :', public_key)
    print('Address      :', eth_address)
    print('Strength     : %d of 40 digits (%3.2f%%)' %
        (varz.best_score[0], 100.0 * varz.best_score[0] / 40.0))


if '__main__' == __name__:
    main()
