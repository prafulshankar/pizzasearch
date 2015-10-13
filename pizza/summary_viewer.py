import curses
import time
import textwrap
import text_formatting
import post_viewer
import utils
import subprocess
import platform

at_bottom = False
last_index = -1

def render(all_pads, index, stdscr):
    global at_bottom, last_index
    index = max(0, index - 1)
    if at_bottom and index >= last_index:
        index = last_index
    pads = all_pads[index:]
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
    at_bottom = i == len(pads)
    last_index = index
    if i < len(pads):
        pads[i].refresh(0, 0, pad_y, pad_x,
                    min(pad_y + pads[i].getmaxyx()[0], window_height - 1),
                    pad_x + pads[i].getmaxyx()[1])
    elif pad_y < window_height:
        pad = curses.newpad(window_height, window_width)
        pad.refresh(0, 0, pad_y, pad_x, window_height - 1, window_width - 1)
        
    stdscr.refresh()

def summary_pad(subject, contents, stdscr, reverse=False):
    contents = contents.replace('___bold_start___', '').replace('___bold_end___', '') + '...'
    width = stdscr.getmaxyx()[1]
    subject_lines = textwrap.wrap(subject, width - 2)
    lines = textwrap.wrap(contents, width - 2)
    height = len(subject_lines) + len(lines) + 2
    pad = curses.newpad(height, width)
    pad.bkgd(' ', curses.A_REVERSE if reverse else curses.A_NORMAL)
    pad.addstr("\n")
    bold_val = curses.A_BOLD
    norm_val = curses.A_NORMAL
    if reverse:
        bold_val = bold_val | curses.A_REVERSE
        norm_val = norm_val | curses.A_REVERSE
    for line in subject_lines:
        pad.addstr(" " + line + "\n", bold_val)
    for line in lines:
        pad.addstr(" " + line + "\n", norm_val)
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

def remake_pads(summaries, stdscr, index):
    new_pads = []
    for i in range(0, len(summaries)):
        subject = utils.format_html(summaries[i]['subject'])
        contents = utils.format_html(summaries[i]['content_snipet'])
        reverse = i == index
        new_pads.append(summary_pad(subject, contents, stdscr, reverse))
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

data = []

def view_summaries(stdscr, feed, network):
    curses.use_default_colors()
    
    pads = []
    summaries = []
    global data
    data = []
    unsaved_post = None
    height_sum = 0
    window_height = stdscr.getmaxyx()[0]
    window_width = stdscr.getmaxyx()[1]
    while True:
        post = feed.next_post()
        if not post:
            break
        subject = utils.format_html(post['subject'])
        contents = utils.format_html(post['content_snipet'])
        subject_lines = textwrap.wrap(subject, window_width - 2)
        lines = textwrap.wrap(contents, window_width - 2)
        height = len(subject_lines) + len(lines) + 2
        if height_sum + height <= window_height*2:
            summaries.append(post)
            data.append((subject, contents))
            height_sum += height
            pads.append(summary_pad(subject, contents, stdscr))
        else:
            unsaved_post = post
            break
    # Main loop
    i = 0
    stdscr.erase()
    stdscr.refresh()
    if len(pads) > 0:
        pads[i] = summary_pad(data[i][0], data[i][1], stdscr, True)
    stdscr.nodelay(False) # getch is non-blocking
    render(pads, i, stdscr)
    while True:
        c = stdscr.getch()

        # Quit the program
        if c == ord('q') or c == curses.KEY_BACKSPACE:
            break
        
        elif c == ord('i'):
            url = "https://piazza.com/class/" + network._nid + "?cid=" + summaries[i]['id']
            plat = platform.system()
            if plat == "Windows":
                subprocess.Popen(["explorer", url])
            elif plat == "Darwin":
                subprocess.Popen(["open", url])
            elif plat == "Linux":
                subprocess.Popen(["x-www-browser", url])

        # Check for ENTER
        elif c == ord('\n'):
            stdscr.clear()
            stdscr.refresh()
            post_summary_obj = summaries[i]
            id_num = post_summary_obj['id']
            post_obj = network.get_post(id_num)
            post_viewer.view_post(post_obj, network, stdscr)
            pads = remake_pads(summaries, stdscr, i)

        # Scroll down
        elif c == ord('j') or c == curses.KEY_DOWN:
            post = unsaved_post if unsaved_post else feed.next_post()
            unsaved_post = None
            if post:
                subject = utils.format_html(post['subject'])
                contents = utils.format_html(post['content_snipet'])
                summaries.append(post)
                data.append((subject, contents))
                pads.append(summary_pad(subject, contents, stdscr))
            if i < len(pads) - 1:
                pads[i] = summary_pad(data[i][0], data[i][1], stdscr)
                i += 1
                pads[i] = summary_pad(data[i][0], data[i][1], stdscr, True)

        # Scroll up
        elif (c == ord('k') or c == curses.KEY_UP) and i > 0:
            pads[i] = summary_pad(data[i][0], data[i][1], stdscr)
            i -= 1
            pads[i] = summary_pad(data[i][0], data[i][1], stdscr, True)

        # Check for window resize
        if c == curses.KEY_RESIZE:
            stdscr.erase()
            stdscr.refresh()
            pads = remake_pads(summaries, stdscr, i)
            
        render(pads, i, stdscr)
