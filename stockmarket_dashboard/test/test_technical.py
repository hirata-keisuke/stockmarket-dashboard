import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app"))

import yfinance
import unittest
from unittest import TestCase
from callback.technicals import calc_sma, calc_sigma, calc_dmi

class TestTechnicals(TestCase):

    @classmethod
    def setUpClass(self):
        self.st = yfinance.download("7203.T", "2022-1-1", "2022-1-19")

    def test_sma(self):
        """単純移動平均線の計算をテストする
        """

        sma = calc_sma(self.st, n=5)
        self.assertEqual(sma[4], 2288.1)

    def test_bollinger(self):
        """ボリンジャーバンドの計算をテストする
        """

        sigma = calc_sigma(self.st, n=10)
        self.assertEqual(sigma[-1], 66.31995258676761)
    
    def test_dmi(self):
        """DMIの計算をテストする
        """

        pdi, mdi, adx = calc_dmi(self.st, n=5)
        self.assertEqual(pdi[-1], 45.9375)
        self.assertEqual(mdi[-1], 0)
        self.assertEqual(adx[-1], 97.85440960238309)


if __name__ == "__main__":
    unittest.main()