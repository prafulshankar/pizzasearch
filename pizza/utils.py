import html_parse

def filter_plus_ones(followup):
    new_children = []
    plus_ones = 0
    if 'plus_ones' in followup:
        plus_ones = followup['plus_ones']
    for child in followup['children']:
        sub = html_parse.format_unicde_html(child['subject']).replace(" ", "")
        if sub == '+1' or sub == '<p>+1</p>':
            plus_ones += 1
        else:
            new_children.append(child)
    followup['children'] = new_children
    followup['plus_ones'] = plus_ones
    return plus_ones