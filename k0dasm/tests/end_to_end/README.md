# End-to-End tests

Running `make` will:

 - Assemble the test program with `as78k0`
 - Disassemble that binary with `k0dasm`
 - Assemble the disassembly with `as78k0`
 - Verify that the two binaries are identical

These programs must be installed and in `$PATH`:
 - `as78k0`
 - `srec_cat`
 - `k0dasm`
