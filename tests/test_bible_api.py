import unittest
from unittest.mock import patch, Mock
from bible_tagger import bible_api

class BibleApiTest(unittest.TestCase):
    @patch("requests.get")
    def test_get_verse_success(self, mock_get):
        # Mock the API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "reference": "John 3:16",
            "text": "For God so loved the world...",
        }
        mock_get.return_value = mock_response

        # Call the function
        reference, text = bible_api.get_verse("John 3:16")

        # Assert the results
        self.assertEqual(reference, "John 3:16")
        self.assertEqual(text, "For God so loved the world...")

    @patch("requests.get")
    def test_get_verse_not_found(self, mock_get):
        # Mock the API response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Call the function and assert that it raises an exception
        with self.assertRaises(bible_api.VerseNotFoundException):
            bible_api.get_verse("Invalid 1:1")

if __name__ == "__main__":
    unittest.main()
