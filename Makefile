.PHONY: all clean test openring serve build

all:

serve:
	hugo serve

test:
	hugo version

build:
	hugo --gc --minify

clean:
	rm -rf ./public/
