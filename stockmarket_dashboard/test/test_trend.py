import pandas as pd
from unittest import TestCase
from app.trend import calc_SMA, calc_EMA, calc_LRI

class TestSMA(TestCase):
    def test_simply_moving_average(self):

        nums = [i for i in range(5)]
        df = pd.DataFrame(data={"終値":nums})

        self.assertEqual(
            [None,None,1.0,2.0,3.0],
            calc_SMA(df, 3)
        )
        
    def test_exponental_moving_average(self):

        nums = [i for i in range(5)]
        df = pd.DataFrame(data={"終値":nums})

        self.assertEqual(
            [None,None,1.0,2.0,3.0],
            calc_EMA(df, 3)
        )

    def test_linear_regression_indicator(self):

        nums = [i for i in range(5)]
        df = pd.DataFrame(data={"終値":nums})

        self.assertEqual(
            [None,None,2.0,3.0,4.0],
            calc_LRI(df, 3)
        )