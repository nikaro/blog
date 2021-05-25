.PHONY: all
all:

.PHONY: build
## build: Generate website
build:
	@echo "Rendering..."
	@openring -S webring-in.urls < webring-in.template > layouts/partials/webring-out.html
	@hugo
	@mkdir -p public/feeds
	@cp -f public/index.xml public/feeds/all.atom.xml
	@tar -C public -cvz . > site.tar.gz

.PHONY: serve
## serve: Run development server
serve:
	@echo "Serving..."
	@hugo -D server

.PHONY: deploy
## deploy: Deploy to SourceHut
deploy:
	@echo "Uploading..."
	@curl --oauth2-bearer "${ACCESS_TOKEN}" -F content=@site.tar.gz https://pages.sr.ht/publish/blog2.karolak.fr

.PHONY: clean
## clean: Remove generated files
clean:
	@echo "Cleaning..."
	@[ ! -d ./public ] || rm -rf ./public
	@[ ! -d ./resources ] || rm -rf ./resources
	@[ ! -f ./site.tar.gz ] || rm -rf ./site.tar.gz

.PHONY: help
## help: Print help message
help:
	@echo -e "Usage: \n"
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'
