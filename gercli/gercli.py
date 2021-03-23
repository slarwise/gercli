#!/usr/bin/env python3

import argparse
import configparser
import os.path
import changes
import threads

def main():
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('--user')
    parent_parser.add_argument('--password')
    parent_parser.add_argument('--server')

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser', required=True)

    thread_parser = subparsers.add_parser('threads', parents=[parent_parser],
            help='Print comment threads')
    thread_parser.add_argument('-c', '--change-id', type=int)
    thread_parser.add_argument('-d', '--done', action='store_true',
            help='Only print threads where the last comment is "Done"')
    thread_parser.add_argument('-n', '--not-done', action='store_true',
            help='Only print threads where the last comment is not "Done"')
    thread_parser.add_argument('-p', '--patch-set', type=int,
            help='Only print threads from patch set PATCH_SET. -1 gives the latest patch set.')
    thread_parser.add_argument('-f', '--filename',
            help='Only print threads where FILENAME is in filename (case insensitive)')
    thread_parser.add_argument('-a', '--author',
            help='Only print threads where at least one comment is from AUTHOR (case insensitive partial match)')
    thread_parser.add_argument('--stat', action='store_true',
            help='Add a summary to the output')
    thread_parser.set_defaults(func=threads.main,
            required_args=['user', 'password', 'server', 'change_id'])
    set_defaults_from_config_file(thread_parser, 'threads')

    change_parser = subparsers.add_parser('changes', parents=[parent_parser],
            help='Print changes')
    change_parser.add_argument('-s', '--subject',
            help='Only print changes where SUBJECT is in subject (case insensitive)')
    open_group = change_parser.add_mutually_exclusive_group()
    open_group.add_argument('-o', '--open', action='store_true',
            help='Print open changes only')
    open_group.add_argument('-c', '--closed', action='store_true',
            help='Print closed changes only')
    change_parser.add_argument('--stat', action='store_true',
            help='Add a summary to the output')
    change_parser.set_defaults(func=changes.main,
            required_args=['user', 'password', 'server'])
    set_defaults_from_config_file(change_parser, 'changes')

    args = parser.parse_args()

    subparser = {'threads': thread_parser, 'changes': change_parser}[args.subparser]
    check_required_arguments(subparser, args)

    args.func(args)

def set_defaults_from_config_file(parser, section):
    config_parser = configparser.ConfigParser()
    config_parser.read(os.path.expanduser('~/.config/gercli'))
    if config_parser.has_section(section):
        defaults = {key: val for key, val in config_parser.items(section)}
    else:
        defaults = config_parser.defaults()
    parser.set_defaults(**defaults)

def check_required_arguments(parser, args):
    required_args = args.required_args
    missing_args = [arg for arg in required_args if vars(args)[arg] is None]
    if len(missing_args) > 0:
        parser.error('the following arguments are required: {}'.format(', '.join(missing_args)))

if __name__ == '__main__':
    main()
