import requests
from typing import Tuple

class VerseNotFoundException(Exception):
    pass

def get_verse(reference: str) -> Tuple[str, str]:
    """
    Fetches a verse from the Bible API.

    Args:
        reference: The Bible reference (e.g., "John 3:16").

    Returns:
        A tuple containing the verse reference and the verse text.
    
    Raises:
        VerseNotFoundException: If the verse cannot be found.
    """
    url = f"https://bible-api.com/{reference}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["reference"], data["text"].strip()
    else:
        raise VerseNotFoundException(f"Verse not found: {reference}")
