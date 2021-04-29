from collections import namedtuple, deque
import gerritrequests

import ansi
import comment

class Thread():

    def __init__(self, comments):
        self.comments = comments
        self.file = comments[0].file
        self.patch_set = comments[0].patch_set
        self.context = comments[0].context

    def __str__(self):
        header = ' '.join([
                ansi.format(f'PS{self.patch_set}', [ansi.YELLOW]),
                ansi.format(self.file, [ansi.YELLOW]),
                ])
        context = ''.join([
                self.context[0],
                ansi.format(self.context[1], [ansi.GREEN, ansi.ITALIC]),
                self.context[2],
                ])
        lines = [header, context]

        indent = ' ' * 4
        date = ''
        for c in self.comments:
            if c.date != date:
                date = c.date
                lines.append(f'{indent}{ansi.format(date, [ansi.BLUE])}')
            lines.append(f'{indent}{c}')

        return '\n'.join(lines)

def main(args):
    requester = gerritrequests.GerritRequester(args)
    file_to_comment_dict = requester.comment_request()
    threads = create_threads_from_request(file_to_comment_dict, requester)
    threads = filter_threads(threads, args)
    threads = sort_threads(threads, args.patch_set)
    output = create_output(threads, args.count)
    if output:
        print(output)

def create_threads_from_request(file_to_comment_dict, requester):
    threads = []
    for filename, comments in file_to_comment_dict.items():
        patch_set_to_contents_dict = {}
        id_to_comment_dict = {}
        for c in comments:
            patch_set = c['patch_set']
            if patch_set not in patch_set_to_contents_dict:
                file_contents = requester.file_content_request(filename, patch_set)
                patch_set_to_contents_dict[patch_set] = file_contents
            file_contents = patch_set_to_contents_dict[patch_set]
            id_to_comment_dict[c['id']] = comment.Comment(c, filename, file_contents)
        threads += create_threads(id_to_comment_dict)
    return threads

def create_threads(id_to_comment_dict):
    def create_thread(last_comment):
        thread_comments = deque([last_comment])
        comment = last_comment
        while comment.parent is not None:
            comment = id_to_comment_dict[comment.parent]
            thread_comments.appendleft(comment)
        return Thread(thread_comments)

    last_comments = find_last_comments(id_to_comment_dict)
    return [create_thread(last_comment) for last_comment in last_comments]

def find_last_comments(id_to_comment_dict):
    parent_ids = {c.parent for c in id_to_comment_dict.values() if c.parent is not None}
    all_ids = set(id_to_comment_dict.keys())
    last_comment_ids = all_ids.difference(parent_ids)
    return (id_to_comment_dict[c_id] for c_id in last_comment_ids)

def filter_threads(threads, args):
    if args.author is not None:
        threads = (t for t in threads if any((args.author.lower() in c.author.lower() for c in t.comments)))
    if args.done:
        threads = (t for t in threads if t.comments[-1].message == 'Done')
    if args.not_done:
        threads = (t for t in threads if t.comments[-1].message != 'Done')
    return list(threads)

def sort_threads(threads, patch_set):
    if patch_set is None:
        return sorted(threads, key=lambda thread: thread.comments[0].patch_set)
    else:
        return threads

def create_output(threads, count):
    if len(threads) == 0:
        if count:
            return '0 threads'
        else:
            return ''

    output = '\n\n'.join([str(t) for t in threads])
    if count:
        count_output = f'{len(threads)} threads'
        output = '\n'.join([output, count_output])
    return output
