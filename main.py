import praw
import json
import difflib
import multiprocessing as mp


def parse_config():
    with open("./config.json", "r") as f:
        data = f.read()
    config = json.loads(data)
    return config['client_secret'], config['client_id'], config['username'], config['password']


# configuration stuff
subreddit_str = "cscareerquestions"
client_secret, client_id, username, password = parse_config()
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     username=username,
                     password=password,
                     user_agent='my user agent')
subreddit = reddit.subreddit(subreddit_str)


def diff_percent(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()


def main():
    pool = mp.Pool(mp.cpu_count())
    pool.map(compare_random_post, range(1000))


def compare_random_post(dummy):
    post = subreddit.random()
    similar_post = find_similar_post(post)
    if similar_post is not None:
        print("{} vs. {}".format(post.title, similar_post.title))


def find_similar_post(post):
    """
    param: reddit post object
    Returns a similar post
    """
    first_post = None
    for i, p in enumerate(subreddit.search(post.title)):
        if post.author != p.author and diff_percent(post.title, p.title) > .8:
            first_post = p
            break
    return first_post


if __name__ == "__main__":
    main()
