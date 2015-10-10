from piazza_api import Piazza

import sys, getopt
import argparse
import pickle 
import os 
import getpass

class InputError(Exception): 

    def __init__(self, msg): 
        self.msg = msg

    def __str__(self):
        return self.msg

class QueryObj: 

    def add_query(self, query):
        self.query = ''.join(query)

    def add_tags(self, list_of_tags):
        if (list_of_tags is not None): 
            self.tags = list_of_tags

    def add_time_range(self, range_list): 
        if (range_list is not None):
            self.tr_range = range(int(range_list[0]), int(range_list[1]))

    def bool_pinned(self, pinned): 
        if (pinned is not None):
            self.pinned = pinned 

    def bool_inst_notes(self, inst): 
        if (inst is not None): 
            self.inst_notes = inst

    def __repr__(self): 
        return "Query: " + self.query + "\n List_of_tags: " + str(self.tags) + "\n Time Range " + repr(self.tr_range) + "\n Pinned: " + str(self.pinned) + "\n Inst notes: " + str(self.inst_notes)





def main():

    parser = argparse.ArgumentParser(description='Process user input for piazza queries')
    parser.add_argument('-q', '--query', nargs="+")
    parser.add_argument('-t', '--tags', nargs="+") 
    parser.add_argument('-r', '--range', nargs=2)
    parser.add_argument('-i', '--instructor-only', action='store_true')
    parser.add_argument('-p', '--posts', action='store_true')
    parser.add_argument('-l', '--force-login', action='store_true')
    args = parser.parse_args()

    if (args.query is None): 
        raise(InputError("Query not given!"))

    queryObj = QueryObj()
    queryObj.add_query(args.query)
    queryObj.add_tags(args.tags)
    queryObj.add_time_range(args.range)
    queryObj.bool_inst_notes(args.instructor_only)
    queryObj.bool_pinned(args.posts)

    loginfile = os.path.expanduser("~") + "/.pizza"
    
    if not args.force_login: 
        try: 
            pkl = pickle.load(open(loginfile,"rb"))
            data = {'email': pkl['email'], 'password': pkl['password'].decode('rot13')}
        except IOError:
            email = raw_input('Piazza Email: ')
            password = getpass.getpass()
            data = {'email': email, 'password': password}
            pkl = {'email': email, 'password': password.encode('rot13')}
            pickle.dump(pkl, open(loginfile, "wb"))

    piazza = Piazza() 
    piazza.user_login(data['email'], data['password'])
    user_status = piazza.get_user_status()
    
    classes = user_status['networks']
    classes = sorted(classes, key=lambda k: k['status'])
    # list classes 
    print("Choose a Class")
    counter = 1
    for c in classes: 
        info = c['name']
        if c['status'] == 'inactive':
            info = '(inactive) ' + info
        print '{0:2d}: {1:s}'.format(counter, info)
        counter = counter + 1


if __name__ == '__main__':
    main()

