NOTEBOOKS := $(patsubst notebooks/%,_%,$(patsubst %.ipynb,%.md,$(wildcard notebooks/**/*.ipynb)))

$(NOTEBOOKS): _%.md: notebooks/%.ipynb
	jupyter nbconvert $< --to markdown --output-dir _$(dir $*)
	sed -i -s 's/\.ipynb)/\.html)/g' $@

all: $(NOTEBOOKS)

clean:
	rm -rf $(NOTEBOOKS) $(patsubst %.md,%_files,$(NOTEBOOKS))
