__author__ = 'Sunyam'

import praw
import pickle
import random
import numpy as np

# First Approach: Reddit sampling through newest submissions.
# NOTE: I use subreddit.stream here; could also use reddit.front.new(limit=None) but might need to run more than once for that.
def stream_reddit():
    map_subreddit_subscribers = {}
    counter = 0

    for post in reddit.subreddit('all').stream.submissions():
        # Skip sticky posts:
        if post.stickied:
            continue

        subreddit = str(post.subreddit.display_name)

        if subreddit not in map_subreddit_subscribers:
            subscribers = post.subreddit_subscribers
            map_subreddit_subscribers[subreddit] = subscribers
            counter += 1

            if counter % 50 == 0:
                print "Done with: ", counter

            if counter == 500:
                break

    print "Finally done: ", len(map_subreddit_subscribers.keys())
    print "Partial view of dict: ", map_subreddit_subscribers.items()[:10]
    print "\n\nFirst approach mean: ", np.mean(map_subreddit_subscribers.values())
    print "First approach std-dev: ", np.std(map_subreddit_subscribers.values())



# Second approach: Sampling at random from a list of (almost) all subreddits.
def random_sample():
    with open('./allsubreddits.txt', 'rb') as f:
        allsubreds = f.readlines()

    random.shuffle(allsubreds)

    map_subreddit_subscribers = {}
    counter = 0

    for link in allsubreds:
        temp = link.split('/')
        subred = temp[4]

        try:
            subreddit = reddit.subreddit(subred)
            subscribers = subreddit.subscribers

        except:
            print "Could not retrieve. Possibly banned: ", subred
            continue

        counter += 1
        map_subreddit_subscribers[subred] = subscribers

        if counter % 50 == 0:
            print "Done with: ", counter

        if counter == 500:
            break
    print "Ending counter: ", counter


    print "Done: ", len(map_subreddit_subscribers.keys())
    print "Partial view of dict: ", map_subreddit_subscribers.items()[:10]
    print "\n\nSecond approach mean: ", np.mean(map_subreddit_subscribers.values())
    print "Second approach std-dev: ", np.std(map_subreddit_subscribers.values())


if __name__ == '__main__':

    # NOTE: I have obviously removed the client_id, secret, username, password. Substitute these values with your own client ID, username etc. to access the Reddit API.
    reddit = praw.Reddit(client_id='',
                         client_secret='',
                         user_agent='',
                         username='',
                         password='')

    print "Streaming Reddit Approach: "
    stream_reddit()

    print "\n\nRandom Sampling Approach: "
    random_sample()
