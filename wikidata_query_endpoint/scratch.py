# itemID = 'q1002697'
#
# wikidata_id = "wd:" + str(itemID).upper()
#
# query_string = """
#     SELECT ?c ?cLabel
#     WHERE{
#         %s wdt:P279 ?c
#         SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
#     }
# """
#
# query_string = query_string % (wikidata_id)
#
# print(query_string)

from api_accessor import WikidataApiAccessor
from sparql_query_endpoint import QueryProcessor

# new_api_endpoint = WikidataApiAccessor("https://www.wikidata.org/w/api.php", 5)
#
# print(new_api_endpoint.get_pages(["periodical", "Elton John"]))


new_query_processor = QueryProcessor('my_sparql_endpoint/0.2 witjacob42@gmail.com')
print(new_query_processor.getSuperClasses(id='Q1002697'))
