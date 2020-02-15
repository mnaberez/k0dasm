k0dasm
======

Overview
--------

k0dasm is a disassembler for NEC 78K0 binaries that generates output compatible with the `as78k0 <http://shop-pdp.net/ashtml/as78k0.htm>`_ assembler.  It can be used to disassemble firmware for many 8-bit NEC 78K0 microcontrollers.  Note that NEC has several microcontroller families with similar names, such as 78K0S, that use different instruction sets.  These are not supported.

k0dasm was developed to disassemble the firmware of the `Volkswagen Premium V <https://github.com/mnaberez/vwradio>`_ car radios made by Delco.  These radios use the undocumented NEC µPD78F0831Y microcontroller, which is similar to the `µPD78F0833Y <https://web.archive.org/web/20180328161019/https://www.renesas.com/en-us/doc/DocumentServer/021/U13892EJ2V0UM00.pdf>`_.  A companion program, `k0emu <https://github.com/mnaberez/k0emu>`_, is a 78K0 emulator developed for the same project.

Features
--------

- Identical Reassembly.  The assembly language output of k0dasm will assemble to a bit-for-bit exact copy of the original binary using as78k0.  This has been tested using several real firmware binaries.

- Code / Data Separation.  Starting from the vectors at the bottom of memory, k0dasm uses recursive traversal disassembly to separate code from data.  This automates much of the disassembly process but indirect jumps (``br ax``) will still need to be resolved manually.

- Symbol Generation.  k0dasm tries not to write hardcoded addresses in the output when possible.  It will automatically add symbols for hardware registers and vectors, other memory locations used, and will add labels for branches and subroutines.

Installation
------------

k0dasm is written in Python and requires Python 3.4 or later.  Packages are `available <https://pypi.org/project/k0dasm/>`_ on the Python Package Index (PyPI).  You can download them from there or you can use ``pip`` to automatically install or upgrade ``k0dasm``::

    $ pip install -U k0dasm

Usage
-----

k0dasm accepts a plain binary file as input::

    $ k0dasm input.bin > output.asm

The file is assumed to be a ROM image that should be aligned to the bottom of memory.  For example, if a 32K file is given, k0dasm will assume the image should be located at 0x0000-0x7FFF.  After loading the image, the disassembler reads the vectors and starts tracing instructions from their targets.

Author
------

`Mike Naberezny <https://github.com/mnaberez>`_
