CREATE TABLE dbmeta (
    id integer PRIMARY KEY DEFAULT 0 CHECK (id = 0),
    generation integer NOT NULL DEFAULT 0,
    lastupdate timestamp with time zone NOT NULL DEFAULT '1904-01-01T00:00:00',
    list_size integer NOT NULL DEFAULT 0,
    items_crawled integer NOT NULL DEFAULT 0
);

INSERT INTO dbmeta DEFAULT VALUES;

CREATE FUNCTION generation() RETURNS integer AS $$
    SELECT generation FROM dbmeta;
$$ LANGUAGE SQL;

CREATE TABLE item (
    generation integer NOT NULL DEFAULT generation(),
    path text PRIMARY KEY,
    name text NOT NULL,
    year integer,
    descr_html text,
    descr_text text,
    compat_notes text,
    document tsvector GENERATED ALWAYS AS (
        setweight(to_tsvector('english', path), 'A')
        || setweight(to_tsvector('english', name), 'A')
        || setweight(to_tsvector('english', coalesce(year::text, '')), 'A')
        || setweight(to_tsvector('english', coalesce(descr_html, '')), 'B')
        || setweight(to_tsvector('english', coalesce(compat_notes, '')), 'D')
    ) STORED
);

CREATE INDEX ON item USING gin (document);

CREATE TABLE category (
    generation integer NOT NULL DEFAULT generation(),
    path text PRIMARY KEY,
    name text NOT NULL,
    document tsvector GENERATED ALWAYS AS (
        to_tsvector('english', path || ' ' || name)
    ) STORED
);

CREATE INDEX ON category USING gin (document);

CREATE TABLE item_category (
    generation integer NOT NULL DEFAULT generation(),
    item_path text NOT NULL REFERENCES item,
    category_path text NOT NULL  REFERENCES category,
    UNIQUE (item_path, category_path)
);

CREATE TABLE author (
    generation integer NOT NULL DEFAULT generation(),
    path text PRIMARY KEY,
    name text NOT NULL,
    document tsvector GENERATED ALWAYS AS (
        to_tsvector('english', path || ' ' || name)
    ) STORED
);

CREATE INDEX ON author USING gin (document);

CREATE TABLE item_author (
    generation integer NOT NULL DEFAULT generation(),
    item_path text NOT NULL REFERENCES item,
    author_path text NOT NULL REFERENCES author,
    UNIQUE (item_path, author_path)
);

CREATE TABLE item_publisher (
    generation integer NOT NULL DEFAULT generation(),
    item_path text NOT NULL REFERENCES item,
    author_path text NOT NULL REFERENCES author,
    UNIQUE (item_path, author_path)
);

CREATE TYPE sysver AS ENUM ('1-5', '6', '7', '8-8.1', '8.5-8.6', '9', 'X');

CREATE TABLE item_sysver (
    generation integer NOT NULL DEFAULT generation(),
    item_path text NOT NULL REFERENCES item,
    sysver sysver NOT NULL,
    UNIQUE (item_path, sysver)
);

CREATE TABLE download (
    generation integer NOT NULL DEFAULT generation(),
    item_path text NOT NULL REFERENCES item,
    number integer NOT NULL,
    name text NOT NULL,
    size text NOT NULL,
    md5 text,
    UNIQUE (item_path, number),
    document tsvector GENERATED ALWAYS AS (
        to_tsvector('english', name || md5)
    ) STORED
);

CREATE INDEX ON download USING gin (document);
