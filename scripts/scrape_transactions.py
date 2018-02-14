#!/usr/bin/env python3
"""Given a block-id, crawl the transactions for ETH addresses.

Given a block-id on the command line, go through every transaction collecting
the public addresses.  Recursively.
"""

import os
import random
import re
import sys
import time
import urllib.parse

from bs4 import BeautifulSoup
import click
import requests
import yaml


def _find_last_page(html_text):
    """Scan the HTML for the Last page, and return a list of relative URLs."""
    soup = BeautifulSoup(html_text, 'html.parser')

    # Searching for 'https://etherscan.io/txs?block=5066192&p=2'
    last_page = soup.find('a',
                          attrs={'class': 'btn btn-default btn-xs logout'},
                          string='Last')
    if not last_page:
        return 1
    url = last_page.get('href')
    last_page = urllib.parse.parse_qs(url).get('p', ['0'])
    return int(last_page[0])


def _find_addresses_in_page(html_text):
    """Scrape addresses from block-id page."""
    soup = BeautifulSoup(html_text, 'html.parser')
    addresses = soup.find_all('a', href=re.compile('^/address/0x([a-z0-9]+)'))
    addr_urls = [a.get('href') for a in addresses]
    return set([url.split('/', 2)[-1] for url in addr_urls])


def get_block(block_id, page_number):
    """Get the HTML for a particular block."""
    pth = 'data/block-%d.html' % (block_id,)
    if page_number != 1:
        pth = 'data/block-%d-%d.html' % (block_id, page_number)

    if os.path.exists(pth):
        with open(pth) as fin:
            return fin.read()
    else:
        url = 'https://etherscan.io/txs?block=%d&p=%d' % (block_id,
                                                          page_number)
        done = False
        while not done:
            try:
                reply = requests.get(url)
                done = True
            except:
                # sleep 3 - 10 seconds when rate-limited
                time.sleep(3.0 + 7.0 * random.random())

        with open(pth, 'w') as fout:
            fout.write(reply.text)
            return reply.text


def echo_new_addresses_found(block, page, existing_addresses, new_addresses):
    click.echo('# block=%d, page=%d, %d new addresses found' % (
        block, page, len(new_addresses.difference(existing_addresses))))


def scrape_block(block, page):
    """Scrape a full block and return all addresses"""
    eth_addrs = set()

    reply = get_block(block, page)
    last_page = _find_last_page(reply)

    new_addrs = _find_addresses_in_page(reply)
    echo_new_addresses_found(block, page, eth_addrs, new_addrs)
    eth_addrs.update(new_addrs)

    page_num = 2
    while page_num < last_page:
        reply = get_block(block, page_num)
        new_addrs = _find_addresses_in_page(reply)
        echo_new_addresses_found(block, page, eth_addrs, new_addrs)
        eth_addrs.update(new_addrs)
        page_num += 1
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
