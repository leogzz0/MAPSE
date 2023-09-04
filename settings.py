#import os
#search_key_env = os.environ.get("SEARCH_KEY_ENV")
#search_id_env = os.environ.get("SEARCH_ID_ENV")

#SEARCH_KEY = search_key_env
#SEARCH_ID = search_id_env
SEARCH_KEY = "AIzaSyCkuJv15IMXiJj308Gu-tX8tRUBtt1e3vY"
SEARCH_ID = "57ad62ed35a284c1b"
COUNTRY = "mx"

SEARCH_URL = "https://www.googleapis.com/customsearch/v1?key={key}&cx={cx}&q={query}&start={start}&num=10&gl=" + COUNTRY
RESULT_COUNT = 20
