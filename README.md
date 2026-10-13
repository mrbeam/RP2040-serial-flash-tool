# `serial-flash` - Tool for interacting with Pico bootloaders

This is a command-line tool for uploading code to Raspberry Pi Pico
* [`rp2040_serial_bootloader`](https://github.com/mrbeam/RP2040-serial-bootloader), for upload
  over UART

Generate or refresh the vendored dependencies before building:

```sh
go mod vendor
```

This may download dependencies. Commit `vendor/` after dependency changes so
Yocto can build offline using `-mod=vendor`.

Build it with Go from this checkout. The executable is always named
`serial-flash` when using `make` or the commands below:

```
make
# Equivalent:
go build -mod=vendor -o serial-flash .
```

Install the resulting binary into a directory on your `$PATH`.

Then (assuming your `go` binary install location is on your `$PATH`, see you can
run `serial-flash`:

```
# rp2040_serial_bootloader
serial-flash /dev/ttyUSB0:250000 app.elf

# rp2040_serial_bootloader used on the Raspberry Pi
serial-flash /dev/ttyAMA0:250000 app.elf
```

You can also build it without installing:

```
git clone https://github.com/mrbeam/RP2040-serial-flash-tool.git
cd RP2040-serial-flash-tool
make
```

To build for RPi as target:

```
make raspberrypi3
```

The `raspberrypi3` target selects Linux ARMv7 and produces `serial-flash`.
Plain `make` builds for the host platform. The Yocto recipe uses this target
with its cross compiler and build flags. `GO`, `BUILD_FLAGS`, and `OUTPUT` can
be supplied by the caller.

## Versioning

`make` and `make raspberrypi3` derive the version from Git release tags, using
Python 3's standard library. An exact clean tag reports `v1.0.0`; subsequent
commits report `v1.0.0+1.gabcdef0`, with `.dirty` for tracked local edits.
Without a reachable release tag the version is `v0.0.0+0.g<commit>`. No Git
metadata falls back to `devel`. Query without opening a serial port:

```sh
./serial-flash --version
```

Override for source archives or controlled release builds:

```sh
make raspberrypi3 VERSION=v1.0.0
```

Plain `go build -o serial-flash` reports `devel`. The Yocto recipe embeds
`SERIAL_FLASH_VERSION` through its existing linker flags and preserves those
flags. Its default identifies the pinned `SRCREV`; set `SERIAL_FLASH_VERSION`
to the corresponding release tag when publishing a release. Advance `SRCREV`
to a commit containing these versioning changes before building in Yocto.
