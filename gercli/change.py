import gerritrequests
import ansi

class Change():

    def __init__(self, data):
        self.change_id = data['_number']
        self.status = data['status']
        self.datetime = data['updated'][:16]
        self.subject = data['subject']
        current_revision = data['current_revision']
        self.current_patch_set = data['revisions'][current_revision]['_number']

    def pad_status(self, width):
        self.status = ('{:<' + str(width) + '}').format(self.status)

    def __str__(self):
        return ' '.join([
            ansi.format(self.change_id, [ansi.YELLOW]),
            ansi.format(self.status, [ansi.MAGENTA]),
            ansi.format(self.datetime, [ansi.ITALIC]),
            ansi.format(f'PS{self.current_patch_set}', [ansi.YELLOW]),
            self.subject,
            ])

def main(args):
    requester = gerritrequests.GerritRequester(args)
    response = request(requester, args)
    changes = [Change(data) for data in response]
    changes = filter_changes(changes, args)
    changes = sort_changes(changes)
    output = create_output(changes, args.count)
    if output:
        print(output)

def request(requester, args):
    open_query_params = [
            'is:open owner:self',
            'is:open reviewer:self -owner:self',
            ]
    closed_query_params = [
            'is:closed owner:self',
            'is:closed reviewer:self -owner:self',
            ]
    if args.open:
        params = {'q': open_query_params}
    elif args.closed:
        params = {'q': closed_query_params}
    else:
        params = {'q': open_query_params + closed_query_params}
    return requester.change_request(params)

def filter_changes(changes, args):
    if args.subject:
        changes = [c for c in changes if args.subject.lower() in c.subject.lower()]
    return changes

def sort_changes(changes):
    return sorted(changes, key=lambda change: change.datetime, reverse=True)

def create_output(changes, count):
    if len(changes) == 0:
        if count:
            return '0 changes'
        else:
            return ''

    longest_status = max([len(c.status) for c in changes])
    for c in changes:
        c.pad_status(longest_status)
    output = '\n'.join([str(c) for c in changes])
    if count:
        count_output = f'{len(changes)} changes'
        output = '\n'.join([output, count_output])
    return output
