all: clean testprog.bin list

testprog.bin: testprog.hex
	srec_cat testprog.hex -intel -o testprog.bin -binary

testprog.hex: testprog.lmf
	oc78k0 testprog.lmf

testprog.lmf: testprog.prn
	lk78k0 testprog.rel

testprog.prn:
	ra78k0 -cf0831y testprog.asm

list: testprog.prn
	cat testprog.prn

clean:
	rm -f *.bin *.hex *.lmf *.map *.prn *.rel *.sym
