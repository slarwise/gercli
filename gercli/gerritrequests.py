import base64
import json
from requests.auth import HTTPDigestAuth
import requests

class GerritRequester():

    def __init__(self, user, password, server):
        self.user = user
        self.password = password
        self.server = server

    def change_request(self, query_params):
        url = '{server}/a/changes/'.format(server=self.server)
        r = requests.get(url, params=query_params, auth=HTTPDigestAuth(self.user, self.password))
        result = parse_json(r.text)
        return [change for changes in result for change in changes]

    def comment_request(self, change_id, patch_set):
        if patch_set is not None:
            url = '{server}/a/changes/{change_id}/revisions/{patch_set}/comments'.format(
                    server=self.server,
                    change_id=str(change_id),
                    patch_set=str(patch_set) if patch_set > 0 else 'current',
                    )
        else:
            url = '{server}/a/changes/{change_id}/comments'.format(
                    server=self.server,
                    change_id=str(change_id),
                    )
        r = requests.get(url, auth=HTTPDigestAuth(self.user, self.password))
        return parse_json(r.text)

    def file_content_request(self, change_id, patch_set, filename):
        url = '{server}/a/changes/{change_id}/revisions/{patch_set}/files/{filename}/content'.format(
                server=self.server,
                change_id=str(change_id),
                patch_set=str(patch_set) if patch_set > 0 else 'current',
                filename=filename.replace('/', '%2F'),
                )
        r = requests.get(url, auth=HTTPDigestAuth(self.user, self.password))
        utf8_str = (base64.standard_b64decode(r.text)).decode('utf-8')
        file_contents = utf8_str.split('\n')
        if filename == '/COMMIT_MSG':
            file_contents = ['']*6 + file_contents
        return file_contents

def parse_json(text):
    text_without_security_header = text[len(")]}'"):]
    return json.loads(text_without_security_header)
