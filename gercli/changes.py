import gerritrequests
import output

def main(args):
    requester = gerritrequests.GerritRequester(args.user, args.password, args.server)
    changes = request(requester, args)
    changes = filter_changes(changes, args)
    changes = sort_changes(changes)
    output.print_changes(changes, args.stat)

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
