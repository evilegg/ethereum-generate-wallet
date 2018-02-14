#!/usr/bin/env python3
"""Given a block-id, crawl the transactions for ETH addresses.

Given a block-id on the command line, go through every transaction collecting
the public addresses.  Recursively.
"""

import click
import yaml
def scrape_block(block, page):
    """Scrape a full block and return all addresses"""
    eth_addrs = set()
    return eth_addrs


@click.command()
@click.option('--first-block', required=True, type=int)
@click.option('--last-block', type=int)
@click.option('--outfile', type=click.File('w'))
def main(first_block, last_block, outfile):

    last_block = last_block or last_block + 1
    eth_addrs = set()
    for block in range(first_block, last_block + 1):
        eth_addrs.update(scrape_block(block, 1))

    yaml.safe_dump(list(eth_addrs), outfile or sys.stdout, default_flow_style=False)
    click.echo('# Total %d addresses found' % len(eth_addrs))


if '__main__' == __name__:
    main()
