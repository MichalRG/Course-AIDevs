import json
import requests


def get_json_data_from_url(url: str):
  return json.loads(requests.get(url).content)