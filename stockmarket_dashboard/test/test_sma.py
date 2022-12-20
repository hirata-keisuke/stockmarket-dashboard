import pandas as pd
from unittest import TestCase
from app.trend import calc_SMA

class TestSMA(TestCase):
    def test_simply_moving_average(self):

        nums = [i for i in range(5)]
        df = pd.DataFrame(data={"終値":nums})

        self.assertEqual(calc_SMA(df,5)[-1], sum(nums)/len(nums))

