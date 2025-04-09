import re

Allias = ["I", "F", "P", "A", "T", "U", "L", "O", "S", "E"]

def toList(devices):
    list_ = devices[4:].split(",")
    error = []

    for x in list_:
        if len(x) < 4:
            error.append(x)

    for x in error:
        try:
            list_.remove(x)
        except:
            pass
    return list_

def is_valid_ipv4(ip):
    pattern = r"^(25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])\." \
              r"(25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])\." \
              r"(25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])\." \
              r"(25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])$"
    
    return bool(re.match(pattern, ip))

def isIP(ip):
    tok = ip.strip()

    if tok.count(" ") == 3:
        toks = tok.split(" ")
        for toke in toks:
            if len(toke) > 3:  # Fixed incorrect method call
                return False
        
        temp = tok
        for c in temp.replace(" ",""):
            if not (c in Allias):
                return False
        return True

    return False

def toCali(ip):
    result = ""

    for c in ip:
        if c == ".":
            result += " "
        else:
            result += Allias[int(c)]
    return result

def toIP(cali):
    result = ""
    cal = cali.strip()

    for c in cal:
        if c == " ":
            result += "."
        else:
            result += str(Allias.index(c))
    return result
