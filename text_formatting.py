def color_format(string, i):
    return "\033[" + str(i) + "m" + string + "\033[0m"

def red(string):
    return color_format(string, 31)

def green(string):
    return color_format(string, 32)

def yellow(string):
    return color_format(string, 33)

def blue(string):
    return color_format(string, 34)

def pink(string):
    return color_format(string, 35)

def cyan(string):
    return color_format(string, 36)

def white(string):
    return color_format(string, 37)
