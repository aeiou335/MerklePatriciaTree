def raw_to_hex(string):
    assert isinstance(string, str), "Input must be string!"
    _hex = []
    for s in string:
        _hex += divmod(ord(s), 16)
    return _hex

def hex_to_raw(hexarray):
    assert len(hexarray) % 2 == 0
    result = ""
    for i in range(0, len(hexarray), 2):
        result += chr(16 * hexarray[i] + hexarray[i + 1])

    return result

def hex_to_hp(hexarray):
    #print(hexarray)
    assert isinstance(hexarray, list), "Input must be list!"
    
    
    if hexarray[-1] == 16:
        term = 1
        hexarray = hexarray[:-1]
    else:
        term = 0
    oddlen = len(hexarray) % 2
    flag = 2*term+oddlen
    
    if not oddlen:
        hexarray = [flag, 0] + hexarray
    else:
        hexarray = [flag] + hexarray
    result = ''
    #print(hexarray)
    for i in range(0, len(hexarray), 2):
        result += chr(16 * hexarray[i] + hexarray[i + 1])
    return result

def hp_to_hex(nib):

    res = raw_to_hex(nib)
    flag = res[0]
    if flag & 2:
        res.append(16)
    if flag & 1:
        res = res[1:]
    else:
        res = res[2:]

    return res
    
def terminator(nib, has_terminator):
    assert isinstance(nib, list), "Input must be list!"
    if has_terminator:
        nib.append(16)
    else:
        #print(nib)
        if nib[-1] == 16:
            del nib[-1]
    return nib

