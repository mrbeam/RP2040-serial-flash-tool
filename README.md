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
cd serial-flash
go get -v .
go build .
```

To build for RPi as target:

```
env GOOS=linux GOARCH=arm go build .
```
