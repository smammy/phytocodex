mgurl = http://macintoshgarden.org
collections = apps games

curl = curl \
    --proxy 'http://localhost:3128' \
    --user-agent 'Phytocodexbot/1 (sam+phyt@porcupine.club)' \
    --retry 1 \
    --no-progress-meter

#     \
#    --write-out '%{stderr}%{url}\t%{filename_effective}\n'

.DELETE_ON_ERROR:
.NOTINTERMEDIATE: $(collections:%=pagecache/list/%.last)

# ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ #
# parse all item pages and load into database

.PHONY: db
db: db.stamp

db.stamp: pagecache/item/item.stamp
	find pagecache/item -type f | phyt-db-load --go-hard --prune @-
	touch $@

# ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ #
# download all item pages

pagecache/item/.stamp: list
	< $< xargs -I{} printf '%s=%s\n' url $(mgurl)/{} output {}.html \
	| $(curl) \
	    --output-dir $(@D) \
	    --create-dirs \
	    --remove-on-error \
	    --config -
	touch $@

# ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ #
# extract the item paths from all categories' list pages

list: $(collections:%=pagecache/list/%.listpages)
	find $(^:%.listpages=%) -type f \
	| phyt-extract-paths \
	| sed 's|^/||' \
	| sort \
	> $@

# ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ #
# fetch all pages of a collection's item list

%.listpages: %.lastpage
	$(curl) \
	    --variable lastpage@$< \
	    --output-dir $* \
	    --create-dirs \
	    --output '#1.html' \
	    --remove-on-error \
	    --expand-url '$(mgurl)/$(*F)/all?page=[0-{{lastpage:trim}}]'
	touch $@

# ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ #
# determine the index of the last page of each collection

%.lastpage:
	mkdir -p $(@D)
	$(curl) '$(mgurl)/$(*F)/all' | phyt-extract-last-page > $@
	@printf 'Collection “%s” has %s list pages.\n' $(*F) $$(( $$(cat $@) + 1 ))
