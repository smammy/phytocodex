from urllib.parse import urlparse
import os
import unicodedata

from ..config import HOST, PORT


class GopherEntity:
    def __init__(self, itemtype, username, selector="-", host=HOST, port=PORT):
        self.itemtype = itemtype
        self.username = username
        self.selector = selector
        self.host = host
        self.port = port
    
    @classmethod
    def text(cls, *args, **kwargs):
        return cls("0", *args, **kwargs)
    
    @classmethod
    def menu(cls, *args, **kwargs):
        return cls("1", *args, **kwargs)
    
    @classmethod
    def search(cls, *args, **kwargs):
        return cls("7", *args, **kwargs)
    
    @classmethod
    def binary(cls, *args, **kwargs):
        return cls("9", *args, **kwargs)
    
    @classmethod
    def getslash_link(cls, username, url):
        url = urlparse(url)
        assert url.scheme == "http"
        assert not any([url.params, url.query, url.fragment])
        path = url.path if url.path else "/"
        port = url.port if url.port else "80"
        return cls("h", username, f"GET {path}", url.hostname, port)
    
    @classmethod
    def url_link(cls, username, url):
        return cls("h", username, f"URL:{url}")
    
    @classmethod
    def info(cls, username):
        return cls("i", username)
    
    @classmethod
    def title(cls, username):
        return cls("i", username, "TITLE")
    
    def __bytes__(self):
        return b"".join([
            self.itemtype.encode("ascii"),
            b"\t".join([
                unicodedata.normalize("NFKC", self.username)
                    .encode("iso-8859-1", errors="replace"),
                self.selector.encode("ascii"),
                self.host.encode("ascii"),
                self.port.encode("ascii"),
            ]),
            b"\r\n",
        ])
