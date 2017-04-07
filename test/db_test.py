import unittest

from crawler import db


class TestDB(unittest.TestCase):
    def test_get_and_set_status(self):
        db.set_status(1)
        self.assertEqual(1, db.get_status())
        db.set_status(0)
        self.assertEqual(0, db.get_status())

    def test_source_curd(self):
        db.add_source(1, 'test', 'test')
        self.assertEqual('test', db.get_source(1)['name'])
        db.update_source(1, 'test2', 'test2')
        self.assertEqual('test2', db.get_source(1)['name'])
        db.delete_source(1)
        self.assertEqual(None, db.get_source(1))

    def test_set_and_get_config(self):
        db.set_config({'test': 1})
        self.assertEqual({'test': 1}, db.get_config())


if __name__ == '__main__':
    unittest.main()
