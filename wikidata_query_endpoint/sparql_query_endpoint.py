from SPARQLWrapper import SPARQLWrapper, JSON

class QueryProcessor:

    def __init__(self, user_agent):
        self.user_agent = user_agent
        self.endpoint = "https://query.wikidata.org/sparql"

    # wrapper function that returns the superclasses of a wikidata entity given its id
    def getSuperClasses(self, id):
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", 'my_sparql_endpoint/0.2 witjacob42@gmail.com')
        sparql.setReturnFormat(JSON)

        wikidata_id = "wd:" + str(id).upper()
        query_string = """
            SELECT ?c ?cLabel
            WHERE{
                %s wdt:P279 ?c
                SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            }
        """

        query_string = query_string % (wikidata_id)
        sparql.setQuery(query_string)

        results = sparql.query().convert()
        return self.format_results(results)

    # wrapper function that returns the parent classes of a wikidata entity given its id (uses "instance of" instead
    # of "subclass of" relationship) - we don't use this in our final product
    def getParentClasses(self, id):
        sparql = SPARQLWrapper(self.endpoint, agent=self.user_agent)
        sparql.setReturnFormat(JSON)

        wikidata_id = "wd:" + str(id).upper()
        query_string = """
            SELECT ?c ?cLabel
            WHERE{
                %s wdt:P31 ?c
                SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            }
        """

        query_string = query_string % (wikidata_id)
        sparql.setQuery(query_string)

        results = sparql.query().convert()
        return self.format_results(results)

    # formats the wikidata results
    def format_results(self, results):
        search_results = results.get('results').get('bindings')
        final_results = []

        for binding in search_results:
            new_entry = {}
            new_entry['label'] = binding.get('cLabel').get('value')
            new_entry['url'] = binding.get('c').get('value')
            final_results.append(new_entry)

        return final_results

# test_endpoint = QueryProcessor('my_sparql_endpoint/0.2 witjacob42@gmail.com')
# print(test_endpoint.getSuperClasses('Q1002697'))



