all: clean compare

compare: testprog.bin reassembled.bin
	diff testprog.bin reassembled.bin

clean:
	rm -f *.bin *.hlr *.ihx *.lst *.rel
	rm -f reassembled.asm

testprog.bin:
	as78k0 -l -o testprog.asm
	aslink -i testprog
	srec_cat testprog.hex -intel -o testprog.bin -binary

reassembled.bin: testprog.bin
	k0dasm testprog.bin > reassembled.asm
	as78k0 -l -o reassembled.asm
	aslink -i reassembled
	srec_cat reassembled.hex -intel -o reassembled.bin -binary
