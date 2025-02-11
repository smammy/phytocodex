logo = r"""
.-------. .---.  .---.   ____     __ ,---------.    ,-----.
\  _(`)_ \|   |  |_ _|   \   \   /  /\          \ .'  .-,  '.
| (_ o._)||   |  ( ' )    \  _. /  '  `--.  ,---'/ ,-.|  \ _ \
|  (_,_) /|   '-(_{;}_)    _( )_ .'      |   \  ;  \  '_ /  | :
|   '-.-' |      (_,_) ___(_ o _)'       :_ _:  |  _`,/ \ _/  |
|   |     | _ _--.   ||   |(_,_)'        (_I_)  : (  '\_/ \   ;
|   |     |( ' ) |   ||   `-'  /        (_(=)_)  \ `"/  \  ) /
/   )     (_{;}_)|   | \      /          (_I_)    '. \_/``".'
`---'     '(_,_) '---'  `-..-'           '---'      '-----'
    _______      ,-----.     ______         .-''-.   _____     __
   /   __  \   .'  .-,  '.  |    _ `''.   .'_ _   \  \   _\   /  /
  | ,_/  \__) / ,-.|  \ _ \ | _ | ) _  \ / ( ` )   ' .-./ ). /  '
,-./  )      ;  \  '_ /  | :|( ''_'  ) |. (_ o _)  | \ '_ .') .'
\  '_ '`)    |  _`,/ \ _/  || . (_) `. ||  (_,_)___|(_ (_) _) '
 > (_)  )  __: (  '\_/ \   ;|(_    ._) ''  \   .---.  /    \   \
(  .  .-'_/  )\ `"/  \  ) / |  (_.\.' /  \  `-'    /  `-'`-'    \
 `-'`-'     /  '. \_/``".'  |       .'    \       /  /  /   \    \
   `._____.'     '-----'    '-----'`       `'-..-'  '--'     '----'
"""[1:-1]

logo2 = r"""
   .-.                                                .
  (_) )-.      /              /                      /    `--.  .-.
     /   \    /-. .    .-.---/---.-._..-.  .-._..-../   .-.   \/
    /     )  /   | )  /     /   (   )(    (   )(   /  ./.-'_  /\
 .-/  `--'_.'    |(_.'     /     `-'  `---'`-'  `-'-..(__.'.-'  `-.
(_/             ..-._)
"""[1:-1]

stats = r"""
Crawler Stats
-------------
Items found   : {dbmeta.list_size}
Items crawled : {dbmeta.items_crawled}

Database Stats
--------------
Generation    : {dbmeta.generation}
Last update   : {dbmeta.lastupdate}
Items         : {counts.item}
Categories    : {counts.category}
Authors       : {counts.author}
Publishers    : {counts.publisher}
Downloads     : {counts.download}
"""[1:-1]

textfiles = dict(
    about=r"""
Phytocodex is an independent index of the apps and games in the
Macintosh Garden, provided as a Gopher server. The index is updated
periodically, but not particularly frequently.

You can access Phytocodex on vintage Macs, running system software as
old as System 6, using a Gopher client like TurboGopher. I've also
tested it with Lynx on Linux, Lagrange on modern macOS, OverbiteNX on
Firefox, and the Floodgap Systems gopher proxy.

The search function accepts pretty normal "web search" syntax: quoted
text, "OR", and "-" are recognized. Your query is matched against the
path, name, year and description of each item in the garden. At most
100 results are returned.

There are two sets of download links for every item: the first set use
the unofficial "GET /" selector to directly link to the Garden via
HTTP. Some Gopher clients understand this syntax, and some don't.
Unfortunately, TurboGopher for System 6 is one that doesn't.

The second set of download links uses a local HTTP-to-Gopher proxy to
deliver files over the Gopher protocol. This should work with any
Gopher client that supports the 

The download links use the unofficial "GET /" selector to directly
link to the Macintosh Garden via HTTP. Some Gopher clients understand
this syntax, and some don't. TurboGopher for System 6 is one that
doesn't: you'll have to use Fetch to connect to the Macintosh Garden
FTP site, and find the file manually.

Please send feedback to sam+phyt@porcupine.club. Thanks!

Known Issues

  * Character encoding for non-ASCII characters is messed up in some
    situations. You may see odd glyphs.

  * The search result ranking function could be better.

Future Work

  * Match search terms against an item's categories, authors,
    publishers, and download file names. Add syntax for searching a
    particular field.

  * Figure out a way to deliver a download seamlessly on TurboGopher
    on System 6 without proxying downloads through Phytocodex. Or at
    least find some way that doesn't require manually pawing through
    the FTP site.

  * Automate updates.

History

v1.1, 2024-02-04

  * Added download proxy for Gopher clients that don't support
    "GET /" pseudo-selectors for HTTP.
  * Rewrote the crawler as a Python script rather than a big ball of
    fighting animals held together with a makefile.
  * Added a handler for nonexistent selectors.
  * Fixed a bug that prevented display of all but the first download
    for an item.

"""[1:-1],
    ftpserver=r"""
Host:     repo1.macintoshgarden.org
Path:     /Garden/
Login:    macgarden
Password: publicdl

Connect using any normal FTP client. Note that downloads for all items
in each collection (apps, games) are in a single directory. Those
directories are quite large (tens of thousands of files) and an old
Mac may choke on the listings. It might help to use a client that
allows you to enter the path to a file directly, to save the
aggravation of loading the directory listing.
"""[1:-1]
)
