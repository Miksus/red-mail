
import re

def remove_extra_lines(s:str):
    # Alternatively: os.linesep.join([line for line in s.splitlines() if line])
    return re.sub('\n+', '\n', s)

def remove_email_extra(s:str):
    s = remove_extra_lines(s)
    return s.replace("=20", "").replace('"3D', "").replace("=\n", "")