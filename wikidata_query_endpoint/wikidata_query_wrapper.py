from .sparql_query_endpoint import QueryProcessor
from .api_accessor import WikidataApiAccessor
import time


# returns possible wikidata answer types given detailed information about the question
def get_possible_answer_types(question_data):
    api_accessor = WikidataApiAccessor("https://www.wikidata.org/w/api.php")
    query_endpoint = QueryProcessor('my_sparql_endpoint/0.2 witjacob42@gmail.com')

    types = []
    already_searched = []

    for key in question_data:
        term = None
        if key != 'Adjectives' and key != 'Objects':
            term = question_data[key]['text'].lower()

        go_forward_with_search = True
        if term:
            if term in already_searched:
                go_forward_with_search = False

        if go_forward_with_search:
            search_results = api_accessor.get_pages(question_data[key], key)

            append_result = False
            if key == 'Pure_subject' or key == 'Compound_subject':
                append_result = True

            for r in search_results:
                if append_result:
                    new_entry = {"label": r['label'], "url": r['url']}
                    types.append(new_entry)

                qid = r['id']
                superclasses = query_endpoint.getSuperClasses(qid)
                time.sleep(1) #an attempt to solve the wikidata issue of too many requests

                for c in superclasses:
                    types.append(c)
            already_searched.append(term)



    return types






    # search_results = api_accessor.get_pages(key_phrases)
    #
    # if not search_results:
    #     return None
    #
    # types = []
    #
    # for term in search_results:
    #     pages = search_results[term]
    #
    #     for page in pages:
    #         qid = page['id']
    #
    #         superclasses = query_endpoint.getSuperClasses(qid)
    #
    #         for c in superclasses:
    #             types.append(c)
    #
    # return types






