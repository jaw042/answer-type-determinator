import spacy
from spacy.matcher import DependencyMatcher
from spacy import displacy

nlp = spacy.load('en_core_web_sm')

# ************ NOTE *******************
# most of this file isn't used, the only function that is used is "get_question_words" - we scrapped most of this file
# and replaced its functionality with "parse_question"


# merge_phrases
def merge_phrases(doc):
    with doc.retokenize() as retokenizer:
        for np in list(doc.noun_chunks):
            attrs = {
                "tag": np.root.tag_,
                "lemma": np.root.lemma_,
                "ent_type": np.root.ent_type_,
            }
            retokenizer.merge(np, attrs=attrs)
    return doc

# Retrieve named entities
def get_named_entities(question):
    doc = nlp(question)
    return doc.ents

# Removes named entities from sentence
def remove_named_entities(question):
    doc = nlp(question)
    # return doc.ents[0]
    return " ".join([ent.text for ent in doc if not ent.ent_type_])

# Returns subject from sentence
def get_subject(question: str):
    """
    Retrieves the subject word/words from given sentence
    
    parameter: question (str)
    return: list of words (str)
    """
    # remove named entities from question
    question_no_named_entities = remove_named_entities(question)
    doc = nlp(question_no_named_entities)
    subject = [tok for tok in doc if (tok.dep_ == "nsubj")]
    if subject == []:
        subject = [tok for tok in doc if (tok.dep_ == "nsubjpass")]
    return subject
        
# Returns object word/words from question
def get_object(question: str):
    """
    Retrieves object word/words from given sentence

    parameter: question(str)
    return: list of words(str)
    """
    doc = nlp(question)
    dobject = [tok for tok in doc if (tok.dep_ == "dobj" or tok.dep_ == "pobj")]
    return dobject

# Returns adjectival modifier
def get_amod(question):
    doc = nlp(question)
    adj_mod = [tok for tok in doc if (tok.dep_ == "amod")]
    return adj_mod

# Returns question word
def get_question_words(question):
    doc = nlp(question)
    qwords = ['which', 'what', 'whose', 'who', 'whom', 'whose' 'where', 'does', 'did', 'whence', 'when', "can", "could", "would", "is", "does", "has", "was", "were", "had", "have", "did", "are", "will",'how', 'why', 'whether']
    question_word = [tok.text for tok in doc if tok.text.lower() in qwords]
    try:
        return question_word[0]
    except:
        return ""


def match_adjectives(question):
    pattern = [
        {
            "RIGHT_ID": "target",
            "RIGHT_ATTRS": {"POS": "NOUN"}
        },
        # founded -> subject
        {
            "LEFT_ID": "target",
            "REL_OP": ">",
            "RIGHT_ID": "modifier",
            "RIGHT_ATTRS": {"DEP": {"IN": ["amod", "nummod"]}}
        },
    ]

    matcher = DependencyMatcher(nlp.vocab)
    matcher.add("FOUNDED", [pattern])

    doc = nlp(question)
    mods = {}
    for match_id, (target, modifier) in matcher(doc):
        t = str(doc[target])
        m = str(doc[modifier])
        if t in mods:
            mods[t].append(m)
        else:
            mods[t] = [m]

    return mods

def match_subjects(question):
    pattern = [
        {
            "RIGHT_ID": "target",
            "RIGHT_ATTRS": {"POS": "NOUN"}
        },
        # founded -> subject
        {
            "LEFT_ID": "target",
            "REL_OP": ">",
            "RIGHT_ID": "modifier",
            "RIGHT_ATTRS": {"DEP": "det"}
        },
    ]

    matcher = DependencyMatcher(nlp.vocab)
    matcher.add("FOUNDED", [pattern])

    doc = nlp(question)
    pairs = {}
    for match_id, (target, modifier) in matcher(doc):
        t = str(doc[target])
        m = str(doc[modifier])
        if m in pairs:
            pairs[m].append(t)
        else:
            pairs[m] = [t]

    return pairs

def get_subject_attribute_relationships(question):
    phrases = s_att_t(question)
    return d_att_s(question, phrases)



def s_att_t(question):
    # pattern = [
    #     {
    #         "RIGHT_ID": "target",
    #         "RIGHT_ATTRS": {"POS": "NOUN"}
    #     },
    #     # founded -> subject
    #     {
    #         "LEFT_ID": "target",
    #         "REL_OP": "<",
    #         "RIGHT_ID": "auxillary_term",
    #         "RIGHT_ATTRS": {"DEP": "attr", "POS": "AUX"}
    #     }, {
    #         "LEFT_ID": "auxillary_term",
    #         "REL_OP": ">",
    #         "RIGHT_ID": "determinor",
    #         "RIGHT_ATTRS": {"DEP": "nsubj"}
    #
    #     },
    # ]

    pattern = [
        {
            "RIGHT_ID": "auxillary_term",
            "RIGHT_ATTRS": {"POS": "AUX"}
        },
        # founded -> subject
        {
            "LEFT_ID": "target",
            "REL_OP": "<",
            "RIGHT_ID": "auxillary_term",
            "RIGHT_ATTRS": {"DEP": "attr", "POS": "AUX"}
        }, {
            "LEFT_ID": "auxillary_term",
            "REL_OP": ">",
            "RIGHT_ID": "determinor",
            "RIGHT_ATTRS": {"DEP": "nsubj"}

        },
    ]

    matcher = DependencyMatcher(nlp.vocab)
    matcher.add("FOUNDED", [pattern])

    doc = nlp(question)
    phrases = {}
    for match_id, (target, aux, det) in matcher(doc):
        t = str(doc[target])
        a = str(doc[aux])
        det = str(doc[det])
        if det in phrases:
            phrases[det].append(t)
        else:
            phrases[det] = [t]

    return phrases


def d_att_s(question, phrases):
    pattern = [
        {
            "RIGHT_ID": "target",
            "RIGHT_ATTRS": {"POS": "NOUN"}
        },
        # founded -> subject
        {
            "LEFT_ID": "target",
            "REL_OP": "<",
            "RIGHT_ID": "auxillary_term",
            "RIGHT_ATTRS": {"DEP": "nsubj", "POS": "AUX"}
        }, {
            "LEFT_ID": "auxillary_term",
            "REL_OP": ">",
            "RIGHT_ID": "determinor",
            "RIGHT_ATTRS": {"DEP": "attr"}

        },
    ]

    matcher = DependencyMatcher(nlp.vocab)
    matcher.add("FOUNDED", [pattern])

    doc = nlp(question)
    for match_id, (target, aux, det) in matcher(doc):
        t = str(doc[target])
        a = str(doc[aux])
        det = str(doc[det])
        if det in phrases:
            phrases[det].append(t)
        else:
            phrases[det] = [t]

    return phrases




# Returns dictionary of labels from question 
def retrieve_dictionary(question):
    """
    Returns a dictionary of different labels from given question input

    parameter: question(str)
    return: dictionary of question, question word, subject, object, adjective modifier
    """
    tokenized_dict = {}
    tokenized_dict['question'] = question
    tokenized_dict['question_word'] = get_question_words(question)
    tokenized_dict['subject'] = get_subject(question)
    tokenized_dict['object'] = get_object(question)
    # tokenized_dict['adjective_modifier'] = get_amod(question)
    tokenized_dict['modifier_pairs'] = match_adjectives(question)
    tokenized_dict['determination_pairs'] = match_subjects(question)
    # tokenized_dict['subject_attribute_pairs'] = get_subject_attribute_relationships(question)
    return tokenized_dict
    

# How to call file 
# Pass in question input
# Invoke retrieve_dictionary to get dictionary results
# question_input = input("Please type question: ")
# docs = nlp(question_input)
# # displacy.serve(docs, "dep")
# print(retrieve_dictionary(question_input))
# print(s_att_t(question_input))
# print(d_att_s(question_input, {}))
