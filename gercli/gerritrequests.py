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
        self.filename = getattr(config, 'filename', None)
        self.change_id = getattr(config, 'change_id', None)

    def change_request(self, query_params):
        url = '{server}/a/changes/'.format(server=self.server)
        query_params['o'] = 'CURRENT_REVISION'
        r = self.session.get(url, params=query_params)
        result = parse_json(r.text)
        return [change for changes in result for change in changes]

    def comment_request(self):
        if self.patch_set is not None:
            url = '{server}/a/changes/{change_id}/revisions/{patch_set}/comments'.format(
                    server=self.server,
                    change_id=str(self.change_id),
                    patch_set=str(self.patch_set) if self.patch_set > 0 else 'current',
                    )
        else:
            url = '{server}/a/changes/{change_id}/comments'.format(
                    server=self.server,
                    change_id=str(self.change_id),
                    )
        r = self.session.get(url)
        data = parse_json(r.text)

        if self.filename_pattern is not None:
            for filename in list(data.keys()):
                if self.filename_pattern.lower() not in filename.lower():
                    del data[filename]

        if self.patch_set is not None:
            for comment_list in data.values():
                for comment in comment_list:
                    comment['patch_set'] = self.patch_set

        return data

    def file_content_request(self, filename, patch_set):
        url = '{server}/a/changes/{change_id}/revisions/{patch_set}/files/{filename}/content'.format(
                server=self.server,
                change_id=str(self.change_id),
                patch_set=str(patch_set) if patch_set > 0 else 'current',
                filename=filename.replace('/', '%2F'),
                )
        r = self.session.get(url)
        utf8_str = (base64.standard_b64decode(r.text)).decode('utf-8')
        file_contents = utf8_str.split('\n')
        if filename == '/COMMIT_MSG':
            file_contents = ['']*6 + file_contents
        return file_contents

def parse_json(text):
    text_without_security_header = text[len(")]}'"):]
    return json.loads(text_without_security_header)
