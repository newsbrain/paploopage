.PHONY: build check preview

PORT ?= 4173

build:
	scripts/build.sh

check:
	scripts/check.sh

preview: build
	cd dist && python3 -m http.server $(PORT)
