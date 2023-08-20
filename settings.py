import os
search_key_env = os.environ.get("SEARCH_KEY_ENV")
search_id_env = os.environ.get("SEARCH_ID_ENV")

SEARCH_KEY = search_key_env
SEARCH_ID = search_id_env
COUNTRY = "MX"

SEARCH_URL = "https://www.googleapis.com/customsearch/v1?key={key}&cx={cx}&q={query}&start={start}&gl=" + COUNTRY
RESULT_COUNT = 20
