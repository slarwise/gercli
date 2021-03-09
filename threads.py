from collections import namedtuple, deque
import output
import json
import requests
from requests.auth import HTTPBasicAuth

Comment = namedtuple('Comment', ['patch_set', 'date', 'author', 'parent', 'message'])
Thread = namedtuple('Thread', ['filename', 'patch_set', 'comments'])

def main(args):
    request = make_request(args)
    threads = create_threads_from_request(request)

def make_request(args):
    # url = args.server + '/changes/' + str(args.change_id) + '/comments'
    # r = requests.get(url, HTTPBasicAuth(args.user, args.password))
    # text = r.text[len(")]}'"):]
    # return json.loads(text)
    url = 'https://sv.wikipedia.org/wiki/Portal:Huvudsida'
    return requests.get(url)

def create_threads_from_request(request):
    threads = []
    for filename, comment_list in request.items():
        comments = create_comment_dict(comment_list)
        for t in create_file_threads(filename, comments):
            threads.append(t)
    return threads

def create_comment_dict(comment_list):
    comment_dict = {}
    for c in comment_list:
        comment_dict[c['id']] = Comment(
                c['patch_set'],
                c['updated'][:19],
                c['author']['name'],
                c.get('in_reply_to', None),
                c['message']
                )
    return comment_dict

def create_file_threads(filename, comments):

    def create_thread(last_comment):
        thread_comments = deque([last_comment])
        c = last_comment
        while c.parent:
            c = comments[c.parent]
            thread_comments.appendleft(c)
        patch_set = thread_comments[0].patch_set
        return Thread(filename, patch_set, thread_comments)

    last_comments = find_last_comments(comments)
    return list(map(create_thread, last_comments))

def find_last_comments(comments):
    replied_to_comment_ids = {c.parent for c in comments.values() if c.parent}
    all_ids = set(comments.keys())
    last_comment_ids = all_ids.difference(replied_to_comment_ids)
    return {comments[c_id] for c_id in last_comment_ids}

def filter_threads(threads, args):
    if args.done:
        threads = filter(lambda t: t.comments[-1].message == 'Done', threads)
    if args.not_done:
        threads = filter(lambda t: t.comments[-1].message != 'Done', threads)
    if args.patch_set:
        threads = filter(lambda t: t.patch_set == args.patch_set, threads)
    return list(threads)

def create_thread_output(thread):
    indent = ' ' * 4
    thread_str = []
    patch_set_str = output.Yellow + 'PS' + str(thread.patch_set) + ' ' + output.END
    filename_str = output.Yellow + thread.filename + output.END
    thread_str.append(patch_set_str + filename_str)
    date = ''
    for c in thread.comments:
        if c.date[:10] != date:
            date = c.date[:10]
            thread_str.append(indent + date)
        message_str = output.Italic + c.message + output.END
        comment_str = indent + c.author + ': ' + message_str
        thread_str.append(comment_str)
    return '\n'.join(thread_str)
