import unittest
import threads
from collections import namedtuple, deque

Comment = namedtuple('Comment', ['patch_set', 'date', 'author', 'parent', 'message'])
Thread = namedtuple('Thread', ['filename', 'patch_set', 'comments'])

class TestThreads(unittest.TestCase):

    def test_create_comment_dict(self):
        comment_list = [
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
                ]
        actual = threads.create_comment_dict(comment_list)
        expected = {
                'TvcXrmjM':
                Comment(1, '2013-02-26 15:40:43', 'John Doe',
                    None, '[nit] trailing whitespace'),
                'TveXwFiA': 
                Comment(2, '2013-02-26 15:40:45', 'Jane Roe', 'TfYX-Iuo', 'Done')
                }
        self.assertEqual(actual, expected)

    def test_find_last_comments(self):
        comments = {
                'TvcXrmjM':
                Comment(1, '2013-02-26 15:40:43', 'John Doe',
                    None, '[nit] trailing whitespace'),
                'TfYX-Iuo': 
                Comment(2, '2013-02-26 15:40:45', 'John Doe',
                    None, 'Could you fix this?'),
                'TveXwFiA': 
                Comment(2, '2013-02-26 15:40:45', 'Jane Roe',
                    'TfYX-Iuo', 'Done')
                }
        actual = threads.find_last_comments(comments)
        expected = {comments['TvcXrmjM'], comments['TveXwFiA']}
        self.assertEqual(actual, expected)

    def test_create_file_threads(self):
        comments = {
                'TvcXrmjM':
                Comment(1, '2013-02-26 15:40:43', 'John Doe',
                    None, '[nit] trailing whitespace'),
                'TfYX-Iuo': 
                Comment(2, '2013-02-26 15:40:45', 'John Doe',
                    None, 'Could you fix this?'),
                'TveXwFiA': 
                Comment(2, '2013-02-26 15:40:45', 'Jane Roe',
                    'TfYX-Iuo', 'Done')
                }
        filename = 'file.py'
        expected = [
                Thread(filename, 1, deque([comments['TvcXrmjM']])),
                Thread(filename, 2,
                    deque([comments['TfYX-Iuo'], comments['TveXwFiA']])
                    ),
                ]
        actual = threads.create_file_threads(filename, comments)
        self.assertEqual(len(actual), len(expected))
        for t_actual in actual:
            self.assertIn(t_actual, expected)

    def test_create_threads_from_request(self):
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
                        "updated": "2013-02-26 15:54:45.328000000",
                        "author": {
                            "_account_id": 1000097,
                            "name": "John Doe",
                            "email": "jane.roe@example.com"
                            }
                        }
                    ]
                }
        actual = threads.create_threads_from_request(request)
        expected = [
                Thread('file.py', 1,
                    deque([
                        Comment(1, '2013-02-26 15:40:43', 'John Doe', None,
                            '[nit] trailing whitespace')
                        ])
                    ),
                Thread('file.py', 2,
                    deque([
                        Comment(2, '2013-02-26 15:40:45', 'John Doe', None,
                            'Can you fix this?'),
                        Comment(2, '2013-02-26 15:40:45', 'Jane Roe',
                            'TfYX-Iuo', 'Done')
                        ])
                    ),
                Thread('file2.py', 1,
                    deque([
                        Comment(1, '2013-02-26 15:40:45', 'Jane Roe', None,
                            'What does this mean?'),
                        Comment(1, '2013-02-26 15:54:45', 'John Doe', 'sdfh',
                            'I should clarify that')
                        ])
                    ),
                ]
        self.assertEqual(len(actual), len(expected))
        for t_actual in actual:
            self.assertIn(t_actual, expected)

    def test_filter_threads_done(self):
        ts = [
                Thread('file.py', 2,
                    deque([
                        Comment(2, '2013-02-26 15:40:45', 'John Doe', None,
                            'Can you fix this?'),
                        Comment(2, '2013-02-26 15:40:45', 'Jane Roe',
                            'TfYX-Iuo', 'Done')
                        ])
                    ),
                Thread('file.py', 1,
                    deque([
                        Comment(1, '2013-02-26 15:40:45', 'Jane Roe', None,
                            'What does this mean?'),
                        Comment(1, '2013-02-26 15:54:45', 'John Doe', 'sdfh',
                            'I should clarify that')
                        ]),
                    ),
                ]
        Args = namedtuple('Args', ['done', 'not_done', 'patch_set'])
        args = Args(True, False, None)
        actual = threads.filter_threads(ts, args)
        expected = [ts[0]]
        self.assertEqual(actual, expected)

    def test_filter_threads_not_done(self):
        ts = [
                Thread('file.py', 2,
                    deque([
                        Comment(2, '2013-02-26 15:40:45', 'John Doe', None,
                            'Can you fix this?'),
                        Comment(2, '2013-02-26 15:40:45', 'Jane Roe',
                            'TfYX-Iuo', 'Done')
                        ])
                    ),
                Thread('file.py', 1,
                    deque([
                        Comment(1, '2013-02-26 15:40:45', 'Jane Roe', None,
                            'What does this mean?'),
                        Comment(1, '2013-02-26 15:54:45', 'John Doe', 'sdfh',
                            'I should clarify that')
                        ]),
                    ),
                ]
        Args = namedtuple('Args', ['done', 'not_done', 'patch_set'])
        args = Args(False, True, None)
        actual = threads.filter_threads(ts, args)
        expected = [ts[1]]
        self.assertEqual(actual, expected)

    def test_filter_threads_patch_set(self):
        ts = [
                Thread('file.py', 2,
                    deque([
                        Comment(2, '2013-02-26 15:40:45', 'John Doe', None,
                            'Can you fix this?'),
                        Comment(2, '2013-02-26 15:40:45', 'Jane Roe',
                            'TfYX-Iuo', 'Done')
                        ])
                    ),
                Thread('file.py', 1,
                    deque([
                        Comment(1, '2013-02-26 15:40:45', 'Jane Roe', None,
                            'What does this mean?'),
                        Comment(1, '2013-02-26 15:54:45', 'John Doe', 'sdfh',
                            'I should clarify that')
                        ]),
                    ),
                ]
        Args = namedtuple('Args', ['done', 'not_done', 'patch_set'])
        args = Args(False, False, 1)
        actual = threads.filter_threads(ts, args)
        expected = [ts[1]]
        self.assertEqual(actual, expected)

    def test_create_thread_output(self):
        t = Thread('file.py', 2,
                deque([
                    Comment(2, '2013-02-26 15:40:45', 'John Doe', None,
                        'Can you fix this?'),
                    Comment(2, '2013-02-26 15:49:45', 'Jane Roe',
                        'TfYX-Iuo', 'Sure, like this?'),
                    Comment(2, '2013-02-27 10:40:45', 'Jane Roe',
                        'asdfsadf', 'Done')
                    ])
                )
        actual = threads.create_thread_output(t)
        print()
        print(actual)

if __name__ == '__main__':
    unittest.main(verbosity=2)
