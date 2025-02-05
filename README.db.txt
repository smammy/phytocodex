Create a PostgreSQL database accessible to the user that will be
running Phytocodex. This is how you do it on Debian-derived OSes:

    sudo -u postgres createdb -O sam phytocodex

Load the schema:

    psql -f schema.sql phytocodex

Run the crawler:

    phyt-db-crawl apps games

This will create an "items" directory in the current directory. (As
of this writing, this requires 328 MiB free on disk.)

Then feed the list of fetched items to the loader:

    find items -type f -name '*.html' \
    | phyt-db-load \
        --stat-list-size (cat items/.count) \
        --go-hard \
        --prune \
        @-

You can remove the "items" directory after the loader finishes.
