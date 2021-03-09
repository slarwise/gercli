# gercli

A command line interface for gerrit.

## Functionality

- List and filter comment threads for a change-id
- List all changes for a user

## Help

```
gercli -h
usage: gercli [-h] {thread,change} ...

positional arguments:
  {thread,change}
    thread         Print comment threads
    change         Print changes

optional arguments:
  -h, --help       show this help message and exit
```

```
gercli thread -h
usage: gercli thread [-h] [-u USER] [-s SERVER] [-c CHANGE_ID] [-d] [-n]
                     [-p PATCH_SET]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User and password separated by a comma <user>:password
  -s SERVER, --server SERVER
  -c CHANGE_ID, --change-id CHANGE_ID
  -d, --done
  -n, --not-done
  -p PATCH_SET, --patch-set PATCH_SET
```

```gercli change
usage: gercli change [-h] [-u USER] [-s SERVER]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User and password separated by a comma <user>:password
  -s SERVER, --server SERVER
```
