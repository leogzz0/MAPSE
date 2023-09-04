from settings import *
import requests
from requests.exceptions import RequestException
import pandas as pd
from storage import DBStorage
from datetime import datetime
from urllib.parse import quote_plus

def search_api(query, pages=int(RESULT_COUNT/10)):
    results = []
    for i in range(0, pages):
        start = i*10+i
        url = SEARCH_URL.format(
            key=SEARCH_KEY,
            cx=SEARCH_ID,
            # ensure url format (ex. in: hello world out: hello_world)
            query=quote_plus(query),
            start=start
        )
        #request from api in json format
        response = requests.get(url)
        data = response.json()

        results += data["items"]
    #turn dictionary into a df
    res_df = pd.DataFrame.from_dict(results)
    res_df["rank"] = list(range(1, res_df.shape[0] + 1))
    res_df = res_df[["link", "rank", "snippet", "title"]]
    return res_df

def scrape_page(links):
    html = []
    for link in links:
        print(link)
        try:
            #download the html of each page
            data = requests.get(link, timeout=5)
            html.append(data.text)
        #if requests cant download the page content
        except RequestException:
            html.append("")
    return html

def search(query):
    columns = ["query", "rank", "link", "title", "snippet", "html", "created"]
    storage = DBStorage()

    #when results are already in the database storage
    stored_results = storage.query_results(query)
    if stored_results.shape[0] > 0:
        stored_results["created"] = pd.to_datetime(stored_results["created"])
        print("Results founded in database.")
        return stored_results[columns]
    
    #when results are not in the database storage
    print("No results in database. Using the API.")

    #preparing results for the database
    results = search_api(query)
    html = scrape_page(results["link"])
    #save results in df
    results["html"] = html
    #remove results where html is empty
    results = results[results["html"].str.len() > 0].copy()
    results["query"] = query
    results["created"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    results = results[columns]

    #insert each row into the database
    results.apply(lambda x: storage.insert_row(x), axis=1)
    print(f"Inserted {results.shape[0]} records.")
    return results
