#!/usr/bin/env python3

from pathlib import Path
from socketserver import StreamRequestHandler
import logging
import re

import psycopg

from .data import logo, logo2, ftpserver, stats, textfiles
from .menuentity import GopherEntity as Ent
from ..config import PGURL


class GopherHandler(StreamRequestHandler):
    def handle(self):
        self.cur = psycopg.connect(
            PGURL, row_factory=psycopg.rows.namedtuple_row
        ).cursor()
        
        reqbytes = self.rfile.readline()
        logging.debug(f"recv: “{self.nicebytes(reqbytes)}”")
        reqfields = reqbytes.rstrip().split(b"\t")
        match reqfields:
            case [selector, stuff]:
                query = stuff.decode("iso-8859-1")
            case [selector]:
                query = None
        selector = selector.decode("ascii")
        logging.debug(f"selector: “{selector}”")
        parts = [x for x in selector.split('/') if x != ""]
        logging.debug(f"parts: “{parts}”")
        assert all(re.fullmatch(r"[-.0-9A-Z_a-z]+", part) for part in parts)
        match parts:
            case []:
                self.browse_root()
            case [filename] if filename.endswith(".txt"):
                self.show_textfile(filename.removesuffix(".txt"))
            case ["category", *rest]:
                self.browse_categories(rest)
            case [("author"|"publisher") as atype]:
                self.browse_authors(atype)
            case [("author"|"publisher") as atype, asuffix]:
                self.browse_by_author(atype, asuffix)
            case [("apps"|"games") as coll, item] if item.endswith(".md5"):
                self.show_checksums(coll, item.removesuffix(".md5"))
            case [("apps"|"games") as coll, item, *extra]:
                self.browse_item(coll, item, extra)
            case ["search"]:
                self.search(query)
            case ["stats"]:
                self.show_stats()
            case [*_]:
                self.not_found()
    
    def browse_root(self):
        self.writemenu([
            Ent.title("Phytocodex: your guide to the Macintosh Garden"),
            *[Ent.info(line) for line in logo2.splitlines()],
            Ent.text("About Phytocodex", "/about.txt"),
            Ent.menu("Categories", "/category"),
            Ent.menu("Authors", "/author"),
            Ent.menu("Publishers", "/publisher"),
            Ent.search("Search", "/search"),
            Ent.text("Crawler & Database Statistics", "/stats"),
            Ent.url_link(
                "Macintosh Garden on the WWW",
                "http://macintoshgarden.org/",
            ),
            Ent.url_link(
                "Macintosh Garden FTP server",
                "ftp://macgarden:publicdl@repo1.macintoshgarden.org/Garden/",
            ),
            *[Ent.info(line) for line in ftpserver.splitlines()],
        ])
    
    def show_textfile(self, textfile):
        if textfile in textfiles:
            self.writetext(textfiles[textfile])
        else:
            self.writetext("Not found.")
    
    def browse_categories(self, parts):
        if not parts:
            self.writemenu([
                Ent.menu("Apps", "/category/apps"),
                Ent.menu("Games", "/category/games"),
            ])
            return
        
        catpath = "".join(f"/{part}" for part in parts)
        catpattern = f"{catpath}/[^/]+"
        
        self.cur.execute("""
            (
                SELECT
                    1 AS sortorder, '1' AS itemtype,
                    CASE
                        WHEN %(depth)s > 1 THEN 'Subcategory: '
                        ELSE 'Category: '
                    END || name AS username,
                    '/category' || path AS selector
                FROM category
                WHERE path SIMILAR TO %(catpattern)s
            ) UNION (
                SELECT
                    2 AS sortorder,
                    '1' AS itemtype,
                    name AS username,
                    path AS selector
                FROM item AS i
                JOIN item_category AS ic ON i.path=ic.item_path
                WHERE ic.category_path=%(catpath)s
            ) ORDER BY sortorder, username;
        """, dict(depth=len(parts), catpattern=catpattern, catpath=catpath))
        
        for rec in self.cur:
            self.writeent(Ent(rec.itemtype, rec.username, rec.selector))
        self.writeend()
    
    def browse_authors(self, atype):
        self.cur.execute(f"""
            SELECT
                a.name AS username,
                replace(a.path, '/author/', '/' || %(atype)s || '/') AS selector
            FROM author AS a
            JOIN item_{atype} AS ix ON a.path=ix.author_path
            GROUP BY a.path
            ORDER BY a.name;
        """, dict(atype=atype))
        
        for rec in self.cur:
            self.writeent(Ent.menu(rec.username, rec.selector))
        self.writeend()
    
    def browse_by_author(self, atype, asuffix):
        path = f"/author/{asuffix}"
        self.cur.execute(f"""
            SELECT i.name AS username, i.path AS selector
            FROM item AS i
            JOIN item_{atype} AS ix ON i.path=ix.item_path
            WHERE ix.author_path=%(path)s
        """, dict(path=path))
        
        for rec in self.cur:
            self.writeent(Ent.menu(rec.username, rec.selector))
        self.writeend()
    
    def browse_item(self, collection, item, extra):
        path = f"/{collection}/{item}"
        item = self.cur.execute(
            "SELECT path, name, year, descr_text FROM item WHERE path=%(path)s",
            dict(path=path),
        ).fetchone()
        
        match extra:
            case []:
                self.writeinfo(item)
            case ["about.txt"]:
                self.writetext(item.descr_text)
            case ["downloads"]:
                self.writedownloads(item)
            case ["downloads", other] if other.endswith(".md5"):
                self.writemd5file(item, other.removesuffix(".md5"))
    
    def search(self, query):
        self.cur.execute("""
            SELECT path, name
            FROM item, websearch_to_tsquery(%(query)s) AS query
            WHERE document @@ query
            ORDER BY ts_rank_cd(document, query, 2) DESC
            LIMIT 100;
        """, dict(query=query))
        
        for hit in self.cur:
            self.writeent(Ent.menu(hit.name, hit.path))
        self.writeend()
    
    def writeinfo(self, item):
        self.writemenu([
            Ent.text(f"About {item.name}", f"{item.path}/about.txt"),
            Ent.menu(f"{item.name} Downloads", f"{item.path}/downloads"),
            Ent.text(f"{item.name} Checksums", f"{item.path}.md5"),
            Ent.url_link(
                f"WWW Page for {item.name}",
                f"http://macintoshgarden.org/{item.path}",
            ),
        ])
    
    def writetext(self, text):
        for line in text.splitlines():
            line = line.rstrip()
            line = ".." if line == "." else line
            self.wfile.write(line.encode("iso-8859-1", errors="replace"))
            self.wfile.write(b"\r\n")
        self.wfile.write(b".\r\n")
    
    def writedownloads(self, item):
        self.cur.execute("""
            SELECT number, name, size, md5
            FROM download WHERE item_path=%(path)s
        """, dict(path=item.path))
        
        for dl in self.cur:
            dldir = item.path.split('/')[1]
            self.writeent(Ent.binary(
                f"DL#{dl.number} {dl.name} ({dl.size})",
                f"GET /sites/macintoshgarden.org/files/{dldir}/{dl.name}",
                "macintoshgarden.org", "80",
            ))
            self.writeend()
    
    def show_checksums(self, collection, item):
        path = f"/{collection}/{item}"
        self.cur.execute("""
            SELECT number, name, size, md5
            FROM download WHERE item_path=%(path)s
        """, dict(path=path))
        
        for dl in self.cur:
            self.wfile.write(b"".join([
                dl.md5.encode("ascii"), b"  ",
                dl.name.encode("ascii"), b"\r\n",
            ]))
        self.wfile.write(b".\r\n")
    
    def show_stats(self):
        dbmeta = self.cur.execute("""
            SELECT list_size, items_crawled, generation, lastupdate FROM dbmeta
        """).fetchone()
        
        counts = self.cur.execute("""
            SELECT
                (SELECT count(*) FROM item) AS item,
                (SELECT count(*) FROM category) AS category,
                (SELECT count(DISTINCT author_path) FROM item_author) AS author,
                (SELECT count(DISTINCT author_path) FROM item_publisher) AS publisher,
                (SELECT count(*) FROM download) AS download
        """).fetchone()
        
        self.writetext(stats.format(dbmeta=dbmeta, counts=counts))

    def writeent(self, entity):
        self.wfile.write(bytes(entity))
    
    def writeend(self):
        self.wfile.write(b".\r\n")
    
    def writemenu(self, entities):
        for entity in entities:
            self.writeent(entity)
        self.writeend()
    
    @staticmethod
    def nicebytes(bstr):
        return "".join(
            f"{b:c}" if 0x20 <= b <= 0x7F else f"<{b:02X}>" for b in bstr
        )
