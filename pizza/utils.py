def filter_plus_ones(followup):
    new_children = []
    plus_ones = 0
    for child in followup['children']:
        if child['subject'] == '+1' or child['subject'] == '<p>+1</p>':
            plus_ones += 1
        else:
            new_children.append(child)
    followup['children'] = new_children
    followup['plus_ones'] = plus_ones
    return plus_ones