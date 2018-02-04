all: clean list

testprog.prn:
	ra78k0 -cf0833y testprog.asm

list: testprog.prn
	cat testprog.prn

clean:
	rm -f *.rel *.prn
