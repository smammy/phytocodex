#!/usr/bin/env python3

from argparse import ArgumentParser
from collections import namedtuple
from datetime import datetime
from pathlib import Path
from textwrap import TextWrapper
from urllib.parse import urlparse, urljoin
import json
import re
import sys
import traceback

from bs4 import BeautifulSoup
from html2text import HTML2Text
from psycopg import Rollback
import psycopg

from ..config import PGURL, MGURL

wsrun = re.compile(r"\s+")
vsrun = re.compile(r"[\n\v\f\r\u0085\u2028\u2029]+")
hsrun = re.compile(r"[^\S\n\v\f\r\u0085\u2028\u2029]+")

stats_columns = {"list_size", "items_crawled"}


def main():
    global opts
    
    parser = ArgumentParser()
    parser.add_argument('--stat-list-size', type=int)
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--go-hard', action='store_true')
    parser.add_argument('--log-queries', action='store_true')
    parser.add_argument('--prune', action='store_true')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('paths', metavar='FILE', nargs="+")
    opts = parser.parse_args()
    stats = dict((k[5:], v) for (k, v) in vars(opts).items() if k[:5]=="stat_")
    
    with psycopg.connect(PGURL) as conn:
        with conn.cursor() as cur:
            bump_generation(cur)
            
            crawled = 0
            failures = 0
            
            for path in gen_paths(opts.paths, sys.stdin):
                crawled += 1
                if opts.verbose:
                    eprint(f"Processing {path}...")
                succeeded = process_path(cur, path)
                if not succeeded:
                    failures += 1
                    if opts.go_hard:
                        if opts.verbose:
                            eprint("Bravely persevering...")
                        continue
                    else:
                        if opts.verbose:
                            eprint("Cowardly giving up.")
                        break
            
            if opts.verbose:
                eprint(f"{failures} failure(s) while processing.")
            
            if failures and not opts.go_hard:
                raise Rollback
            elif opts.prune:
                prune_database(cur)
            
            stats["items_crawled"] = crawled
            update_stats(cur, stats)


def gen_paths(args, stdin):
    for arg in args:
        meta = False
        if arg[0] == "@":
            meta = True
            arg = arg[1:]
        if arg == "-":
            arg = stdin.fileno()
        if meta:
            with open(arg) as file:
                for line in file:
                    yield line.rstrip("\r\n")
        else:
            yield arg


def process_path(cur, path):
    try:
        file = open(path, errors="surrogateescape")
        soup = BeautifulSoup(file, "lxml")
        drink_the_soup(cur, soup)
        return True
    except Exception as ex:
        eprint(f"\nFailed processing {path}:")
        traceback.print_exception(ex, file=sys.stderr)
        if opts.debug and soup is not None:
            eprint("\nHere's the soup:\n")
            eprint(soup.prettify())
        return False


def drink_the_soup(cur, soup):
    tagsdiv = soup.find("div", class_="descr")
    path = urlparse(soup.find("link", rel="canonical")["href"]).path
    descr = extract_description(soup)
    
    insert_item(cur, dict(
        path=path,
        name=fix_space(soup.h1.get_text()),
        year=extract_tag(tagsdiv, "Year released:"),
        descr_html=descr,
        descr_text=html_to_text(descr),
    ))
    
    for (tagpath, tagname) in extract_taglist(tagsdiv, "Category:"):
        insert_tag(cur, dict(
            _type="category",
            _rel="category",
            itempath=path,
            tagpath=tagpath,
            tagname=tagname,
        ))
    
    for (tagpath, tagname) in extract_taglist(tagsdiv, "Author:"):
        insert_tag(cur, dict(
            _type="author",
            _rel="author",
            itempath=path,
            tagpath=tagpath,
            tagname=tagname,
        ))
    
    for (tagpath, tagname) in extract_taglist(tagsdiv, "Publisher:"):
        insert_tag(cur, dict(
            _type="author",
            _rel="publisher",
            itempath=path,
            tagpath=tagpath,
            tagname=tagname,
        ))
    
    for download in extract_downloads(tagsdiv):
        insert_download(cur, download | dict(itempath=path))


def fix_space(text, multiline=False):
    if multiline:
        return vsrun.sub("\n", hsrun.sub(" ", text)).strip()
    else:
        return wsrun.sub(" ", text).strip(" \n")


def extract_tag(soup, label):
    tags = extract_taglist(soup, label)
    if len(tags):
        return tags[0][1]
    else:
        return None


def extract_taglist(soup, label):
    alist = soup.find("td", string=label).find_next_sibling("td").find_all("a")
    return [(atag["href"], fix_space(atag.get_text())) for atag in alist]


def extract_description(soup):
    html = ""
    
    elem = soup.find("div", class_="game-preview")
    stop = elem.parent.find("strong", string="Compatibility", recursive=False)
    while elem := elem.next_sibling:
        if elem == stop:
            break
        html += str(elem)
    
    return html


def html_to_text(html):
    h2t = HTML2Text(baseurl=MGURL)
    h2t.unicode_snob = True
    h2t.body_width = 70
    h2t.inline_links = False
    h2t.wrap_links = False
    h2t.wrap_list_items = True
    h2t.wrap_tables = True
    h2t.ignore_emphasis = True
    
    return h2t.handle(html).rstrip()


def extract_downloads(soup):
    downloads = []
    
    for downloaddiv in soup.find_all("div", class_="download"):
        try:
            downloads.append(extract_download(downloaddiv))
        except Exception as ex:
            if opts.verbose:
                eprint("\nOdd download, skipping it.\n")
                traceback.print_exception(ex, file=sys.stderr)
                if opts.debug:
                    eprint("\nHere it is:\n")
                    eprint(downloaddiv.prettify())
    
    return downloads


def extract_download(soup):
    number = soup.find("div", class_="numeral").get_text()
    assert number.startswith("#")
    
    atags = soup.find_all("a")
    md5 = atags.pop().get_text()
    urls = [urljoin(MGURL, atag["href"]) for atag in atags]
    
    fileinfo = ""
    for tag in soup.find("br").next_siblings:
        if tag.name == "br":
            break
        fileinfo += tag.get_text()
    name_and_size = re.match(r"(.*?) \((.*)\)", fix_space(fileinfo))
    
    return dict(
        number=fix_space(number[1:]),
        name=fix_space(name_and_size[1]),
        size=fix_space(name_and_size[2]),
        md5=fix_space(md5),
    )


def bump_generation(cur):
    maybe_execute(cur, """
        UPDATE dbmeta
        SET generation=generation+1, lastupdate=now()
        RETURNING generation;
    """)
    
    if opts.verbose:
        if opts.dry_run:
            eprint(f"Would have incremented generation.")
        else:
            generation = cur.fetchone()[0]
            eprint(f"Incremented generation to {generation}.")


def update_stats(cur, stats):
    for col, val in stats.items():
        if col in stats_columns:
            maybe_execute(cur, f"UPDATE dbmeta SET {col}=%s", (val,))
            if opts.verbose:
                if opts.dry_run:
                    eprint(f"Would have set stat {col} to {val}.")
                else:
                    eprint(f"Set stat {col} to {val}.")


def insert_item(cur, item):
    maybe_execute(cur, """
        INSERT INTO item (path, name, year, descr_html, descr_text)
        VALUES (%(path)s, %(name)s, %(year)s, %(descr_html)s, %(descr_text)s)
        ON CONFLICT (path) DO UPDATE
        SET generation=DEFAULT, name=%(name)s, year=%(year)s,
            descr_html=%(descr_html)s, descr_text=%(descr_text)s;
    """, item)


def insert_tag(cur, tag):
    maybe_execute(cur, f"""
        INSERT INTO {tag['_type']} (path, name)
        VALUES (%(tagpath)s, %(tagname)s)
        ON CONFLICT (path) DO UPDATE
        SET generation=DEFAULT, name=%(tagname)s;
    """, tag)
    
    maybe_execute(cur, f"""
        INSERT INTO item_{tag['_rel']} (item_path, {tag['_type']}_path)
        VALUES (%(itempath)s, %(tagpath)s)
        ON CONFLICT (item_path, {tag['_type']}_path) DO UPDATE
        SET generation=DEFAULT;
    """, tag)


def insert_download(cur, download):
    maybe_execute(cur, f"""
        INSERT INTO download (item_path, number, name, size, md5)
        VALUES (%(itempath)s, %(number)s, %(name)s, %(size)s, %(md5)s)
        ON CONFLICT (item_path, number) DO UPDATE
        SET generation=DEFAULT, name=%(name)s, size=%(size)s, md5=%(md5)s;
    """, download)


def prune_database(cur):
    for table in [
        "download", "item_category", "item_author", "item_publisher",
        "item_sysver", "category", "author", "item",
    ]:
        maybe_execute(cur, f"""
            DELETE FROM {table}
            WHERE generation < generation();
        """, dict(table=table))
        
        if opts.verbose:
            if opts.dry_run:
                eprint(f'Would haved pruned "{table}".')
            else:
                rows = cur.rowcount
                eprint(f'Pruned {rows} rows from "{table}".')


def eprint(*args, file=sys.stderr, **kwargs):
    print(*args, file=file, **kwargs)


def maybe_execute(cur, *args, **kwargs):
    if opts.log_queries:
        eprint(format_call("execute", args, kwargs))
    
    if not opts.dry_run:
        cur.execute(*args, **kwargs)
    
    return cur


def format_call(name, args, kwargs):
    return f"{name}(" + ", ".join(
        [f"{v!r}" for v in args] + [f"{k}={v!r}" for k, v in kwargs.items()],
    ) + ")"


if __name__ == "__main__":
    main()
