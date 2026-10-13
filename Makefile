GO ?= go
GOFLAGS ?= -mod=vendor
BUILD_FLAGS ?= $(GOFLAGS)
OUTPUT ?= serial-flash
PYTHON ?= python3
VERSION ?= $(shell $(PYTHON) tools/git_version.py)
# Yocto supplies its own combined linker flags and overrides this to empty.
VERSION_FLAGS ?= -ldflags="-X main.version=$(VERSION)"

.PHONY: all build raspberrypi3
all: build

build:
	$(GO) build $(BUILD_FLAGS) $(VERSION_FLAGS) -o $(OUTPUT) .

raspberrypi3: export GOOS = linux
raspberrypi3: export GOARCH = arm
raspberrypi3: export GOARM = 7
raspberrypi3: export CGO_ENABLED = 0
raspberrypi3: build
