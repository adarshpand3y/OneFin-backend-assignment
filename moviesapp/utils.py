import time
import requests
from requests.exceptions import RequestException


def fetch_with_retries(url, max_retries=10, delay=1):
    attempt = 0
    while attempt < max_retries:
        try:
            response = requests.get(url, verify=False)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            attempt += 1
            if attempt >= max_retries:
                raise e
            time.sleep(delay) 
