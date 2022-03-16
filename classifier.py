from parse_question import get_key_subject_phrase, get_complete_subject_data
from wikidata_query_endpoint.wikidata_query_wrapper import get_possible_answer_types
from tokenize_question import get_question_words
import spacy
import warnings
nlp = spacy.load('en_core_web_sm')

warnings.filterwarnings("ignore")

def classify_question(question_string):

    # section 1 of this code checks for special question phrases that aren't conventional question words

    special_phrase_answer_type = search_phrases(question_string)
    if special_phrase_answer_type and special_phrase_answer_type != 'resource':
        if special_phrase_answer_type == 'boolean':
            return format_output("boolean", [special_phrase_answer_type])
        else:
            return format_output("literal", [special_phrase_answer_type])

    # section 2 of this code looks for 'who' 'what' 'where' 'when' 'which' questions; this involves using sPacy to
    # find questison words

    docs = nlp(question_string)
    primary_subject_phrase = get_key_subject_phrase(docs)
    if primary_subject_phrase:
        question_word = primary_subject_phrase['question_word']
        subject = primary_subject_phrase['subject']
        primary_phrase_answer_type = try_type_based_on_question_word(question_string, question_word, subject)

        if primary_phrase_answer_type != 'resource':
            if primary_phrase_answer_type == 'boolean':
                return format_output("boolean", [primary_phrase_answer_type])
            else:
                return format_output("literal", [primary_phrase_answer_type])

        return get_resource(docs, question_word)

    # section 3 of this code looks for any other question word that the previous section may have missed

    other_question_words = get_question_words(question_string)
    possible_type = try_type_based_on_question_word(question_string, other_question_words, None)
    if possible_type != 'date' and possible_type != 'boolean' and possible_type != 'number':
        return format_output("literal", ['string'])
    else:
        if possible_type == 'boolean':
            return format_output("boolean", [possible_type])
        else:
            return format_output("literal", [possible_type])


# a wrapper function for retrieving possible resource answer types
# this function actually initiates a wikidata search
def get_resource(docs, q_word):

    complete_data = get_complete_subject_data(docs)
    possible_answer_types = get_possible_answer_types(complete_data)
    if q_word.lower() == 'who':
        possible_answer_types.append({'label': 'human', 'url': 'http://www.wikidata.org/entity/Q5'})
        possible_answer_types.append({'label': 'natural person', 'url': 'http://www.wikidata.org/entity/Q154954'})
        possible_answer_types.append({'label': 'person', 'url': 'http://www.wikidata.org/entity/Q215627'})
    return format_output("resource", possible_answer_types)


# a function to search for specific phrases without using sPacy
# the function is part of the rule based element of our classifier
def search_phrases(question):
    question = question.lower()
    if 'is it true' in question or 'is it false' in question:
        return 'boolean'
    elif 'time zone' in question or 'timezone' in question:
        return 'resource'
    elif 'what year' in question or 'which year' in question or 'what age' in question or 'what date' in question \
            or 'what time' in question or 'how long' in question or 'end time' in question or 'what day' in question\
            or 'which day' in question or 'which date' in question or 'which age' in question \
            or 'point in time' in question or 'start time' in question or 'starttime' in question \
            or 'endtime' in question or 'period of time' in question or 'time point' in question\
            or 'which time' in question or 'end of time' in question or 'last year' in question:
        return 'date'
    elif ('how many' in question) or ('how much' in question):
        return 'number'
    elif ('name a' in question) or ('name the' in question) or ('tell me' in question) or ('example' in question):
        return 'resource'
    return None


# another element of our rule based classifier that attempts to classify a question based only on the question word
# this function also includes a "catch all" answer type - 'string' - which is basically the computer's way of saying
# "I am not sure"
def try_type_based_on_question_word(question, question_word, subject_of_question_word):
    question_word = question_word.lower()
    if question_word == 'when':
        return 'date'
    elif (question_word == 'is' or question_word == 'are' or question_word == 'does' or question_word == 'did'
            or question_word == 'has' or question_word == 'were' or question_word == 'do' or question_word == 'was'
            or question_word == 'can') and (' or ' not in question):
        return 'boolean'
    else:
        if subject_of_question_word:
            special_subjects = ['rate', 'number', 'quantity', 'age', 'volume']
            if subject_of_question_word.lower() in special_subjects:
                return 'number'
            elif subject_of_question_word == 'date':
                return 'date'
            else:
                return 'resource'
        else:
            return 'string'

# formats the answer type output
def format_output(cat, types):
    return {"category": cat, "type": types}


question = input('Please type in a question you would like to classify: ')
print(classify_question(question))




