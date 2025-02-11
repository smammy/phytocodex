#!/usr/bin/env python3

from argparse import ArgumentParser, BooleanOptionalAction
from bs4 import BeautifulSoup
from datetime import timedelta
from pathlib import Path
from requests import Request
from requests.adapters import HTTPAdapter
from requests_cache import CachedSession
from urllib3 import Retry
import sys

retry_on_status = Retry.RETRY_AFTER_STATUS_CODES | set([500, 502, 503, 504])
cache_expire_after = timedelta(days=1)


def main():
    global opts
    global session
    
    parser = ArgumentParser()
    parser.add_argument("-d", "--item-dir", type=Path, default=Path("items"))
    parser.add_argument("--user-agent",
        default="Phytocodexbot/2 (sam+phyt@porcupine.club)")
    parser.add_argument("--no-proxies", action="store_true")
    parser.add_argument("--write-count", action=BooleanOptionalAction,
        default=True, help="write item count to ITEM_DIR/.count")
    parser.add_argument("collection", nargs="+")
    opts = parser.parse_args()
    
    session = CachedSession(
        cache_name="phytocodex/request-cache",
        expire_after=cache_expire_after,
        cache_control=True,
        use_cache_dir=True,
    )
    session.headers["User-Agent"] = opts.user_agent
    if not opts.no_proxies:
        session.proxies["http"] = "http://localhost:3128"
        session.proxies["https"] = "http://localhost:3128"
    retry = Retry(status_forcelist=retry_on_status, backoff_factor=0.1)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    #session.cache.reset_expiration(cache_expire_after)
    #sys.exit()
    
    item_count = 0
    for collection in opts.collection:
        item_count += crawl_collection(collection)
    
    if opts.write_count:
        with open(opts.item_dir/".count", "w") as fp:
            print(item_count, file=fp)


def crawl_collection(collection):
    lastpage = last_page_for_collection(collection)
    eprint(f"{collection=} {lastpage=}")
    item_count = 0
    for page in range(0, lastpage):
        eprint(f"{collection=} {page=}")
        itempaths = item_paths_for_collection_page(collection, page)
        for itempath in itempaths:
            eprint(f"{collection=} {page=} {itempath=}")
            save_page_for_itempath(itempath)
            item_count += 1
    return item_count


def last_page_for_collection(collection):
    url = f"http://macintoshgarden.org/{collection}/all"
    soup = soup_for_request(Request("GET", url))
    return int(soup.find("li", class_="pager-last").a["href"].split("=")[-1])


def item_paths_for_collection_page(collection, page):
    url = f"http://macintoshgarden.org/{collection}/all?page={page}"
    soup = soup_for_request(Request("GET", url))
    for item in soup.find_all("div", {"class": "game-preview"}):
        # N.B. itempath would seem to include collection, but there are a
        # handful of items that appear to be misfiled. That is, the first
        # component of their path doesn't match their collection. Because of
        # this, we can't strip off the first component, just the leading slash.
        yield item.h2.a["href"].lstrip("/")


def save_page_for_itempath(itempath):
    url = f"http://macintoshgarden.org/{itempath}"
    path = opts.item_dir/f"{itempath}.html"
    assert path.resolve().is_relative_to(opts.item_dir.resolve())
    path.parent.mkdir(parents=True, exist_ok=True)
    save_content_for_request(Request("GET", url), path)


def soup_for_request(request, parser="lxml"):
    response = response_for_request(request)
    return BeautifulSoup(response.content, parser)


def save_content_for_request(request, path):
    response = response_for_request(request, stream=True)
    with open(path, "wb") as fp:
        for chunk in response.iter_content(chunk_size=None):
            fp.write(chunk)


def response_for_request(request, stream=False):
    response = session.send(session.prepare_request(request), stream=stream)
    response.raise_for_status()
    return response


def eprint(*args, file=sys.stderr, **kwargs):
    print(*args, file=file, **kwargs)


if __name__ == "__main__":
    main()
