import html_parse

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
        'pinned': 'pin' in post['tags']
    }
    if data['type'] == 'question':
        data['student_answer'] = None
        data['instructor_answer'] = None
        followups = []
        for child in post['children']:
            if child['type'] == 'i_answer':
                data['instructor_answer'] = {
                    'raw': child,
                    'contents': child['history'][0]['contents'],
                    'uid': child['history'][0]['uid']
                }
            elif child['type'] == 's_answer':
                data['student_answer'] = {
                    'raw': child,
                    'contents': child['history'][0]['contents'],
                    'uid': child['history'][0]['uid']
                }
            else:
                followups.append(child)
    else:
        data['followups'] = post['children']
    return data