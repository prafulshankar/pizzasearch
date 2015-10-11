import time
import curses
import html_parse
def view_post(post, network, stdscr):
    # Termination
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()

    # For now output to the root window
    # but eventually output to a large pad
    out = stdscr

    #stdscr.clear()
    question_body = post['history'][0]['content']
    question_body = html_parse.format_unicode_html(question_body)
    views = post['unique_views']
    view = int(views)

#    updates = post['change_log']
#    user_ids = [update['uid'] for update in updates]
#    users = network.get_users(user_ids)

    #print("users = ", users) # Why does this print None?!
    followups = post['children']

    followup_strings = []
    for followup in followups:
        followup_string = ""
        replies = followup['children']
        if(not 'subject' in followup): # Answer to original post
            if(followup['type'] == 's_answer'):
                followup_string += "Student answer\n"
                followup_string += "==============\n"
            else:
                followup_string += "Instructor answer\n"
                followup_string += "=================\n"
            followup_string += html_parse.format_unicode_html(
                                followup['history'][0]['content'])
        else:
            followup_string += html_parse.format_unicode_html(
                                        followup['subject']) + "\n"
        followup_strings.append(followup_string)

    for followup_string in followup_strings:
        print(followup_string)

    time.sleep(500)
