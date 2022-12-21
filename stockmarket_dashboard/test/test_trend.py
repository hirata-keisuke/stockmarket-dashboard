import pandas as pd
from unittest import TestCase
from app.trend import select_calculator

class TestSMA(TestCase):
    def test_simply_moving_average(self):

        nums = [i for i in range(5)]
        df = pd.DataFrame(data={"終値":nums})
        calculator = select_calculator("simple")

        self.assertEqual(
            [None,None,1.0,2.0,3.0],
            calculator(df, 3)
        )
        
    def test_exponental_moving_average(self):

        nums = [i for i in range(5)]
        df = pd.DataFrame(data={"終値":nums})
        calculator = select_calculator("exponential")

        self.assertEqual(
            [None,None,1.0,2.0,3.0],
            calculator(df, 3)
        )

    def test_linear_regression_indicator(self):

        nums = [i for i in range(5)]
        df = pd.DataFrame(data={"終値":nums})
        calculator = select_calculator("regression")

        answer = [None,None,2.0,3.0,4.0]
        averages = calculator(df, 3)
        pred = [
            True if answer[i] is None or abs(averages[i]-answer[i])<1e-5 else False for i in range(5)
        ]
        self.assertEqual(
            [True for _ in range(5)], pred
        )