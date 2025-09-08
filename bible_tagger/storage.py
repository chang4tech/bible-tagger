import json
from pathlib import Path
from typing import Dict, List, TypedDict

class Verse(TypedDict):
    reference: str
    text: str
    tags: List[str]

DATA_FILE = Path.home() / ".bible_tagger_data.json"

def load_verses() -> Dict[str, Verse]:
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
            # Ensure tags are lists
            for ref, verse_data in data.items():
                if "tags" not in verse_data or not isinstance(verse_data["tags"], list):
                    verse_data["tags"] = []
            return data
        except json.JSONDecodeError:
            return {}

def save_verses(verses: Dict[str, Verse]) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump(verses, f, indent=4)

def add_verse(reference: str, text: str, tags: List[str]) -> None:
    verses = load_verses()
    if reference in verses:
        # Verse already exists, just add new tags
        existing_tags = set(verses[reference]["tags"])
        existing_tags.update(tags)
        verses[reference]["tags"] = sorted(list(existing_tags))
    else:
        verses[reference] = {"reference": reference, "text": text, "tags": sorted(list(set(tags)))}
    save_verses(verses)

def get_verses_by_tag(tag: str) -> List[Verse]:
    verses = load_verses()
    return [verse for verse in verses.values() if tag in verse["tags"]]

def get_all_tags() -> List[str]:
    verses = load_verses()
    all_tags = set()
    for verse in verses.values():
        all_tags.update(verse["tags"])
    return sorted(list(all_tags))
