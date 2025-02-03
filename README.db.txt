I. INITIAL SETUP

Create a PostgreSQL database accessible to the user that will be running
Phytocodex. This is how you do it on Debian-derived OSes:

    sudo -u postgres createdb -O sam phytocodex

Load the schema:

    psql -f schema.sql phytocodex

II. RUNNING THE CRAWLER

    phyt-db-crawl apps games

III. LOADING ITEMS INTO THE DATABASE

    find items -type f -name '*.html' \
    | phyt-db-load --stat-list-size (cat items/.count) --go-hard --prune @-
