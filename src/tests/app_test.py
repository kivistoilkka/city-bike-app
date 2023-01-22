import unittest
from app import TextProducer


class TestTextProducer(unittest.TestCase):
    def setUp(self):
        self.text_producer = TextProducer()

    def test_returns_hello_world(self):
        result = self.text_producer.produce_text()
        self.assertEqual(result, 'Hello world!')
