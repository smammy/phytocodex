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

ftpserver = r"""
  Host:     repo1.macintoshgarden.org
  Path:     /Garden/
  Login:    macgarden
  Password: publicdl
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

The download links use the unofficial "GET /" selector to directly
link to the Macintosh Garden via HTTP. Some Gopher clients understand
this syntax, and some don't. TurboGopher for System 6 is one that
doesn't: you'll have to use Fetch to connect to the Macintosh Garden
FTP site, and find the file manually.

Some known issues are:

  * Character encoding for non-ASCII characters is messed up in some
    situations. You may see odd glyphs.

  * There's no "selector not found" handler, so if you request a
    nonexistent selector, you'll see a blank screen or the screen
    won't change, depending on your client.

  * The search result ranking function could be better.

Future work:

  * Match search terms against an item's categories, authors,
    publishers, and download file names. Add syntax for searching a
    particular field.

  * Figure out a way to deliver a download seamlessly on TurboGopher
    on System 6 (without proxying downloads through Phytocodex), or at
    least find some way that doesn't require manually pawing through
    the FTP site.

  * Show the date and time the index was last updated from the Garden.
    Automate updates. (Maybe read the "recent changes" page to detect
    new items, but what about edits to existing items?)

Please send feedback to sam+phyt@porcupine.club. Thanks!
"""[1:-1],
)
