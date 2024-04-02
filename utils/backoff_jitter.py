import random
import time
import requests


def perfrom_backof_jitter_request(url: str, max_attempts: int, base_delay=1, max_delay=32):
    attempt = 0
    session = requests.Session()
    session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    })

    while attempt < max_attempts:
      try:
        response = session.get(url, timeout=30)
        if response.status_code == 200:
          return response.content
        else:
          print(f"[BACKOFF JITTER] Error ({response.status_code}) message: {response.text}")
      except requests.exceptions.Timeout:
        print(f"[BACKOFF JITTER] Timeout Error")
      except requests.exceptions.RequestException as ex:
        print(f"[BACKOFF JITTER] General Error {ex}")

      delay = min(max_delay, base_delay * 2 ** attempt)
      jitter = random.uniform(0, delay)
      print(f"[BACKOFF JITTER] Waiting for {jitter:.2f} seconds before retrying... Error ({response.status_code}) message: {response.text}")
      attempt+=1
      time.sleep(jitter)
    
    return None