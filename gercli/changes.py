import gerritrequests
import ansi

def main(args):
    requester = gerritrequests.GerritRequester(args.user, args.password, args.server)
    changes = request(requester, args)
    changes = filter_changes(changes, args)
    changes = sort_changes(changes)
    print_changes(changes, args.stat)

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
        changes = (c for c in changes if args.subject.lower() in c['subject'].lower())
    return changes

def sort_changes(changes):
    return sorted(changes, key=lambda change: change['updated'], reverse=True)

def print_changes(changes, stat):
    if len(changes) == 0:
        if stat:
            print('0 changes')
        return
    longest_status = max((len(c['status']) for c in changes))
    change_outputs = (create_change_output(c, longest_status) for c in changes)
    print('\n'.join(change_outputs))
    if stat:
        print('{n_changes} changes'.format(n_changes=len(changes)))

def create_change_output(change, longest_status):
    return '{change_id} {status} {updated} {subject}'.format(
            change_id=ansi.format(str(change['_number']), [ansi.YELLOW]),
            status=ansi.format(
                ('{:<' + str(longest_status) + '}').format(change['status']),
                [ansi.MAGENTA]
                ),
            updated=ansi.format(get_datetime(change), [ansi.ITALIC]),
            subject=ansi.format(change['subject'], []),
            )

def get_datetime(change):
    return change['updated'][:19]
