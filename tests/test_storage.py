import json
import unittest
from pathlib import Path
from unittest.mock import patch

from bible_tagger import storage

class StorageTest(unittest.TestCase):
    def setUp(self):
        # Create a temporary data file for testing
        self.temp_data_file = Path("test_data.json")
        storage.DATA_FILE = self.temp_data_file

    def tearDown(self):
        # Clean up the temporary data file
        if self.temp_data_file.exists():
            self.temp_data_file.unlink()

    def test_add_and_get_verse(self):
        # Add a new verse
        storage.add_verse("John 3:16", "For God so loved the world...", ["love", "gospel"])
        verses = storage.load_verses()
        self.assertIn("John 3:16", verses)
        self.assertEqual(verses["John 3:16"]["tags"], ["gospel", "love"])

        # Add a new tag to the same verse
        storage.add_verse("John 3:16", "For God so loved the world...", ["salvation"])
        verses = storage.load_verses()
        self.assertEqual(verses["John 3:16"]["tags"], ["gospel", "love", "salvation"])

    def test_get_verses_by_tag(self):
        storage.add_verse("John 3:16", "For God so loved the world...", ["love", "gospel"])
        storage.add_verse("1 John 4:8", "Whoever does not love does not know God, because God is love.", ["love"])
        storage.add_verse("Genesis 1:1", "In the beginning God created the heavens and the earth.", ["creation"])

        love_verses = storage.get_verses_by_tag("love")
        self.assertEqual(len(love_verses), 2)
        gospel_verses = storage.get_verses_by_tag("gospel")
        self.assertEqual(len(gospel_verses), 1)
        creation_verses = storage.get_verses_by_tag("creation")
        self.assertEqual(len(creation_verses), 1)
        empty_verses = storage.get_verses_by_tag("nonexistent")
        self.assertEqual(len(empty_verses), 0)

    def test_get_all_tags(self):
        storage.add_verse("John 3:16", "For God so loved the world...", ["love", "gospel"])
        storage.add_verse("1 John 4:8", "Whoever does not love does not know God, because God is love.", ["love"])
        storage.add_verse("Genesis 1:1", "In the beginning God created the heavens and the earth.", ["creation"])

        all_tags = storage.get_all_tags()
        self.assertEqual(all_tags, ["creation", "gospel", "love"])

    def test_load_verses_no_file(self):
        # Test loading when the data file doesn't exist
        verses = storage.load_verses()
        self.assertEqual(verses, {})

    def test_load_verses_invalid_json(self):
        # Test loading when the data file contains invalid JSON
        with open(self.temp_data_file, "w") as f:
            f.write("invalid json")
        verses = storage.load_verses()
        self.assertEqual(verses, {})

if __name__ == "__main__":
    unittest.main()
