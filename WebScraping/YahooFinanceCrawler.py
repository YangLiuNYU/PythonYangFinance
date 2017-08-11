#!/usr/bin/python
import sys
import argparse
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

## Return command line arguments
def get_arguments():
    """
    Return command line arguments.
    """
    parser = argparse.ArgumentParser(
        description=("Script for reindexing documents from one index."))
    parser.add_argument("--get_statistics",
                      action = "store",
                      dest = "ticker",
                      help = "Get statistics information for a ticker.")

    return parser.parse_args()


def get_statistics(ticker):
    """
    Scrapeing yahoo finance page to get statistics information
    for a security. Return a key-value hashmap
    """
    hash_map = {}
    try :
        resp = requests.get('https://finance.yahoo.com/quote/AAPL/key-statistics?p=' + ticker)
        bsObj = BeautifulSoup(resp.text, "html.parser")
        statistics_section = bsObj.find("section", {"id":"quote-leaf-comp"}).findAll("tr")
        #print statistics_section

        for item in statistics_section:
            records = item.findAll("td")
            key = records[0].find("span").text
            value = records[1].text
            hash_map[key] = value
    except ConnectionError as e:
        print(e)

    return hash_map


if __name__ == "__main__":
    args = get_arguments()
    if args.ticker:
        apple_mapper = get_statistics(args.ticker)
        for key in apple_mapper:
            print key + " : " + apple_mapper[key]
        print "Done."
    sys.exit(0)
