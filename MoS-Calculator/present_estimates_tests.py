import unittest
from present_estimates import fetch_data
import pandas as pd

class TestPresentEstimates(unittest.TestCase):
    def test_fetch_data(self):
        # Call the function
        result = fetch_data()

        # Check that the result is a pandas DataFrame
        self.assertIsInstance(result, pd.DataFrame)

        # Check that the DataFrame has the required columns
        for column in ['ticker', 'MoS2024', 'MoS2025']:
            self.assertIn(column, result.columns)

if __name__ == '__main__':
    unittest.main()