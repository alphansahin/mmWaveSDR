from math import ceil, log

### int -> list ###
def int2intlist(x, intmax=256, num_ints=0):
    """Convert x (integer) into list of integers.
    The size of each integer in the list can optionally be controlled
    by intmax so that the integer range is 0 to intmax-1 (default: 0-255).
    Number integers in the list can optionally be controlled by parameter num_ints,
    where num_ints=0 (default) means minimum number of integers required.
    """
    vals = []
    temp = x
    if (num_ints == 0):
        if (x != 0):
            num_ints=int(ceil(log(x,intmax)))
        else:
            num_ints = 1
    for i in range(num_ints-1,-1,-1):
        vals.append(int(temp//intmax**i))
        temp=temp%intmax**i
    return vals

### list -> int ###
def intlist2int(intlist):
    """Convert list of integers (range: 0 - intmax-1) to integer."""
    return int.from_bytes(intlist,'big', signed=False)

def fhex(data, size):
    """Return a sized hex-string of value"""
    return '0x{:0{}X}'.format(data,size)