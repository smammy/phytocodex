mgurl = http://macintoshgarden.org
collections = apps games

curl = curl \
    --proxy 'http://localhost:3128' \
    --user-agent 'Phytocodexbot/1 (sam+phyt@porcupine.club)' \
    --retry 1 \
    --silent
#    --no-progress-meter
#    --write-out '%{stderr}%{url}\t%{filename_effective}\n'

.DELETE_ON_ERROR:
.NOTINTERMEDIATE: $(collections:%=pagecache/list/%.lastpage)

# ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ #
# parse all item pages and load into database

.PHONY: db
db: db.stamp

db.stamp: item.count pagecache/item/.stamp
	find pagecache/item -type f -name '*.html' \
	| phyt-db-load \
	    --stat-list-size $(file < $<) \
	    --go-hard \
	    --prune \
	    @-
	touch $@

# ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ #
# download all item pages

.PHONY: items
items: pagecache/item/.stamp

items.d: item.list
	xargs -a $< -d '\n' -r \
	    printf "pagecache/item/.stamp: pagecache/item/%s.html\n" > $@

include items.d

pagecache/item/.stamp:
	touch $@

pagecache/item/%.html:
	@printf "Fetching %s ..." $*
	@$(curl) \
	    --output-dir $(@D) \
	    --create-dirs \
	    --output $(@F) \
	    --remove-on-error \
	    --url $(mgurl)/$*
	@printf " ✓\n"

# ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ #
# extract the item paths from all categories' list pages

.PHONY: list
list: item.list

item.list item.count &: $(collections:%=pagecache/list/%.listpages)
	find $(^:%.listpages=%) -type f \
	| phyt-extract-paths \
	| sed 's|^/||' \
	| sort -u \
	| tee item.list \
	| wc -l \
	> item.count

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
