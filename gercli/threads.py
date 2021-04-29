from collections import namedtuple, deque
import gerritrequests
import ansi

Thread = namedtuple('Thread', ['filename', 'context', 'comments'])

def main(args):
    requester = gerritrequests.GerritRequester(args.user, args.password, args.server)
    request = requester.comment_request(args.change_id, args.patch_set)
    threads = create_threads_from_request(args, requester, request)
    threads = filter_threads(threads, args)
    threads = sort_threads(threads, args)
    print_threads(threads, args.stat)

def create_threads_from_request(args, requester, request):
    threads = []
    if args.filename:
        filenames = [f for f in request.keys() if args.filename.lower() in f.lower()]
    else:
        filenames = request.keys()
    for filename in filenames:
        comments = {c['id']: c for c in request[filename]}
        if args.patch_set is None:
            patch_sets = {c['patch_set'] for c in comments.values()}
            file_contents = {p: requester.file_content_request(args.change_id, p, filename) for p in patch_sets}
        else:
            file_contents = requester.file_content_request(args.change_id, args.patch_set, filename)
            for c in comments.values():
                c['patch_set'] = args.patch_set if args.patch_set > 0 else '-latest'
        threads += create_file_threads(args, filename, comments, file_contents)
    return threads

def create_file_threads(args, filename, comments, file_contents):
    def create_thread(last_comment):
        thread_comments = deque([last_comment])
        comment = last_comment
        if isinstance(file_contents, dict):
            context = create_context(comment, file_contents[comment['patch_set']])
        else:
            context = create_context(comment, file_contents)
        while 'in_reply_to' in comment:
            comment = comments[comment['in_reply_to']]
            thread_comments.appendleft(comment)
        return Thread(filename, context, thread_comments)

    last_comments = find_last_comments(comments)
    return (create_thread(c) for c in last_comments)

def create_context(comment, file_contents):
    if 'range' in comment:
        start_line = comment['range']['start_line'] - 1
        end_line = comment['range']['end_line'] - 1
        start_character = comment['range']['start_character']
        end_character = comment['range']['end_character']
        start = file_contents[start_line][:start_character]
        if start_line == end_line:
            highlighted = file_contents[start_line][start_character:end_character]
        else:
            highlighted = (file_contents[start_line][start_character:]
                    + '\n'.join(file_contents[start_line+1:end_line])
                    + file_contents[end_line][:end_character]
                    )
        end = file_contents[end_line][end_character:]
    elif 'line' in comment:
        start, end = ('',)*2
        highlighted = file_contents[comment['line']-1]
    else:
        start, highlighted, end = ('',)*3
    return {'start': start, 'highlighted': highlighted, 'end': end}

def find_last_comments(comments):
    replied_to_comment_ids = {c['in_reply_to'] for c in comments.values() if 'in_reply_to' in c}
    all_ids = set(comments.keys())
    last_comment_ids = all_ids.difference(replied_to_comment_ids)
    return (comments[c_id] for c_id in last_comment_ids)

def filter_threads(threads, args):
    if args.author is not None:
        threads = (t for t in threads if any((args.author.lower() in c['author']['name'].lower() for c in t.comments)))
    if args.done:
        threads = (t for t in threads if t.comments[-1]['message'] == 'Done')
    if args.not_done:
        threads = (t for t in threads if t.comments[-1]['message'] != 'Done')
    return list(threads)

def sort_threads(threads, args):
    if args.patch_set is None:
        return sorted(threads, key=lambda thread: thread.comments[0]['patch_set'])
    else:
        return threads

def print_threads(threads, stat):
    indent = ' ' * 4
    thread_outputs = (create_thread_output(t, indent) for t in threads)
    if len(threads) > 0:
        print('\n\n'.join(thread_outputs))
    if stat:
        print('{n_threads} threads'.format(n_threads=len(threads)))

def create_thread_output(thread, indent):
    lines = []

    header = '{patch_set} {filename}'.format(
            patch_set=ansi.format(
                'PS' + str(thread.comments[0]['patch_set']), [ansi.YELLOW]
                ),
            filename=ansi.format(thread.filename, [ansi.YELLOW]),
            )
    lines.append(header)

    context = '{start}{highlighted}{end}'.format(
            start=ansi.format(thread.context['start'], []),
            highlighted=ansi.format(
                thread.context['highlighted'], [ansi.GREEN, ansi.ITALIC]
                ),
            end=ansi.format(thread.context['end'], []),
            )
    lines.append(context)

    date = ''
    for comment in thread.comments:
        if get_date(comment) != date:
            date = get_date(comment)
            lines.append('{indent}{date}'.format(
                indent=indent,
                date=ansi.format(date, [ansi.BLUE]),
                ))
        lines.append('{indent}{author} {message}'.format(
            indent=indent,
            author=ansi.format(comment['author']['name'], []),
            message=ansi.format(
                comment['message'], [ansi.GREEN, ansi.ITALIC]
                ),
            ))

    return '\n'.join(lines)

def get_date(comment):
    return comment['updated'][:10]
