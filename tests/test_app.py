import unittest
from meta.app import app, PEER_ADDRESS

class TestApp(unittest.TestCase):
    def test_cmd(self):
        self.assertTrue(PEER_ADDRESS)
