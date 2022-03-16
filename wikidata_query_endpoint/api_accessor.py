import requests
import json

class WikidataApiAccessor:

    def __init__(self, endpoint):
        self.endpoint = endpoint

    # general wrapper function for accessing the wikidata api, takes as input a list of search terms (must be a list)
    # returns a dictionary where each key maps to a list of pages that are associated with said key
    def get_pages(self, phrase_data, key):

        term = phrase_data['text']
        m = phrase_data['match?']
        lim = phrase_data['limit']

        results = []
        if key == 'Adjectives' or key == 'Objects':
            for t in term:
                r = self.send_request(t, lim, m)
                for res in r:
                    results.append(res)
        else:
            results = self.send_request(term, lim, m)

        return results

    # function that actually sends the request for a search term, do not call directly
    def send_request(self, search_term, page_limit, match_results):
        search_term = str(search_term)
        params = {
            "action": "wbsearchentities",
            "language": "en",
            "format": "json",
            "search": search_term
        }

        try:
            data = requests.get(self.endpoint, params=params)
            search_results = self.parse_request(data, search_term, page_limit, match_results)
            return search_results
        except:
            return []

    # parses the results of the request into a more compact format, again do not call directly
    def parse_request(self, data, search_term, page_limit, match_results):
        data = data.json()
        results = data.get('search')
        parsed_results = []

        pages_found = 0
        i = 0
        n = min([len(results), page_limit])

        if n == 0:
            return []

        while pages_found < n and i < 10:
            new_entry = {}
            new_entry['id'] = results[i].get('id')
            new_entry['label'] = results[i].get('label')
            new_entry['url'] = results[i].get('concepturi')

            if match_results:
                if str(results[i].get('label')).lower() == str(search_term).lower():
                    parsed_results.append(new_entry)
                    pages_found += 1
            else:
                parsed_results.append(new_entry)
                pages_found += 1
            i += 1

        return parsed_results

# test_accessor = WikidataApiAccessor("https://www.wikidata.org/w/api.php")
# print(test_accessor.send_request('periodical', 5, False))




