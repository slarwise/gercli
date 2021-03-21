# gercli

A command line interface to gerrit.

## Functionality

- List and filter comment threads for a change-id
- List and filter changes

## Installation

Run `make install` to install the required modules.

## Usage

The gercli program takes two sub commands, `threads` and `changes`. Run `gercli
<sub command> -h` for all available options.

Options can be specified on the command line or in `~/.config/gercli`. See the
config file section for the syntax. Command line options override the options
specified in the config file. The `user`, `password` and `server` options must
always be given, either on the command line or in the config file.

## Examples

This command will list all changes that the user owns or is reviewing, where
`myproject` is part of the change subject:

```sh
gercli changes -s myproject
```

This command will list all comment threads from patch set 2 of the change with
change id 123.

```sh
gercli threads -c 123 -p 2
```

This command will list all comment threads from the change with change id 123
that are not marked as done.

```sh
gercli threads -c 123 -n
```

## Config file

The config file is divided into three sections, one for the default options and
one for each sub command. The syntax is similar INI files where sections are
surrounded with square brackets and the options and values are specified as
`option = value`. Both optional and required options can be specified. The
config file will look something like this: 

```dosini
[DEFAULT]
user = username
password = http-password
server = https://mygerritserver.com

[threads]
change_id = 123

[changes]
subject = myproject
```
