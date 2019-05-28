import unittest
from meta.convert import convert
import pandas as pd

import os

KEYS = ["study_uid", "series_uid"]

class TestQueryStuff(unittest.TestCase):
    def test_convert_old_style(self):
        df = pd.read_excel("tests/resources/test_convert_old_style.xlsx")
        data = convert(df)
        for element in data:
            for k in KEYS:
                self.assertTrue(k in element)

    def test_convert_new_style(self):
        df = pd.read_excel("tests/resources/test_convert_new_style.xlsx")
        data = convert(df)
        for element in data:
            for k in KEYS:
                self.assertTrue(k in element)