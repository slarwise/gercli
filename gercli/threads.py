from collections import namedtuple, deque
import gerritrequests
import output

Thread = namedtuple('Thread', ['filename', 'comments'])

def main(args):
    requester = gerritrequests.GerritRequester(args.user, args.password, args.server)
    request = requester.comment_request(args.change_id, args.patch_set)
    threads = create_threads_from_request(args, requester, request)
    threads = filter_threads(threads, args)
    threads = sort_threads(threads, args)
    output.print_threads(threads, args.stat)

def create_threads_from_request(args, requester, request):
    threads = []
    for filename, comment_list in request.items():
        comments = create_comment_dict(comment_list)
        [threads.append(t) for t in create_file_threads(filename, comments)]
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
    return (create_thread(c) for c in last_comments)

def find_last_comments(comments):
    replied_to_comment_ids = {c['in_reply_to'] for c in comments.values() if 'in_reply_to' in c}
    all_ids = set(comments.keys())
    last_comment_ids = all_ids.difference(replied_to_comment_ids)
    return (comments[c_id] for c_id in last_comment_ids)

def filter_threads(threads, args):
    if args.done:
        threads = (t for t in threads if t.comments[-1]['message'] == 'Done')
    if args.not_done:
        threads = (t for t in threads if t.comments[-1]['message'] != 'Done')
    if args.patch_set is not None:
        threads = (t for t in threads if t.comments[0]['patch_set'] == args.patch_set)
    return list(threads)

def sort_threads(threads, args):
    if args.patch_set is None:
        return sorted(threads, key=lambda thread: thread.comments[0]['patch_set'])
    else:
        return threads
