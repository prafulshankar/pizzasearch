from piazza_api2 import Piazza
from piazza_api2.network import FollowingFilter, FolderFilter

class FeedProcessor:
    
    def __init__(self, network, query): 
        self.network = network
        self.query = query
        self.posts = []
        self.feed = None
        self.feed_index = -1
        self.offset = 0
        self.complete = False
    
    def __getitem__(self, arg):
        while arg >= len(self.posts):
            self.get_post()
            
        return self.posts[arg]
        
    def next_post(self):
        if not self.feed or self.feed_index >= len(self.feed):
            if self.complete:
                return None
            else:
                self.load_feed()
            
        while True:
            if not self.feed:
                return None
            if self.feed_index == -1 or self.feed_index >= len(self.feed):
                return None
            post = self.feed[self.feed_index]
            self.feed_index += 1
            if self.post_allowed(post):
                self.posts.append(post)
                return post
    
    def post_allowed(self, post):
        if self.query.tag and self.query.tag not in post['folders']:
            return False
        if self.query.pinned and 'pin' not in post['tags']:
            return False
        if self.query.following and ('book' not in post or post['book'] == 0):
            return False
        if self.query.inst_notes and 'instructor-note' not in post['tags'] and \
                'instructor-question' not in post['tags'] and \
                'instructor-poll' not in post['tags']:
            return False
        return True
    
    def load_feed(self):
        self.feed_index = 0
        if self.query.query:
            if not self.feed:
                self.feed =  self.network.search_feed(self.query.query)
            self.complete = True
        elif self.query.following:
            if not self.feed:
                self.feed = self.network.get_filtered_feed(FollowingFilter())['feed']
            self.complete = True
        elif self.query.tag:
            if not self.feed:
                self.feed = self.network.get_filtered_feed(FolderFilter(self.query.tag))['feed']
            self.complete = True
        elif not self.feed:
            self.feed = self.network.get_feed()['feed']
        elif len(self.feed) >= 100:
            self.offset += len(self.feed)
            self.feed = self.network.get_feed(offset=self.offset)['feed']
        else:
            self.feed = None
            self.complete = True
            
        return self.feed
    
    
    