#!/usr/bin/env python3
"""Recursively walk transactions from a given ETH address to find more."""


import click


@click.command()
@click.argument('addresses', nargs=-1)
def main(addresses):
    for addr in addresses:
        click.echo('Hello %s' % (addr,))


if '__main__' == __name__:
    main()
