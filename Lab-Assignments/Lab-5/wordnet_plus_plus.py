import nltk
import requests

#create a connection(session)
r_session = requests.Session()

#url for the MediaWiki action API
URL = "https://en.wikipedia.org/w/api.php"

PARAMS = {
    "action": "query", #we are creating a query
    "titles": "car", #for the title car    
    "prop": "redirects", #asking for all the redirects (to the title car)
    "format": "json" #and we want the output in a json format
}

#we obtain the response to the get request with the given parmeters
query_response = r_session.get(url=URL, params=PARAMS)
json_data = query_response.json()

wikipedia_pages = json_data["query"]["pages"]

#we iterate through items and print all the redirects (their title and id)
try:
    for k, v in wikipedia_pages.items():
        for redir in v["redirects"]:
            print("{} redirect to {}({})".format(redir["title"], v["title"], redir["pageid"]))
except KeyError as err:
    if err.args[0]=='redirects':
        print("It has no redirects")
    else:
        print(repr(err))