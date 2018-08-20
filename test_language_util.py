import unittest

import language_util


class LanguageUtilTest(unittest.TestCase):
    def test_get_definitions(self):
        definitions = language_util.get_definitions('dog')
        self.assertEqual(len(definitions), 8)

    def test_get_synonyms(self):
        synonyms = language_util.get_synonyms('dog')
        self.assertEqual(30, len(synonyms))

    def test_to_plural(self):
        self.assertEqual("cats", language_util.to_plural("cat"))
        self.assertEqual("cats", language_util.to_plural("cats"))

    def test_to_singular(self):
        self.assertEqual("cat", language_util.to_singular("cat"))
        self.assertEqual("cat", language_util.to_singular("cats"))

    def test_ing(self):
        self.assertEqual("toying", language_util.to_ing_form("toy"))
        self.assertEqual("playing", language_util.to_ing_form("play"))
        self.assertEqual("lying", language_util.to_ing_form("lie"))
        self.assertEqual("flying", language_util.to_ing_form("fly"))
        self.assertEqual("fleeing", language_util.to_ing_form("flee"))
        self.assertEqual("making", language_util.to_ing_form("make"))

    def test_Replace(self):
        self.assertEqual("this is your test", language_util.replace_word("this is my test", "my", "your"))
        self.assertEqual("test if morphed, before comma",
                         language_util.replace_word("test if changed, before comma", "changed", "morphed"))
        self.assertEqual("Success capital", language_util.replace_word("Test capital", "test", "success"))
        self.assertEqual("Your test is testing if your, is changed",
                         language_util.replace_word("My test is testing if my, is changed", "my", "your"))
        self.assertEqual("Last word is morphed",
                         language_util.replace_word("Last word is changed", "changed", "morphed"))


if __name__ == '__main__':
    unittest.main()
