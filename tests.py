"""Unit Tests."""
from unittest import TestCase

from helloworld.core import get_message


class HelloworldTestCase(TestCase):
    """Tester example."""

    def test_helloworld(self):
        """Standart test."""
        self.assertEqual(get_message(), 'Hello World!')
