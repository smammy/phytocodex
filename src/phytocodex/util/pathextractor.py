#!/usr/bin/env python3

from bs4 import BeautifulSoup
import sys
import traceback


def main():
    any_failure = False

    while path := sys.stdin.readline().rstrip("\r\n"):
        with open(path, errors="replace") as file:
            try:
                soup = BeautifulSoup(file, "lxml")
                for item in soup.find_all("div", {"class": "game-preview"}):
                    print(item.h2.a["href"])
            except Exception as ex:
                any_failure = True
                print(f"{path}: Problem making the soup!", file=sys.stderr)
                traceback.print_exception(ex, file=sys.stderr)

    sys.exit(1 if any_failure else 0)


if __name__ == "__main__":
    main()
