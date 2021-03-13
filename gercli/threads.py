from collections import namedtuple, deque
import base64
import json
import requests
from requests.auth import HTTPBasicAuth
import output

Thread = namedtuple('Thread', ['filename', 'comments'])

def main(args):
    request = comment_request(args)
    threads = create_threads_from_request(request)

def comment_request(args):
    url = args.server + '/changes/' + str(args.change_id) + '/comments'
    return make_json_request(url, args)

def file_content_request(args):
    # TODO
    url = args.server + '/changes/' + str(args.change_id) + '/revision/'
    pass

def make_json_request(url, args):
    r = requests.get(url, HTTPBasicAuth(args.user, args.password))
    text = r.text[len(")]}'"):]
    return json.loads(text)

def make_base64_request(url, args):
    r = requests.get(url, HTTPBasicAuth(args.user, args.password))
    return base64.standard_b64decode(r.text)

def create_threads_from_request(request):
    threads = []
    for filename, comment_list in request.items():
        comments = create_comment_dict(comment_list)
        for t in create_file_threads(filename, comments):
            threads.append(t)
    return threads

def create_comment_dict(comment_list):
    return {c['id']: c for c in comment_list}

def create_file_threads(filename, comments):

    def create_thread(last_comment):
        thread_comments = deque([last_comment])
        c = last_comment
        while 'in_reply_to' in c:
            c = comments[c['in_reply_to']]
            thread_comments.appendleft(c)
        return Thread(filename, thread_comments)

    last_comments = find_last_comments(comments)
    return list(map(create_thread, last_comments))

def find_last_comments(comments):
    replied_to_comment_ids = {c['in_reply_to'] for c in comments.values() if 'in_reply_to' in c}
    all_ids = set(comments.keys())
    last_comment_ids = all_ids.difference(replied_to_comment_ids)
    return [comments[c_id] for c_id in last_comment_ids]

def filter_threads(threads, args):
    if args.done:
        threads = filter(lambda t: t.comments[-1]['message'] == 'Done', threads)
    if args.not_done:
        threads = filter(lambda t: t.comments[-1]['message'] != 'Done', threads)
    if args.patch_set is not None:
        threads = filter(lambda t: t.comments[0]['patch_set'] == args.patch_set, threads)
    return list(threads)

def create_thread_output(thread):
    indent = ' ' * 4
    thread_str = []
    patch_set_str = output.YELLOW + 'PS' + str(thread.comments[0]['patch_set']) + ' ' + output.END
    filename_str = output.YELLOW + thread.filename + output.END
    thread_str.append(patch_set_str + filename_str)
    date = ''
    for c in thread.comments:
        if c['updated'][:10] != date:
            date = c['updated'][:10]
            date_str = output.BLUE + date + output.END
            thread_str.append(indent + date_str)
        message_str = output.ITALIC + c['message'] + output.END
        comment_str = indent + c['author']['name'] + ': ' + message_str
        thread_str.append(comment_str)
    return '\n'.join(thread_str)
