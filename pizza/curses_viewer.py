import curses
import time
import textwrap
import text_formatting

def render(pads):
    window_nums = stdscr.getmaxyx()
    window_height = window_nums[0]
    window_width = window_nums[1]
    pad_y = 0
    pad_x = 0
    i = 0
    while(i < len(pads) and
          pad_y + pads[i].getmaxyx()[0] < window_height):
        pads[i].refresh(0, 0, pad_y, pad_x,
                        pad_y + pads[i].getmaxyx()[0],
                        pad_x + pads[i].getmaxyx()[1])
        pad_y = pad_y + pads[i].getmaxyx()[0]
        i += 1
    stdscr.refresh()

def wrapped_pad(string):
    width = stdscr.getmaxyx()[1]
    lines = textwrap.wrap(string, width - 2)
    height = len(lines) + 2

    pad = curses.newpad(height, width)
    pad.addstr("\n")
    for line in lines:
        pad.addstr(" " + line + "\n", curses.color_pair(1))
    pad.border()
    return pad

def pad_refresh(pad):
    pos = pad.getbegyx();
    size = pad.getmaxyx();

    y1 = pos[0]
    x1 = pos[1]
    y2 = y1 + size[0]
    x2 = x1 + size[1]

    pad.refresh(0, 0, y1, x1, y2, x2)

# Shift a window up or down (down is positive)
def shift(pad, offset):
    pos = pad.getbegyx()
    curr_y = pos[0]
    curr_x = pos[1]
    new_y = curr_y + offset
    stdscr.erase()
    stdscr.refresh()
    mvpad(pad, new_y, curr_x)

def mvpad(pad, new_y1, new_x1):
    size = pad.getmaxyx()
    new_y2 = stdscr.getmaxyx()[0]
    new_x2 = stdscr.getmaxyx()[1]
    pad.refresh(0, 0, new_y1, new_x1, new_y2, new_x2)

# Initialization
stdscr = curses.initscr()
curses.start_color()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)

curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
stdscr.addstr(0, 0, "This is dim text\n",
              curses.A_DIM)
stdscr.addstr("This is regular text\n")
stdscr.addstr("The size of the window is " + str(stdscr.getmaxyx()))
stdscr.refresh()

# Create a sub-window
eyre = []
eyre.append("There was no possibility of taking a walk that day.  We had been wandering, indeed, in the leafless shrubbery an hour in the morning; but since dinner (Mrs. Reed, when there was no company, dined early) the cold winter wind had brought with it clouds so sombre, and a rain so penetrating, that further out-door exercise was now out of the question.")
eyre.append("I was glad of it: I never liked long walks, especially on chilly afternoons: dreadful to me was the coming home in the raw twilight, with nipped fingers and toes, and a heart saddened by the chidings of Bessie, the nurse, and humbled by the consciousness of my physical inferiority to Eliza, John, and Georgiana Reed.")
eyre.append("The said Eliza, John, and Georgiana were now clustered round their mama in the drawing-room: she lay reclined on a sofa by the fireside, and with her darlings about her (for the time neither quarrelling nor crying) looked perfectly happy.")
eyre.append("This is a stupid ")
eyre.append("\"What does Bessie say I have done?\" I asked.")
pads = [wrapped_pad(passage) for passage in eyre]

# Main loop
i = 0
pads[0].bkgd(' ', curses.A_REVERSE)
render(pads)
stdscr.nodelay(1) # getch is non-blocking
c = 'j'
while(1):
    c = stdscr.getch()

    # Quit the program
    if c == ord('q'):
        break

    # Scroll down
    elif c == ord('j') or c == curses.KEY_DOWN:
        pads[i].bkgd(' ', curses.A_NORMAL)
        i += 1
        if i >= len(pads):
            i = len(pads) - 1
        stdscr.erase()
        stdscr.refresh()
        pads[i].bkgd(' ', curses.A_REVERSE)
        render(pads[i:])

    # Scroll up
    elif c == ord('k') or c == curses.KEY_UP:
        pads[i].bkgd(' ', curses.A_NORMAL)
        i -= 1
        if(i < 0):
            i = 0
        stdscr.erase()
        stdscr.refresh()
        pads[i].bkgd(' ', curses.A_REVERSE)
        render(pads[i:])

    # Check for window resize
    if c == curses.KEY_RESIZE:
        stdscr.erase()
        stdscr.refresh()
        render(pads[i:])

# Termination
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
