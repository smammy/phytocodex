mgurl = http://macintoshgarden.org
collections = apps games

curl = curl \
    --proxy 'http://localhost:3128' \
    --user-agent 'Phytocodexbot/1 (sam+phyt@porcupine.club)' \
    --retry 1 \
    --no-progress-meter \
    --write-out '%{stderr}%{url}\t%{filename_effective}\n'

all-item-pages = $(foreach c,$(collections),$(c)-item-pages)
all-lists = $(foreach c,$(collections),$(c)-list)
all-list-pages = $(foreach c,$(collections),$(c)-list-pages)

.DELETE_ON_ERROR:

# ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ #
# parse all item pages and load into database

.PHONY: db
db: db.stamp

db.stamp: $(all-item-pages)
	find $^ -type f | phyt-db-load --go-hard --prune @-
	touch $@

# ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ #
# download the item pages for all items

.PHONY: all-item-pages
all-item-pages: $(all-item-pages)

.PHONY: $(all-item-pages)
$(all-item-pages): %-item-pages: %-item-pages.stamp

%-item-pages.stamp: %-list
	< $< xargs -I{} printf '%s=%s\n' url $(mgurl)/{} output {}.html \
	| $(curl) \
	    --output-dir $(@:%.stamp=%) \
	    --create-dirs \
	    --remove-on-error \
	    --config -
	touch $@

# ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ #
# extract the item paths for all categories' list pages

list: $(all-lists)
	sort --merge $^ > $@

.PHONY: all-lists
all-lists: $(all-lists)

$(all-lists): %-list: %-list-pages.stamp
	find $(<:%.stamp=%) -type f \
	| phyt-extract-paths \
	| sed 's|^/||' \
	| sort \
	> $@

# ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ #
# fetch all pages of each collection's "all" list

.PHONY: all-list-pages
all-list-pages: $(all-list-pages)

.PHONY: $(all-list-pages)
$(all-list-pages): %-list-pages: %-list-pages.stamp

%-list-pages.stamp: %-list-lastpage
	$(curl) \
	    --variable lastpage@$< \
	    --output-dir $(@:%.stamp=%) \
	    --create-dirs \
	    --output '#1.html' \
	    --remove-on-error \
	    --expand-url '$(mgurl)/$(*F)/all?page=[0-{{lastpage:trim}}]'
	touch $@

# ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ #
# determine the index of the last page of each collection

.NOTINTERMEDIATE: *-list-lastpage
%-list-lastpage:
	$(curl) '$(mgurl)/$(*F)/all' | phyt-extract-last-page > $@
	@printf 'Collection “%s” has %s list pages.\n' $(*F) $$(( $$(cat $@) + 1 ))
