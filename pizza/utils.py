import html_parse
import html2text

def format_html(unicode_string):
    h = html2text.HTML2Text()
    h.body_width = 0
    text = h.handle(unicode_string)
    text = text.encode('ascii', 'ignore').strip()
    text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    return text

def filter_plus_ones(followup):
    new_children = []
    plus_ones = 0
    if 'plus_ones' in followup:
        plus_ones = followup['plus_ones']
    for child in followup['children']:
        sub = html_parse.format_unicode_html(child['subject']).replace(" ", "")
        if sub == '+1' or sub == '<p>+1</p>':
            plus_ones += 1
        else:
            new_children.append(child)
    followup['children'] = new_children
    followup['plus_ones'] = plus_ones
    return plus_ones
    
def process_post(post):
    data = {
        'id': post['id'],
        'type': post['type'],
        'folders': post['folders'],
        'pinned': 'pin' in post['tags'],
        'uid': None if 'uid' not in post['history'][0] else post['history'][0]['uid'],
        'subject': post['history'][0]['subject'],
        'contents': post['history'][0]['content']
    }
    data['student_answer'] = None
    data['instructor_answer'] = None
    if data['type'] == 'question':
        followups = []
        for child in post['children']:
            if child['type'] == 'i_answer':
                data['instructor_answer'] = {
                    'raw': child,
                    'contents': child['history'][0]['content'],
                    'uid': None if 'uid' not in child['history'][0] else child['history'][0]['uid']
                }
            elif child['type'] == 's_answer':
                data['student_answer'] = {
                    'raw': child,
                    'contents': child['history'][0]['content'],
                    'uid': None if 'uid' not in child['history'][0] else child['history'][0]['uid']
                }
            else:
                followups.append(child)
        data['followups'] = followups
    else:
        data['followups'] = post['children']
    return data