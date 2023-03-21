import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app"))
from download import download_stock

import unittest
from unittest import TestCase

class TestDownload(TestCase):
        def test_empty_start(self):
            """開始日が記入されていないのでダウンロードできない
            """
            st = download_stock("AAPL", start="", end="2022-6-2")
            self.assertIsNone(st)
        
        def test_empty_end(self):
            """終了日が記入されていないのでダウンロードできない
            """
            st = download_stock("AAPL", start="2022-6-1", end="")
            self.assertIsNone(st)

        def test_no_data(self):
            """yfinanceにデータがないのでダウンロードできない
            """
            st = download_stock("AAPL", start="2022-1-1", end="2022-1-2")
            self.assertIsNone(st)

if __name__ == "__main__":
    unittest.main()