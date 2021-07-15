import unittest

from bot_manager import BotManager


class TestBotManager(unittest.TestCase):

    def test_token(self):
        bot_manager = BotManager()
        token = bot_manager.get_token()
        self.assertTrue(token)


if __name__ == '__main__':
    unittest.main()
