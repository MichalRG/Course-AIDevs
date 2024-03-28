import re
from typing import List


def get_link_from_str(text: str) -> List[str]:
  regex_pattern = r'https?://[-\w.]+(?:\:[0-9]+)?(?:/[\w./%-]*)?'
  return re.findall(regex_pattern, text)