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

BOLD       = "\x1b[1m"
DIM        = "\x1b[2m"
ITALIC     = "\x1b[3m"
UNDERLINED = "\x1b[4m"
BLINK      = "\x1b[5m"
REVERSE    = "\x1b[7m"
HIDDEN     = "\x1b[8m"

END = '\x1b[0m'

def format(item, format_codes):
    return ''.join(format_codes) + str(item) + END
