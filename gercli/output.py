END = '\x1b[0m'

Black         = '\x1b[' + str(38) + ';5;' + '0' + 'm'
Red           = '\x1b[' + str(38) + ';5;' + '1' + 'm'
Green         = '\x1b[' + str(38) + ';5;' + '2' + 'm'
Yellow        = '\x1b[' + str(38) + ';5;' + '3' + 'm'
Blue          = '\x1b[' + str(38) + ';5;' + '4' + 'm'
Cyan          = '\x1b[' + str(38) + ';5;' + '5' + 'm'
Magenta       = '\x1b[' + str(38) + ';5;' + '6' + 'm'
Gray          = '\x1b[' + str(38) + ';5;' + '7' + 'm'
BrightBlack   = '\x1b[' + str(38) + ';5;' + '8' + 'm'
BrightRed     = '\x1b[' + str(38) + ';5;' + '9' + 'm'
BrightGreen   = '\x1b[' + str(38) + ';5;' + '10' + 'm'
BrightYellow  = '\x1b[' + str(38) + ';5;' + '11' + 'm'
BrightBlue    = '\x1b[' + str(38) + ';5;' + '12' + 'm'
BrightCyan    = '\x1b[' + str(38) + ';5;' + '13' + 'm'
BrightMagenta = '\x1b[' + str(38) + ';5;' + '14' + 'm'
BrightGray    = '\x1b[' + str(38) + ';5;' + '15' + 'm'

Bold             = "\x1b[1m"
Dim              = "\x1b[2m"
Italic           = "\x1b[3m"
Underlined       = "\x1b[4m"
Blink            = "\x1b[5m"
Reverse          = "\x1b[7m"
Hidden           = "\x1b[8m"
# Reset formatting
Reset            = "\x1b[0m"
Reset_Bold       = "\x1b[21m"
Reset_Dim        = "\x1b[22m"
Reset_Italic     = "\x1b[23m"
Reset_Underlined = "\x1b[24"
Reset_Blink      = "\x1b[25m"
Reset_Reverse    = "\x1b[27m"
Reset_Hidden     = "\x1b[28m"

def surround_str(string, escape_code):
    return escape_code + string + END
