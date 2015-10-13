import time
import curses
import utils
import textwrap
import text_formatting
import subprocess
import platform

line_count = 1000

def wrap(string, width):
    lines = []
    for section in string.split("\n"):
        lines.extend(textwrap.wrap(section, width))
    return lines

def post_pad(post, network, stdscr):
    lines = []
    width = stdscr.getmaxyx()[1]
    bold = curses.A_BOLD
    norm = curses.A_NORMAL
    #lines.append((" ", norm))
    subject = utils.format_html(post['subject'])
    for line in wrap(subject, width - 2): lines.append((line, bold))
    contents = utils.format_html(post['contents']).replace('___bold_start___', '').replace('___bold_end___', '')
    for line in wrap(contents, width - 2): lines.append((line, norm))
    author = network.get_user_name(post['uid']).encode('ascii', 'ignore') if post['uid'] else 'Anonymous'
    right_author = " "*(width-len(author)-4) + '- ' + author
    lines.append((right_author, norm))
    if post['student_answer']:
        lines.append(("Student Answer:", bold))
        answer = post['student_answer']
        contents = utils.format_html(answer['contents']).replace('___bold_start___', '').replace('___bold_end___', '')
        for line in wrap(contents, width - 2): lines.append((line, norm))
        author = network.get_user_name(answer['uid']).encode('ascii', 'ignore') if answer['uid'] else 'Anonymous'
        right_author = " "*(width-len(author)-4) + '- ' + author
        lines.append((right_author, norm))
    if post['instructor_answer']:
        lines.append(("Instructor Answer:", bold))
        answer = post['instructor_answer']
        contents = utils.format_html(answer['contents']).replace('___bold_start___', '').replace('___bold_end___', '')
        for line in wrap(contents, width - 2): lines.append((line, norm))
        author = network.get_user_name(answer['uid']).encode('ascii', 'ignore') if answer['uid'] else 'Anonymous'
        right_author = " "*(width-len(author)-4) + '- ' + author
        lines.append((right_author, norm))
    if len(post['followups']) > 0:
        lines.append(("Followup Discussions:", bold))
    for followup in post['followups']:
        subject = utils.format_html(followup['subject'])
        hasUID = 'uid' in followup and followup['uid']
        author = network.get_user_name(followup['uid']) if hasUID else 'Anonymous'
        entry = subject + " (" + author.encode('ascii', 'ignore') + ")"
        if followup['plus_ones'] > 0:
            entry += ' +' + str(followup['plus_ones'])
        for line in wrap(entry, width - 2): lines.append((line, norm))
        for reply in followup['children']:
            subject = utils.format_html(reply['subject'])
            hasUID = 'uid' in reply and reply['uid']
            author = network.get_user_name(reply['uid']) if hasUID else 'Anonymous'
            entry = subject + " (" + author.encode('ascii', 'ignore') + ")"
            first = True
            for line in wrap(entry, width - 9): 
                if first:
                    lines.append(("     " + line, norm))
                    first = False
                else:
                    lines.append(("       " + line, norm))
        lines.append(("", norm))
    
    pad = curses.newpad(len(lines) + 1, width)
    for item in lines:
        contents, style = item
        pad.addstr("\n " + contents, style)
    return pad

def render(pad, i, stdscr):
    pad.refresh(i, 0, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1])
    stdscr.refresh()

def view_post(post, network, stdscr):
    processed = utils.process_post(post)
    uid_set = set()
    if ('uid' in processed) and processed['uid']:
        uid_set.add(processed['uid'])
    if ('instructor_answer' in processed) and processed['instructor_answer']:
        inst_ans = processed['instructor_answer']
        if ('uid' in inst_ans) and inst_ans['uid']:
            uid_set.add(inst_ans['uid'])
    if ('student_answer' in processed) and processed['student_answer']:
        stu_ans = processed['student_answer']
        if ('uid' in stu_ans) and stu_ans['uid']:
            uid_set.add(stu_ans['uid'])
    for followup in processed['followups']:
        if ('uid' in followup) and followup['uid']:
            uid_set.add(followup['uid'])
        utils.filter_plus_ones(followup)
        for reply in followup['children']:
            if ('uid' in reply) and reply['uid']:
                uid_set.add(reply['uid'])
    network.get_users(list(uid_set))
    
    pad = post_pad(processed, network, stdscr)
    
    i = 0

    while True:
        #pad = post_pad(processed, network, stdscr, i)
        render(pad, i, stdscr)
        #curses.nonl() # Allows us to read newlines
        #curses.raw() # Characters are passed one by one, no buffering
        c = stdscr.getch()

        # Quit the program
        if c == ord('q') or c == curses.KEY_BACKSPACE:
            break
        
        elif c == ord('i'):
            url = "https://piazza.com/class/" + network._nid + "?cid=" + post['id']
            plat = platform.system()
            if plat == "Windows":
                subprocess.Popen(["explorer", url])
            elif plat == "Darwin":
                subprocess.Popen(["open", url])
            elif plat == "Linux":
                subprocess.Popen(["x-www-browser", url])

        # Scroll down
        elif c == ord('j') or c == curses.KEY_DOWN:
            if i < pad.getmaxyx()[0] - stdscr.getmaxyx()[0]:
                i += 1

        # Scroll up
        elif c == ord('k') or c == curses.KEY_UP:
            if (i > 0):
                i -= 1

        # Check for window resize
        if c == curses.KEY_RESIZE:
            stdscr.erase()
            stdscr.refresh()
            pad = post_pad(processed, network, stdscr)
            