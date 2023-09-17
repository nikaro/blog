.PHONY: all clean test openring serve build

all:

openring:
	openring -S ./config/openring/feeds.txt < ./config/openring/layout.html > ./layouts/partials/webring.html

serve: openring
	hugo serve

test:
	hugo version

build: openring
	hugo --gc --minify

clean:
	rm -rf ./public/