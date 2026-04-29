# k0dasm

## Overview

k0dasm is a disassembler for Renesas (NEC) 78K0 binaries that generates output compatible with the [as78k0](http://shop-pdp.net/ashtml/as78k0.htm) assembler.  It can be used to disassemble firmware for many 8-bit microcontrollers in the 78K0 family.  Note that Renesas has several microcontroller families with similar names, such as 78K0S and 78K0R, that use incompatible instruction sets.  Those other families are not supported by this disassembler.

Originally developed to disassemble firmware for the NEC µPD78F0831Y (an undocumented subset of the [µPD78F0833Y](https://web.archive.org/web/20180328161019if_/https://www.renesas.com/en-us/doc/DocumentServer/021/U13892EJ2V0UM00.pdf)), k0dasm has some baked-in assumptions, such as the vector addresses, that will need to be modified to disassemble code for another MCU. k0dasm was also designed for a single address space, since its target MCU only has one. Supporting multiple flash banks would require extensive changes that are not planned, but adapting k0dasm to other 78K0 MCUs with a flat memory map should be straightforward.

## Features

- Identical Reassembly.  The assembly language output of k0dasm will assemble to a bit-for-bit exact copy of the original binary using [as78k0](http://shop-pdp.net/ashtml/as78k0.htm).  This has been tested using several real firmware binaries.

- Code / Data Separation.  Starting from the vectors at the bottom of memory, k0dasm uses recursive traversal disassembly to separate code from data.  This automates much of the disassembly process but indirect jumps (`br ax`) will still need to be resolved manually.

- Symbol Generation.  k0dasm tries not to write hardcoded addresses in the output when possible.  It will automatically add symbols for hardware registers and vectors, other memory locations used, and will add labels for branches and subroutines.

## Installation

k0dasm is written in Python and requires Python 3.8 or later.  Packages are [available](https://pypi.org/project/k0dasm/) on the Python Package Index (PyPI).  You can download them from there or you can use `pip` to install `k0dasm`:

    $ pip install k0dasm

## Usage

k0dasm accepts a plain binary file as input:

    $ k0dasm input.bin > output.asm

The file is assumed to be a ROM image that should be aligned to the bottom of memory.  For example, if a 32K file is given, k0dasm will assume the image should be located at 0x0000-0x7FFF.  After loading the image, the disassembler reads the vectors and starts tracing instructions from their targets.

For times when static analysis falls short, a companion program, [k0emu](https://github.com/mnaberez/k0emu), is available to run 78K0 binaries under emulation. Both k0dasm and k0emu were developed for the [vwradio](https://github.com/mnaberez/vwradio) project.

## Author

[Mike Naberezny](https://github.com/mnaberez)
