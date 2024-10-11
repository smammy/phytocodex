import os

HOST = os.environ.get("PHYT_HOST", "home.munkynet.org")
PORT = os.environ.get("PHYT_PORT", "70")

MGURL = os.environ.get("PHYT_MGURL", "http://macintoshgarden.org/")
PGURL = os.environ.get("PHYT_PGURL", "postgresql://:5433/phytocodex")

LOGLEVEL = os.environ.get("PHYT_LOGLEVEL", "DEBUG")
