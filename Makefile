.PHONY: all
all:

.PHONY: build
## build: Generate website
build:
	@echo "Rendering..."
	@openring -S webring-in.urls < webring-in.template > layouts/partials/webring-out.html
	@hugo

.PHONY: netlify-build
## netlify-build: Generate website from Netlify build environment
netlify-build:
	-@go get git.sr.ht/~sircmpwn/openring
	-@go install git.sr.ht/~sircmpwn/openring
	-@ls -la $$GOROOT/
	-@/opt/buildhome/cache/.gimme_cache/gopath/bin/openring -S webring-in.urls < webring-in.template > layouts/partials/webring-out.html
	@hugo

.PHONY: serve
## serve: Run development server
serve:
	@echo "Serving..."
	@hugo -D server --bind 0.0.0.0

.PHONY: clean
## clean: Remove generated files
clean:
	@echo "Cleaning..."
	@[ ! -d ./public ] || rm -rf ./public
	@[ ! -d ./resources ] || rm -rf ./resources

.PHONY: help
## help: Print help message
help:
	@echo -e "Usage: \n"
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'
