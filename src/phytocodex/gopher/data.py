logo=r"""
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

logo2=r"""
   .-.                                                .
  (_) )-.      /              /                      /    `--.  .-.
     /   \    /-. .    .-.---/---.-._..-.  .-._..-../   .-.   \/
    /     )  /   | )  /     /   (   )(    (   )(   /  ./.-'_  /\
 .-/  `--'_.'    |(_.'     /     `-'  `---'`-'  `-'-..(__.'.-'  `-.
(_/             ..-._)
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

The download links use the unofficial "GET /" selector to directly
link to the Macintosh Garden via HTTP. Old Gopher clients, including
TurboGopher for System 6, don't understand this syntax: you'll have to
use Fetch to connect to the Macintosh Garden FTP site, and find the
file manually.

(I am hoping to find a better solution for download linking. I don't
want to proxy downloads, but it may come to that!)

Please send feedback to sam+phyt@porcupine.club. Thanks!
"""[1:-1],
)
