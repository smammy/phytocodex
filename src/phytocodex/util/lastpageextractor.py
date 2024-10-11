#!/usr/bin/env python3

from bs4 import BeautifulSoup
import sys


def main():
    soup = BeautifulSoup(sys.stdin, "lxml")
    print(soup.find("li", class_="pager-last").a["href"].split("=")[-1])


if __name__ == "__main__":
    main()
