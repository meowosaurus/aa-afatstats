"""
afatstats Test
"""

# Django
from django.test import TestCase


class Testafatstats(TestCase):
    """
    Testafatstats
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Test setup
        :return:
        :rtype:
        """

        super().setUpClass()

    def test_afatstats(self):
        """
        Dummy test function
        :return:
        :rtype:
        """

        self.assertEqual(True, True)
