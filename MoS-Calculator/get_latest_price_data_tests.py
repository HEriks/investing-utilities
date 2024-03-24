import unittest
from get_latest_price_data import get_latest_price_data

class TestGetLatestPriceData(unittest.TestCase):
    def test_get_latest_price_data(self):
        # Define a list of tickers for testing
        tickers = ['AAPL', 'GOOGL', 'MSFT']

        # Call the function with the test tickers
        result = get_latest_price_data(tickers)

        # Check that the result is a dictionary
        self.assertIsInstance(result, dict)

        # Check that the dictionary contains the test tickers
        for ticker in tickers:
            self.assertIn(ticker, result)

        # Check that the prices are positive numbers
        for price in result.values():
            self.assertGreater(price, 0)

if __name__ == '__main__':
    unittest.main()