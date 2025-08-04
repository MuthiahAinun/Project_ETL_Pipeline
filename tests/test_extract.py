import unittest
from unittest.mock import patch, Mock
import pandas as pd
from utils.extract import extract_data


class TestExtractData(unittest.TestCase):
    def setUp(self):
        self.html_with_products = """
        <div class="collection-card">
            <h3 class="product-title">Cool Jacket</h3>
            <span class="price">$49.99</span>
            <p>Rating: 4.5</p>
            <p>Colors: Red, Blue</p>
            <p>Size: M</p>
            <p>Gender: Unisex</p>
        </div>
        """

        self.html_without_products = "<div class='no-product'></div>"

    @patch("utils.extract.requests.get")
    def test_successful_extraction(self, mock_get):
        mock_response = Mock()
        mock_response.content = self.html_with_products.encode('utf-8')
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        df = extract_data(pages=1)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["Title"], "Cool Jacket")
        self.assertEqual(df.iloc[0]["Price"], "$49.99")
        self.assertEqual(df.iloc[0]["Rating"], "4.5")
        self.assertEqual(df.iloc[0]["Colors"], "Colors: Red, Blue")
        self.assertEqual(df.iloc[0]["Size"], "M")
        self.assertEqual(df.iloc[0]["Gender"], "Unisex")

    @patch("utils.extract.requests.get")
    def test_no_products_found(self, mock_get):
        mock_response = Mock()
        mock_response.content = self.html_without_products.encode('utf-8')
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        df = extract_data(pages=1)
        self.assertTrue(df.empty)

    @patch("utils.extract.requests.get")
    def test_product_missing_title_or_price(self, mock_get):
        html = """
        <div class="collection-card">
            <span class="price">$30.00</span>
            <p>Rating: 5.0</p>
        </div>
        """  # Missing title

        mock_response = Mock()
        mock_response.content = html.encode('utf-8')
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        df = extract_data(pages=1)
        self.assertTrue(df.empty)

    @patch("utils.extract.requests.get")
    def test_request_exception_handled(self, mock_get):
        mock_get.side_effect = Exception("Timeout")
        df = extract_data(pages=1)
        self.assertTrue(df.empty)


if __name__ == '__main__':
    unittest.main()
