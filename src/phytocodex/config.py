import os

HOST = os.environ.get("PHYT_HOST", "phytocodex.porcupine.club")
PORT = os.environ.get("PHYT_PORT", "70")

MGURL = os.environ.get("PHYT_MGURL", "http://macintoshgarden.org/")
PGURL = os.environ.get("PHYT_PGURL", "postgresql://:5433/phytocodex")

LOGLEVEL = os.environ.get("PHYT_LOGLEVEL", "INFO")
