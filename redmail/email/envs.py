
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

def get_span(l:list, loc:int, width=None) -> int:
    "Get span of each value in index/column"
    def get_value(item):
        val = item[:width+1] if width is not None else item
        return val

    prev = get_value(l[loc-1])
    curr = get_value(l[loc])
    if len(l) == 1:
        # Index/column of size 1
        span = 1
    elif prev == curr:
        # Previous value is the same as current
        # --> hide (span=0)
        # The previous should have span>=2
        span = 0
    else:
        span = 1
        for nxt in l[loc+1:]:
            if get_value(nxt) != curr:
                break
            span += 1
    return span

def is_last_group_row(n, index:list, level=None):
    "Check if iteration is the last of the group"
    curr = index[n]
    if not isinstance(curr, tuple):
        return False
    elif n == (index.shape[0] - 1):
        # Last of the whole frame
        return True
    
    n += 1
    next = index[n]

    if level == 0:
        return True
    elif level is None:
        return curr[0] != next[0]
    

    while curr[:level+1] == next[:level+1]:
        # fast forward to the span of the level
        try:
            next = index[n+1]
            n += 1
        except IndexError:
            # End of the dataframe
            return True
    
    # ie. ("blue", "car"), ("green", "car") --> True
    # ("blue", "car"), ("blue", "red") --> False
    return curr[0] != next[0]
