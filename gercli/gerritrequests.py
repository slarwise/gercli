import base64
import json
from requests.auth import HTTPDigestAuth
import requests

class GerritRequester():

    def __init__(self, config):
        self.session = requests.Session()
        self.session.auth = HTTPDigestAuth(config.user, config.password)
        self.server = config.server
        self.patch_set = getattr(config, 'patch_set', None)
        if self.patch_set == -1:
            self.patch_set = 'current'
        self.filename_pattern = getattr(config, 'filename', None)
        self.change_id = getattr(config, 'change_id', None)

    def change_request(self, query_params):
        url = '{server}/a/changes/'.format(server=self.server)
        query_params['o'] = 'CURRENT_REVISION'
        r = self.session.get(url, params=query_params)
        result = parse_json(r.text)
        return [change for changes in result for change in changes]

    def comment_request(self):
        if self.patch_set is not None:
            url = ''.join([
                    f'{self.server}/a/changes/',
                    f'{self.change_id}/revisions/',
                    f'{self.patch_set}/comments',
                    ])
        else:
            url = f'{self.server}/a/changes/{self.change_id}/comments'
        r = self.session.get(url)
        data = parse_json(r.text)

        if self.filename_pattern is not None:
            data = {filename: comments for filename, comments in data.items()
                    if self.filename_pattern.lower() in filename.lower()}

        if self.patch_set is not None:
            for comment_list in data.values():
                for comment in comment_list:
                    comment['patch_set'] = self.patch_set

        return data

    def file_content_request(self, filename, patch_set):
        url = ''.join([
            f'{self.server}/a/changes/',
            f'{self.change_id}/revisions/',
            f'{patch_set}/files/',
            f'{filename.replace("/", "%2F")}/content',
            ])
        r = self.session.get(url)
        utf8_str = (base64.standard_b64decode(r.text)).decode('utf-8')
        file_contents = utf8_str.split('\n')
        if filename == '/COMMIT_MSG':
            file_contents = ['']*6 + file_contents
        return file_contents

def parse_json(text):
    text_without_security_header = text[len(")]}'"):]
    return json.loads(text_without_security_header)
