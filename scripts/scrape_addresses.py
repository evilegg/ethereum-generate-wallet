#!/usr/bin/env python3
"""Fetch addresses from the Ethereum ledger using etherscan.io."""

import collections
import sys

from bs4 import BeautifulSoup
import click
import requests
import yaml


def _parse_etherscan_accounts_page(html_text):
    """Parse the account information out of the webscrape."""
    soup = BeautifulSoup(html_text, 'html.parser')

    retval = []
    div = soup.find('div', attrs={'class': 'table-responsive'})
    if not div:
        return retval

    headings = [str(th.find(text=True)) for th in div.findAll('th') if th]
    for tr in div.findAll('tr'):
        cols = [str(td.find(text=True)) for td in tr.findAll('td') if td]
        row = dict(zip(headings, cols))
        address = row.get('Address', '0x')[2:]
        if address:
            retval.append(address)

    return retval


@click.command()
@click.option('--start', default=0, help='First page to scrape.')
@click.option('--end', default=10, help='Last page to scrape.')
@click.option('--outfile',
              type=click.File('w'),
              help='Write addresses (in yaml) to this file.')
def main(start, end, outfile):
    """Scrape https://etherscan.io for the top ETH addresses."""
    all_addrs = collections.OrderedDict()

    for page_num in range(start, end + 1):
        before = len(all_addrs)

        url = 'https://etherscan.io/accounts/%d' % (page_num,)
        reply = requests.get(url)
        for addr in _parse_etherscan_accounts_page(reply.text):
            all_addrs[addr] = True
        print('%s added %d new addresses' % (url, len(all_addrs) - before))

    print('Total addresses found:', len(all_addrs))

    outfile = outfile or sys.stdout
    yaml.safe_dump(list(all_addrs.keys()), outfile, default_flow_style=False)

    
if '__main__' == __name__:
    main()
