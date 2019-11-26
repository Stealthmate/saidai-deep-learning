NOTEBOOKS := $(patsubst notebooks/%,_%,$(patsubst %.ipynb,%.md,$(wildcard notebooks/**/*.ipynb)))

serve:
	bundle exec jekyll serve --host=0.0.0.0 --destination docs_local

$(NOTEBOOKS): _%.md: notebooks/%.ipynb
	jupyter nbconvert $< --to markdown --output-dir _$(dir $*)
	sed -i -s 's/\.ipynb)/\.html)/g' $@
	python excluded/trunclines.py $@
	# sed -s 'H;1h;$!d;x; s/\n\n\n*/\n/g' $@.sed > $@
	# mv $@.sed $@
	# mv $@.sed $@

build: clean $(NOTEBOOKS)
	bundle exec jekyll build

clean:
	rm -rf $(NOTEBOOKS) $(patsubst %.md,%_files,$(NOTEBOOKS))
