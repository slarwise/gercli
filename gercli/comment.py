import ansi

class Comment():

    def __init__(self, data, filename, file_contents=None):
        self.id = data['id']
        self.patch_set = data['patch_set']
        self.parent = data.get('in_reply_to')
        self.author = data['author']['name']
        self.message = data['message']
        self.date = data['updated'][:10]
        self.file = filename
        self.context = create_context(data, file_contents)

    def __str__(self):
        return ' '.join([
            self.author,
            ansi.format(self.message, [ansi.GREEN, ansi.ITALIC])
            ])

def create_context(data, contents):
    if 'range' in data:
        start_line = data['range']['start_line'] - 1
        end_line = data['range']['end_line'] - 1
        start_char = data['range']['start_character']
        end_char = data['range']['end_character']
        
        start = contents[start_line][:start_char]
        if start_line == end_line:
            highlighted = contents[start_line][start_char:end_char]
        else:
            highlighted = (
                    contents[start_line][start_char:]
                    + '\n'
                    + '\n'.join(contents[start_line+1:end_line])
                    + '\n'
                    + contents[end_line][:end_char]
                    )
        end = contents[end_line][end_char:]
    elif 'line' in data:
        start, end = '', ''
        line = data['line'] - 1
        highlighted = contents[line]
    else:
        start, highlighted, end = '', '', ''
    return start, highlighted, end
