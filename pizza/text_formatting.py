def color_format(string, i):
    #return "\033[" + str(i) + "m" + string + "\033[0m"
    return string

def create_func(i):
    def func(string):
        return color_format(string, i)
    return func

bold = create_func(1)
gray = create_func(2)
underline = create_func(4)
strikethrough = create_func(9)
red = create_func(31)
green = create_func(32)
yellow = create_func(33)
blue = create_func(34)
pink = create_func(35)
cyan = create_func(36)
white = create_func(37)
