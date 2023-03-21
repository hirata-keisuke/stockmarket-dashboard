import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app"))
from filter import stock_filter

import unittest
import pandas as pd
from datetime import datetime as dt
from datetime import timezone as tz
from datetime import timedelta
from unittest import TestCase


class TestFilter(TestCase):
    def test_pass_with_total_items(self):
        """株価・出来高でフィルタリングして結果が残る
        """

        st = pd.DataFrame(
            data={
                "Open":[100.,120.], "High":[130., 150.], "Low":[98.,105.], 
                "Close":[119.,110.], "Adj Close":[118.,109.], "Volume":[500,500]
            },
            index=[
                dt(2022,1,1,tzinfo=tz(timedelta(hours=9),name="Asia/Tokyo")),
                dt(2022,1,2,tzinfo=tz(timedelta(hours=9),name="Asia/Tokyo"))
            ]
        )

        res = stock_filter(st, price_upper=120, price_lower=90, volume_upper=1000, volume_lower=100)
        self.assertEqual(id(st), id(res))


if __name__ == "__main__":
    unittest.main()