import unittest

from db_manager import DbManager


@unittest.skip
class TestDbManager(unittest.TestCase):
    def test_connection(self):
        db = DbManager()
        self.assertTrue(db._connection)


if __name__ == '__main__':
    unittest.main()
