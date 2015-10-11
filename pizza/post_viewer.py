import time
import curses
import html_parse
import utils
import textwrap
import text_formatting

def post_pad(post, network, stdscr, i):
    lines = []
    width = stdscr.getmaxyx()[1]
    bold = curses.A_BOLD
    norm = curses.A_NORMAL
    subject = html_parse.format_unicode_html(post['subject'])
    for line in textwrap.wrap(subject, width - 2): lines.append((line, bold))
    contents = html_parse.format_unicode_html(post['contents']).replace('___bold_start___', '').replace('___bold_end___', '')
    for line in textwrap.wrap(contents, width - 2): lines.append((line, norm))
    author = network.get_user_name(post['uid']).encode('ascii', 'ignore') if post['uid'] else 'Anonymous'
    right_author = " "*(width-len(author)-4) + '- ' + author
    lines.append((right_author, norm))
    if post['student_answer']:
        lines.append(("Student Answer:", bold))
        answer = post['student_answer']
        contents = html_parse.format_unicode_html(answer['contents']).replace('___bold_start___', '').replace('___bold_end___', '')
        for line in textwrap.wrap(contents, width - 2): lines.append((line, norm))
        author = network.get_user_name(answer['uid']).encode('ascii', 'ignore') if answer['uid'] else 'Anonymous'
        right_author = " "*(width-len(author)-4) + '- ' + author
        lines.append((right_author, norm))
    if post['instructor_answer']:
        lines.append(("Instructor Answer:", bold))
        answer = post['instructor_answer']
        contents = html_parse.format_unicode_html(answer['contents']).replace('___bold_start___', '').replace('___bold_end___', '')
        for line in textwrap.wrap(contents, width - 2): lines.append((line, norm))
        author = network.get_user_name(answer['uid']).encode('ascii', 'ignore') if answer['uid'] else 'Anonymous'
        right_author = " "*(width-len(author)-4) + '- ' + author
        lines.append((right_author, norm))
    if len(post['followups']) > 0:
        lines.append(("Followup Discussions:", bold))
    for followup in post['followups']:
        subject = html_parse.format_unicode_html(followup['subject'])
        hasUID = 'uid' in followup and followup['uid']
        author = network.get_user_name(followup['uid']) if hasUID else 'Anonymous'
        entry = subject + " (" + author.encode('ascii', 'ignore') + ")"
        if followup['plus_ones'] > 0:
            entry += ' +' + str(followup['plus_ones'])
        for line in textwrap.wrap(entry, width - 2): lines.append((line, norm))
        for reply in followup['children']:
            subject = html_parse.format_unicode_html(reply['subject'])
            hasUID = 'uid' in reply and reply['uid']
            author = network.get_user_name(reply['uid']) if hasUID else 'Anonymous'
            entry = subject + " (" + author.encode('ascii', 'ignore') + ")"
            first = True
            for line in textwrap.wrap(entry, width - 6): 
                if first:
                    lines.append(("   " + line, norm))
                    first = False
                else:
                    lines.append(("    " + line, norm))
        lines.append(("", norm))
    
    pad = curses.newpad(min(len(lines) + 2, stdscr.getmaxyx()[0]), width)
    pad.addstr("\n")
    counter = 2
    for index in range(i, len(lines)):
        contents, style = lines[index]
        pad.addstr(" " + contents + "\n", style)
        counter += 1
        if counter >= stdscr.getmaxyx()[0]:
            return pad
    return pad

def render(pad, i, stdscr):
    pad.refresh(0, 0, 0, 0, stdscr.getmaxyx()[0], pad.getmaxyx()[1])
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
    
    pad = post_pad(processed, network, stdscr, 0)
    
    i = 0
    
    render(pad, i, stdscr)
    
    while True:
        #curses.nonl() # Allows us to read newlines
        #curses.raw() # Characters are passed one by one, no buffering
        c = stdscr.getch()

        # Quit the program
        if c == ord('q') or c == curses.KEY_BACKSPACE:
            break

        # Scroll down
        elif c == ord('j') or c == curses.KEY_DOWN:
            i += 1
            #if i >= len(pad):
            #    i = len(pads) - 1
            pad = post_pad(processed, network, stdscr, i)
            stdscr.erase()
            stdscr.refresh()
            render(pad, i, stdscr)

        # Scroll up
        elif c == ord('k') or c == curses.KEY_UP:
            i -= 1
            if(i < 0):
                i = 0
            pad = post_pad(processed, network, stdscr, i)
            stdscr.erase()
            stdscr.refresh()
            render(pad, i, stdscr)

        # Check for window resize
        if c == curses.KEY_RESIZE:
            pad = post_pad(processed, network, stdscr, i)
            stdscr.erase()
            stdscr.refresh()
            render(pad, i, stdscr)