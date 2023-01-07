
from collections import Counter
import re

def remove_extra_lines(s:str):
    # Alternatively: os.linesep.join([line for line in s.splitlines() if line])
    return re.sub('\n+', '\n', s)

def remove_email_extra(s:str):
    s = remove_extra_lines(s)
    return s.replace("=20", "").replace('"3D', "").replace("=\n", "")

def remove_email_content_id(s:str, repl="<ID>"):
    return re.sub(r"(?<================)[0-9]+(?===)", repl, s)

def remove_email_message_id(s:str, repl="<message_id>"):
    return re.sub(r"(?<=Message-ID: <).+?(?=>)", repl, s)

def remove_date(s:str, repl="<date>"):
    regex = r'(?<=Date: )[A-Za-z]{3}, [0-9]{2} [A-Za-z]{3} [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}( [+-][0-9]{4})?'
    return re.sub(regex, repl, s)

def prune_generated_headers(s:str):
    transformers = (
        remove_email_content_id,
        remove_email_message_id,
        remove_date
    )
    for transf in transformers:
        s = transf(s)
    return s

def payloads_to_dict(*parts):
    data = {}
    for part in parts:

        payload = part.get_payload()
        key = part.get_content_type()
        if key in data:
            new_key = key
            n = 0
            while new_key in data:
                n += 1
                new_key = key + f"_{n}"
            key = new_key
        if isinstance(payload, str):
            data[key] = payload
        elif payload is None:
            # Most likely empty message
            pass
        else:
            data[key] = payloads_to_dict(*payload)
    return data