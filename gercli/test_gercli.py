from collections import namedtuple, deque
import unittest
import threads

Comment = namedtuple('Comment', ['patch_set', 'date', 'author', 'parent', 'message'])
Thread = namedtuple('Thread', ['filename', 'comments'])

request = {
        'file.py': [
            {
                "patch_set": 1,
                "id": "TvcXrmjM",
                "line": 23,
                "message": "[nit] trailing whitespace",
                "updated": "2013-02-26 15:40:43.986000000",
                "author": {
                    "_account_id": 1000096,
                    "name": "John Doe",
                    "email": "john.doe@example.com"
                    }
                },
            {
                "patch_set": 2,
                "id": "TfYX-Iuo",
                "line": 49,
                "message": "Can you fix this?",
                "updated": "2013-02-26 15:40:45.328000000",
                "author": {
                    "_account_id": 1000097,
                    "name": "John Doe",
                    "email": "john.doe@example.com"
                    }
                },
            {
                "patch_set": 2,
                "id": "TveXwFiA",
                "line": 49,
                "in_reply_to": "TfYX-Iuo",
                "message": "Done",
                "updated": "2013-02-26 15:40:45.328000000",
                "author": {
                    "_account_id": 1000097,
                    "name": "Jane Roe",
                    "email": "jane.roe@example.com"
                    }
                }
            ],
        'file2.py': [
            {
                "patch_set": 1,
                "id": "sdfh",
                "line": 49,
                "message": "What does this mean?",
                "updated": "2013-02-26 15:40:45.328000000",
                "author": {
                    "_account_id": 1000097,
                    "name": "Jane Roe",
                    "email": "jane.roe@example.com"
                    }
                },
            {
                "patch_set": 1,
                "id": "sdfasd",
                "line": 49,
                "in_reply_to": "sdfh",
                "message": "I should clarify that",
                "updated": "2013-02-27 15:54:45.328000000",
                "author": {
                    "_account_id": 1000097,
                    "name": "John Doe",
                    "email": "jane.roe@example.com"
                    }
                }
            ]
        }

class TestThreads(unittest.TestCase):

    def test_create_comment_dict(self):
        comment_list = request['file.py']
        actual = threads.create_comment_dict(comment_list)
        expected = {c['id']: c for c in comment_list}
        self.assertEqual(actual, expected)

    def test_find_last_comments(self):
        comment_list = request['file.py']
        comments = {c['id']: c for c in comment_list}
        actual = threads.find_last_comments(comments)
        expected = [comments['TvcXrmjM'], comments['TveXwFiA']]
        for t_actual in actual:
            self.assertIn(t_actual, expected)

    def test_create_file_threads(self):
        comment_list = request['file.py']
        comments = {c['id']: c for c in comment_list}
        filename = 'file.py'
        expected = [
                Thread(filename, deque([comments['TvcXrmjM']])),
                Thread(filename, deque([comments['TfYX-Iuo'], comments['TveXwFiA']])),
                ]
        actual = threads.create_file_threads(filename, comments)
        self.assertEqual(len(list(actual)), len(expected))
        for t_actual in actual:
            self.assertIn(t_actual, expected)

    def test_create_threads_from_request(self):
        actual = threads.create_threads_from_request(request)
        expected = [
                Thread('file.py', deque([request['file.py'][0]])),
                Thread('file.py', deque(request['file.py'][1:])),
                Thread('file2.py', deque(request['file2.py'])),
                ]
        self.assertEqual(len(actual), len(expected))
        for t_actual in actual:
            self.assertIn(t_actual, expected)

    def test_filter_threads_done(self):
        ts = [
                Thread('file.py', deque([request['file.py'][0]])),
                Thread('file.py', deque(request['file.py'][1:])),
                Thread('file2.py', deque(request['file2.py'])),
                ]
        Args = namedtuple('Args', ['done', 'not_done', 'patch_set'])
        args = Args(True, False, None)
        actual = threads.filter_threads(ts, args)
        expected = [ts[1]]
        self.assertEqual(actual, expected)

    def test_filter_threads_not_done(self):
        ts = [
                Thread('file.py', deque([request['file.py'][0]])),
                Thread('file.py', deque(request['file.py'][1:])),
                Thread('file2.py', deque(request['file2.py'])),
                ]
        Args = namedtuple('Args', ['done', 'not_done', 'patch_set'])
        args = Args(False, True, None)
        actual = threads.filter_threads(ts, args)
        expected = [ts[0]] + [ts[2]]
        self.assertEqual(len(actual), len(expected))
        for t_actual in actual:
            self.assertIn(t_actual, expected)

    def test_filter_threads_patch_set(self):
        ts = [
                Thread('file.py', deque([request['file.py'][0]])),
                Thread('file.py', deque(request['file.py'][1:])),
                Thread('file2.py', deque(request['file2.py'])),
                ]
        Args = namedtuple('Args', ['done', 'not_done', 'patch_set'])
        args = Args(False, False, 1)
        actual = threads.filter_threads(ts, args)
        expected = [ts[0]] + [ts[2]]
        self.assertEqual(len(actual), len(expected))
        for t_actual in actual:
            self.assertIn(t_actual, expected)

    def test_filter_threads_patch_set_and_done(self):
        ts = [
                Thread('file.py', deque([request['file.py'][0]])),
                Thread('file.py', deque(request['file.py'][1:])),
                Thread('file2.py', deque(request['file2.py'])),
                ]
        Args = namedtuple('Args', ['done', 'not_done', 'patch_set'])
        args = Args(False, True, 1)
        actual = threads.filter_threads(ts, args)
        expected = [ts[0]] + [ts[2]]
        self.assertEqual(len(actual), len(expected))
        for t_actual in actual:
            self.assertIn(t_actual, expected)

    def test_create_thread_output(self):
        ts = [
                Thread('file.py', deque([request['file.py'][0]])),
                Thread('file.py', deque(request['file.py'][1:])),
                Thread('file2.py', deque(request['file2.py'])),
                ]
        for t in ts:
            actual = threads.create_thread_output(t)
            print()
            print(actual)

if __name__ == '__main__':
    unittest.main(verbosity=0)
