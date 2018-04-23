
def intel_byte(num):
    '''Format an 8-bit number in Intel hexadecimal notation: 0xAB -> 0ABh'''
    return _intel_num(num, width=2)

def intel_word(num):
    '''Format a 16-bit number in Intel hexadecimal notation: 0xABCD -> 0ABCDh'''
    return _intel_num(num, width=4)

def _intel_num(num, width=2):
    fmt = "%0" + str(width) + "x"
    ihex = (fmt % num) + "h"
    if not ihex[0].isdigit():
        ihex = "0" + ihex
    return ihex
