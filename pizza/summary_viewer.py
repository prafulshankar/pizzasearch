import curses
import time
import textwrap
import text_formatting

import html_parse

def render(pads, stdscr):
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

def summary_pad(subject, contents, stdscr):
    width = stdscr.getmaxyx()[1]
    subject_lines = textwrap.wrap(subject, width - 2)
    lines = textwrap.wrap(contents, width - 2)
    height = len(subject_lines) + len(lines) + 2

    pad = curses.newpad(height, width)
    pad.addstr("\n")
    for line in subject_lines:
        pad.addstr(" " + line + "\n", curses.A_BOLD)
    for line in lines:
        pad.addstr(" " + line + "\n")
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
    
def remake_pads(summaries, stdscr):
    new_pads = []
    for i in range(0, len(summaries)):
        subject = html_parse.format_unicode_html(summaries[i]['subject'])
        contents = html_parse.format_unicode_html(summaries[i]['content_snipet'])
        new_pads.append(summary_pad(subject, contents, stdscr))
    return new_pads
    

# Shift a window up or down (down is positive)
def shift(pad, offset, stdscr):
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
    
def view_summaries(feed):
    stdscr = curses.initscr()
    curses.start_color()
    curses.use_default_colors()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    
    # Create a sub-window
    pads = []
    summaries = []
    unsaved_post = None
    height_sum = 0
    window_height = stdscr.getmaxyx()[0]
    window_width = stdscr.getmaxyx()[1]
    while True:
        post = feed.next_post()
        if not post:
            break
        subject = html_parse.format_unicode_html(post['subject'])
        contents = html_parse.format_unicode_html(post['content_snipet'])
        subject_lines = textwrap.wrap(subject, window_width - 2)
        lines = textwrap.wrap(contents, window_width - 2)
        height = len(subject_lines) + len(lines) + 2
        if height_sum + height <= window_height*2:
            summaries.append(post)
            height_sum += height
            pads.append(summary_pad(subject, contents, stdscr))
        else:
            unsaved_post = post
            break
    # Main loop
    i = 0
    stdscr.erase()
    stdscr.refresh()
    pads[0].bkgd(' ', curses.A_REVERSE)
    render(pads, stdscr)
    stdscr.nodelay(1) # getch is non-blocking
    c = 'j'
    while True:
        c = stdscr.getch()
    
        # Quit the program
        if c == ord('q'):
            break
    
        # Scroll down
        elif c == ord('j') or c == curses.KEY_DOWN:
            post = unsaved_post if unsaved_post else feed.next_post()
            unsaved_post = None
            if post:
                subject = html_parse.format_unicode_html(post['subject'])
                contents = html_parse.format_unicode_html(post['content_snipet'])
                summaries.append(post)
                pads.append(summary_pad(subject, contents, stdscr))
            pads[i].bkgd(' ', curses.A_NORMAL)
            i += 1
            if i >= len(pads):
                i = len(pads) - 1
            stdscr.erase()
            stdscr.refresh()
            pads[i].bkgd(' ', curses.A_REVERSE)
            render(pads[i:], stdscr)
    
        # Scroll up
        elif c == ord('k') or c == curses.KEY_UP:
            pads[i].bkgd(' ', curses.A_NORMAL)
            i -= 1
            if(i < 0):
                i = 0
            stdscr.erase()
            stdscr.refresh()
            pads[i].bkgd(' ', curses.A_REVERSE)
            render(pads[i:], stdscr)
    
        # Check for window resize
        if c == curses.KEY_RESIZE:
            stdscr.erase()
            stdscr.refresh()
            pads = remake_pads(summaries, stdscr)
            render(pads[i:], stdscr)
    
    # Termination
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()