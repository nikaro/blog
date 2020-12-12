.PHONY: all
all:

.PHONY: setup
## setup: Install required tools
setup:
	@echo "Installing..."
	@command -v netlify || npm install --global netlify-cli
	@command -v pelican || pip install --requirement requirements.txt

.PHONY: build
## build: Generate using production settings
build:
	@echo "Rendering..."
	@pelican ./content -o ./output -s ./publishconf.py -t ./themes/etchy

.PHONY: serve
## serve: Serve content on port 8000
serve:
	@echo "Serving at http://localhost:8000/"
	@pelican -l ./content -o ./output -s ./pelicanconf.py -t ./themes/etchy -b 0.0.0.0

.PHONY: deploy
## deploy: Deploy to Netlify
deploy:
	@echo "Uploading..."
	@netlify deploy --dir=output --prod --build

.PHONY: clean
## clean: Remove generated files
clean:
	@[ ! -d ./output ] || rm -rf ./output

.PHONY: help
## help: Print help message
help:
	@echo -e "Usage: \n"
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'
