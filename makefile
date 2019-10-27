ALL_FILES := $(patsubst %.org,%.html,$(wildcard *.org))

all: $(ALL_FILES)

%.html: %.org
	emacs $^ --batch -f org-html-export-to-html --kill
