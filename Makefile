.PHONY: all
all:

.PHONY: build
## build: Generate website
build:
	@echo "Rendering..."
	@hugo

.PHONY: simplecss
## simplecss: Update CSS file
simplecss:
	@curl -Lo assets/main.css https://raw.githubusercontent.com/kevquirk/simple.css/main/simple.min.css

.PHONY: serve
## serve: Run development server
serve:
	@echo "Serving..."
	@hugo -D server --bind 0.0.0.0

.PHONY: clean
## clean: Remove generated files
clean:
	@echo "Cleaning..."
	@rm -rf ./public
	@rm -rf ./resources

.PHONY: help
## help: Print help message
help:
	@echo -e "Usage: \n"
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'
