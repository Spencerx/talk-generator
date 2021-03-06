import unittest
from unittest import mock
import random

from talkgenerator import run
from talkgenerator.util import os_util
from talkgenerator.schema import schemas


class TestTalkGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(1)

    def test_google_images(self):
        self.assertTrue(bool(schemas.generate_full_screen_google_image({"seed": "cat"})))

    def test_main(self):
        arguments = mock.Mock()
        arguments.configure_mock(topic='cat')
        arguments.configure_mock(num_slides=3)
        arguments.configure_mock(schema='test')
        arguments.configure_mock(parallel=False)
        arguments.configure_mock(output_folder=os_util.to_actual_file("../output/test/", __file__))
        arguments.configure_mock(open_ppt=False)
        arguments.configure_mock(save_ppt=True)
        ppt = run.main(arguments)

        self.assertEqual(3, len(ppt.slides))

    def test_parallel(self):
        arguments = mock.Mock()
        arguments.configure_mock(topic='dog')
        arguments.configure_mock(num_slides=3)
        arguments.configure_mock(schema='test')
        arguments.configure_mock(parallel=True)
        arguments.configure_mock(output_folder=os_util.to_actual_file("../output/test/", __file__))
        arguments.configure_mock(open_ppt=False)
        arguments.configure_mock(save_ppt=True)
        ppt = run.main(arguments)

        self.assertEqual(3, len(ppt.slides))


if __name__ == '__main__':
    unittest.main()
