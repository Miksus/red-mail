
import re

def remove_extra_lines(s:str):
    # Alternatively: os.linesep.join([line for line in s.splitlines() if line])
    return re.sub('\n+', '\n', s)