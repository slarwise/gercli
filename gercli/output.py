BLACK         = '\x1b[' + str(38) + ';5;' + '0' + 'm'
RED           = '\x1b[' + str(38) + ';5;' + '1' + 'm'
GREEN         = '\x1b[' + str(38) + ';5;' + '2' + 'm'
YELLOW        = '\x1b[' + str(38) + ';5;' + '3' + 'm'
BLUE          = '\x1b[' + str(38) + ';5;' + '4' + 'm'
CYAN          = '\x1b[' + str(38) + ';5;' + '5' + 'm'
MAGENTA       = '\x1b[' + str(38) + ';5;' + '6' + 'm'
GRAY          = '\x1b[' + str(38) + ';5;' + '7' + 'm'
BRIGHTBLACK   = '\x1b[' + str(38) + ';5;' + '8' + 'm'
BRIGHTRED     = '\x1b[' + str(38) + ';5;' + '9' + 'm'
BRIGHTGREEN   = '\x1b[' + str(38) + ';5;' + '10' + 'm'
BRIGHTYELLOW  = '\x1b[' + str(38) + ';5;' + '11' + 'm'
BRIGHTBLUE    = '\x1b[' + str(38) + ';5;' + '12' + 'm'
BRIGHTCYAN    = '\x1b[' + str(38) + ';5;' + '13' + 'm'
BRIGHTMAGENTA = '\x1b[' + str(38) + ';5;' + '14' + 'm'
BRIGHTGRAY    = '\x1b[' + str(38) + ';5;' + '15' + 'm'

BOLD             = "\x1b[1m"
DIM              = "\x1b[2m"
ITALIC           = "\x1b[3m"
UNDERLINED       = "\x1b[4m"
BLINK            = "\x1b[5m"
REVERSE          = "\x1b[7m"
HIDDEN           = "\x1b[8m"

END = '\x1b[0m'

def surround_str(string, format_codes):
    return ''.join(format_codes) + string + END

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
            change_id=surround_str(str(change['_number']), [YELLOW]),
            status=surround_str(('{:<' + str(longest_status) + '}').format(change['status']), [MAGENTA]),
            updated=surround_str(get_change_datetime(change), [ITALIC]),
            subject=surround_str(change['subject'], []),
            )

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
            patch_set=surround_str('PS' + str(thread.comments[0]['patch_set']), [YELLOW]),
            filename=surround_str(thread.filename, [YELLOW]),
            )
    lines.append(header)

    context = '{start}{highlighted}{end}'.format(
            start=surround_str(thread.context['start'], []),
            highlighted=surround_str(thread.context['highlighted'], [GREEN, ITALIC]),
            end=surround_str(thread.context['end'], []),
            )
    lines.append(context)

    date = ''
    for comment in thread.comments:
        if get_comment_date(comment) != date:
            date = get_comment_date(comment)
            lines.append('{indent}{date}'.format(
                indent=indent,
                date=surround_str(date, [BLUE]),
                ))
        lines.append('{indent}{author} {message}'.format(
            indent=indent,
            author=surround_str(comment['author']['name'], []),
            message=surround_str(comment['message'], [GREEN, ITALIC]),
            ))

    return '\n'.join(lines)

def get_change_datetime(change):
    return change['updated'][:19]

def get_comment_date(comment):
    return comment['updated'][:10]
