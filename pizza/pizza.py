from piazza_api2 import Piazza

import sys, getopt
import argparse
import pickle
import os
import getpass
import curses
from feed_processor import FeedProcessor
from requests.packages import urllib3
import utils
import summary_viewer


class InputError(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class QueryObj:

    def add_query(self, query):
        if query is None:
            self.query = None
        else:
            self.query = ''.join(query)

    def add_tag(self, tag):
        self.tag = tag

    def add_time_range(self, range_list):
        if (range_list is not None):
            self.tr_range = range(int(range_list[0]), int(range_list[1]))
        else:
            self.tr_range = None

    def bool_pinned(self, pinned):
        self.pinned = pinned

    def bool_inst_notes(self, inst):
        self.inst_notes = inst

    def bool_following(self, follow):
        self.following = follow

    def __repr__(self):
        return "Query: " + self.query + "\n List_of_tags: " + str(self.tags) + "\n Time Range " + repr(self.tr_range) + "\n Pinned: " + str(self.pinned) + "\n Inst notes: " + str(self.inst_notes)

def main():
    urllib3.disable_warnings()
    parser = argparse.ArgumentParser(description='Process user input for piazza queries')
    parser.add_argument('-q', '--query', nargs="+")
    parser.add_argument('-t', '--tag', nargs=1)
    #parser.add_argument('-r', '--range', nargs=2)
    parser.add_argument('-i', '--instructor-only', action='store_true')
    parser.add_argument('-p', '--pinned', action='store_true')
    parser.add_argument('-f', '--following', action='store_true')
    parser.add_argument('-l', '--force-login', action='store_true')
    args = parser.parse_args()

    queryObj = QueryObj()
    queryObj.add_query(args.query)
    queryObj.add_tag(args.tag)
    #queryObj.add_time_range(args.range)
    queryObj.bool_inst_notes(args.instructor_only)
    queryObj.bool_pinned(args.pinned)
    queryObj.bool_following(args.following)

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


    index = raw_input('Class Number: ')
    network = piazza.network(classes[int(index) - 1]['id'])
    feed_processor = FeedProcessor(network, queryObj)
    curses.wrapper(summary_viewer.view_summaries, feed_processor, network)


if __name__ == '__main__':
    main()
