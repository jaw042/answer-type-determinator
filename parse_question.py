import spacy
from spacy.matcher import DependencyMatcher
nlp = spacy.load('en_core_web_sm')


def get_det_relationships(doc):
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
            "RIGHT_ATTRS": {"DEP": "det", "TAG": {"IN": ["WP", "WDT"]}}
        },
    ]

    matcher = DependencyMatcher(nlp.vocab)
    matcher.add("FOUNDED", [pattern])

    pairs = {}
    for match_id, (target, modifier) in matcher(doc):
        t = str(doc[target])
        m = str(doc[modifier])
        pairs[m] = t

    return pairs



def get_subject_relationships(doc):
    pattern = [
        {
            "RIGHT_ID": "target",
            "RIGHT_ATTRS": {}
        },
        # founded -> subject
        {
            "LEFT_ID": "target",
            "REL_OP": ">",
            "RIGHT_ID": "subject",
            "RIGHT_ATTRS": {"DEP": "nsubj"}
        },
    ]

    matcher = DependencyMatcher(nlp.vocab)
    matcher.add("FOUNDED", [pattern])

    pairs = {}
    for match_id, (aux, subject) in matcher(doc):
        a = str(doc[aux])
        s = str(doc[subject])
        pairs[s] = {'Word' : a, 'Position' : aux, 'Pos': doc[subject].pos_}
        # if m in pairs:
        #     pairs[m].append(t)
        # else:
        #     pairs[m] = [t]

    return pairs


def get_attr_relationships(doc):
    pattern = [
        {
            "RIGHT_ID": "aux",
            "RIGHT_ATTRS": {}
        }, {
            "LEFT_ID": "aux",
            "REL_OP": ">",
            "RIGHT_ID": "noun",
            "RIGHT_ATTRS": {"DEP": "attr"}
        },
    ]

    matcher = DependencyMatcher(nlp.vocab)
    matcher.add("FOUNDED", [pattern])

    pairs = {}
    for match_id, (aux, subject) in matcher(doc):
        a = str(doc[aux])
        s = str(doc[subject])
        pairs[a] = {'Word': s, 'Position': aux, 'Pos': doc[subject].pos_}
        # if m in pairs:
        #     pairs[m].append(t)
        # else:
        #     pairs[m] = [t]

    return pairs


def get_who_relationships(doc):
    pattern1 = [
        {
            "RIGHT_ID": "aux",
            "RIGHT_ATTRS": {"POS": "AUX"}
        }, {
            "LEFT_ID": "aux",
            "REL_OP": ">",
            "RIGHT_ID": "Pron",
            "RIGHT_ATTRS": {"DEP": "attr", "POS": "PRON"}
        },
    ]
    matcher = DependencyMatcher(nlp.vocab)
    matcher.add("FOUNDED", [pattern1])

    pairs1 = {}
    for match_id, (aux, subject) in matcher(doc):
        a = str(doc[aux])
        s = str(doc[subject])
        pairs1[s] = {'Word': a, 'Position': aux, 'Pos': doc[subject].pos_}

    pairs2 = get_attr_relationships(doc)

    if pairs1 and pairs2:
        for key in pairs1:
            connector = pairs1[key]['Word']
            connector_pos = pairs1[key]['Position']

            if connector in pairs2:
                if connector_pos == pairs2[connector]['Position']:
                    return {key.lower() : pairs2[connector]['Word'].lower()}

    return None


def get_subject_verb_object_relationships(doc):
    pattern1 = [
        {
            "RIGHT_ID": "action",
            "RIGHT_ATTRS": {"POS": "VERB"}
        }, {
            "LEFT_ID": "action",
            "REL_OP": ">",
            "RIGHT_ID": "Pron",
            "RIGHT_ATTRS": {"DEP": "nsubj", "POS": "PRON"}
        },
    ]

    matcher = DependencyMatcher(nlp.vocab)
    matcher.add("FOUNDED", [pattern1])

    pairs1 = {}
    for match_id, (verb, subject) in matcher(doc):
        v = str(doc[verb])
        s = str(doc[subject])
        pairs1[s] = {'Word': v, 'Position': verb, 'Pos': doc[subject].pos_}

    pattern2 = [
        {
            "RIGHT_ID": "action",
            "RIGHT_ATTRS": {"POS": "VERB"}
        }, {
            "LEFT_ID": "action",
            "REL_OP": ">",
            "RIGHT_ID": "Pron",
            "RIGHT_ATTRS": {"DEP": "dobj"}
        },
    ]

    pairs2 = {}

    matcher2 = DependencyMatcher(nlp.vocab)
    matcher2.add("FOUNDED", [pattern2])

    for match_id, (verb, object) in matcher2(doc):
        v = str(doc[verb])
        o = str(doc[object])
        pairs2[v] = {'Word': o, 'Position': verb, 'Pos': doc[object].pos_}

    if pairs1 and pairs2:
        for key in pairs1:
            connector = pairs1[key]['Word']
            connector_pos = pairs1[key]['Position']

            if connector in pairs2:
                if connector_pos == pairs2[connector]['Position']:
                    return {key.lower(): connector.lower() + " " + pairs2[connector]['Word'].lower()}

    elif pairs1:
        pairs1_keys = list(pairs1.keys())
        k = pairs1_keys[0]
        word = pairs1[k]['Word']
        return {k : word}

    return None


def get_where_when_relationships(doc):
    pattern1 = [
        {
            "RIGHT_ID": "action",
            "RIGHT_ATTRS": {}
        }, {
            "LEFT_ID": "action",
            "REL_OP": ">",
            "RIGHT_ID": "Pron",
            "RIGHT_ATTRS": {"DEP": "advmod"}
        },
    ]

    matcher = DependencyMatcher(nlp.vocab)
    matcher.add("FOUNDED", [pattern1])

    pairs1 = {}
    for match_id, (verb, subject) in matcher(doc):
        v = str(doc[verb])
        s = str(doc[subject])
        pairs1[s] = {'Word': v, 'Position': verb, 'Pos': doc[subject].pos_}

    pattern2 = [
        {
            "RIGHT_ID": "action",
            "RIGHT_ATTRS": {"POS": "AUX"}
        }, {
            "LEFT_ID": "action",
            "REL_OP": ">",
            "RIGHT_ID": "Pron",
            "RIGHT_ATTRS": {"DEP": "nsubj"}
        },
    ]

    pairs2 = {}

    matcher2 = DependencyMatcher(nlp.vocab)
    matcher2.add("FOUNDED", [pattern2])

    for match_id, (verb, object) in matcher2(doc):
        v = str(doc[verb])
        o = str(doc[object])
        pairs2[v] = {'Word': o, 'Position': verb, 'Pos': doc[object].pos_}

    if pairs1 and pairs2:
        for key in pairs1:
            connector = pairs1[key]['Word']
            connector_pos = pairs1[key]['Position']

            if connector in pairs2:
                if connector_pos == pairs2[connector]['Position']:
                    return {key.lower(): connector.lower() + " " + pairs2[connector]['Word'].lower()}

    pattern3 = [
        {
            "RIGHT_ID": "action",
            "RIGHT_ATTRS": {}
        }, {
            "LEFT_ID": "action",
            "REL_OP": ">",
            "RIGHT_ID": "Pron",
            "RIGHT_ATTRS": {"DEP": "advmod"}
        },
    ]

    matcher3 = DependencyMatcher(nlp.vocab)
    matcher3.add("FOUNDED", [pattern3])

    pairs3 = {}
    for match_id, (verb, subject) in matcher3(doc):
        v = str(doc[verb])
        s = str(doc[subject])
        pairs3[s] = {'Word': v, 'Position': verb, 'Pos': doc[subject].pos_}

    pattern4 = [
        {
            "RIGHT_ID": "action",
            "RIGHT_ATTRS": {}
        }, {
            "LEFT_ID": "action",
            "REL_OP": ">",
            "RIGHT_ID": "Pron",
            "RIGHT_ATTRS": {"DEP": "nsubj"}
        },
    ]

    pairs4 = {}

    matcher4 = DependencyMatcher(nlp.vocab)
    matcher4.add("FOUNDED", [pattern4])

    for match_id, (verb, object) in matcher4(doc):
        v = str(doc[verb])
        o = str(doc[object])
        pairs4[v] = {'Word': o, 'Position': verb, 'Pos': doc[object].pos_}

    if pairs3 and pairs4:
        for key in pairs3:
            connector = pairs3[key]['Word']
            connector_pos = pairs3[key]['Position']

            if connector in pairs4:
                if connector_pos == pairs4[connector]['Position']:
                    return {key.lower():  pairs4[connector]['Word'].lower() + " " + connector.lower()}

    return None





def get_key_subject_phrase(doc):
    # ******************** section 1 checks for what and which direct relationships *********************************
    active_determination_relationships = get_det_relationships(doc)

    # print(active_determination_relationships)

    if active_determination_relationships:
        return format_dict(active_determination_relationships)

    # ******************* section 2 checks for passive relationships between question words and a subject **********
    # this typically means what/which followed by a "be" verb

    subject_relationships = get_subject_relationships(doc)
    # print(subject_relationships)
    attribute_relationships = get_attr_relationships(doc)
    # print(attribute_relationships)

    key_phrases = []

    for key in subject_relationships:
        if subject_relationships[key]['Pos'] != 'NOUN':
            if subject_relationships[key]['Word'] in attribute_relationships:
                w = subject_relationships[key]['Word'].lower()
                if subject_relationships[key]['Position'] == attribute_relationships[w]['Position']:
                    new_phrase = {key.lower() : attribute_relationships[w]['Word'].lower()}
                    key_phrases.append(new_phrase)
                    return format_dict(new_phrase)
        else:
            w = subject_relationships[key]['Word']
            if w in attribute_relationships:
                if subject_relationships[key]['Position'] == attribute_relationships[w]['Position']:
                    new_phrase = {attribute_relationships[w]['Word'].lower() : key.lower()}
                    key_phrases.append(new_phrase)
                    return format_dict(new_phrase)

    # ****************** section 3 checks for passive relationships with "who" ************************

    who_relationships = get_who_relationships(doc)

    if who_relationships:
        return format_dict(who_relationships)


    # ****************** section 4 checks for active relationships between a question word and a verb *****************

    action_relationships = get_subject_verb_object_relationships(doc)
    if action_relationships:
        return format_dict(action_relationships)

    # ***************** section 5 checks for ... *********************
    # Still needs to be done: where and when (I think) - look through question table to determine what is appropriate

    where_when_relationships = get_where_when_relationships(doc)
    if where_when_relationships:
        return format_dict(where_when_relationships)

    return None


def format_dict(phrases):
    final_dict = {}

    question_words = ['who', 'what', 'when', 'where', 'which']
    for key in phrases:
        new_key = key.lower()
        new_value = phrases[key].lower()
        if new_value in question_words:
            final_dict['question_word'] = new_value
            final_dict['subject'] = new_key
        else:
            final_dict['question_word'] = new_key
            final_dict['subject'] = new_value

    return final_dict


def get_adjective_relationships(doc, question_subject, include_compound):
    dependency_list = []
    if include_compound:
        dependency_list = ["amod", "nummod", "advmod", "compound"]
    else:
        dependency_list = ["amod", "nummod", "advmod"]
    pattern = [
        {
            "RIGHT_ID": "subject",
            "RIGHT_ATTRS": {"LOWER": question_subject}
        }, {
            "LEFT_ID": "subject",
            "REL_OP": ">",
            "RIGHT_ID": "adjective",
            "RIGHT_ATTRS": {"DEP": {"IN": dependency_list}}
        },
    ]

    matcher = DependencyMatcher(nlp.vocab)
    matcher.add("FOUNDED", [pattern])

    matches = []
    for match_id, (subj, adj) in matcher(doc):
        s = str(doc[subj])
        a = str(doc[adj])
        matches.append([a, adj, s])

    output_phrase = ""
    output_list = []

    if len(matches) == 0:
        return {"phrase": output_phrase, "list": output_list}
    elif len(matches) == 1:
        m = matches[0]
        output_phrase = m[0] + " "
        output_list = [m[0]]
    else:
        s = ""
        adjectives_only = []
        for m in matches:
            adjectives_only.append([m[1], m[0]])
            output_list.append(m[0])
        adjectives_only.sort()
        n = len(adjectives_only)
        i = n - 1
        while i >= 0:
            s = adjectives_only[i][1] + " " + s
            i -= 1
        output_phrase = s
    return {"phrase": output_phrase, "list": output_list}


def get_only_compounds(doc, question_subject):
    pattern = [
        {
            "RIGHT_ID": "subject",
            "RIGHT_ATTRS": {"LOWER": question_subject}
        }, {
            "LEFT_ID": "subject",
            "REL_OP": ">",
            "RIGHT_ID": "adjective",
            "RIGHT_ATTRS": {"DEP": "compound"}
        },
    ]

    matcher = DependencyMatcher(nlp.vocab)
    matcher.add("FOUNDED", [pattern])

    matches = []
    for match_id, (subj, compound) in matcher(doc):
        s = str(doc[subj])
        c = str(doc[compound])
        matches.append([c, compound, s])

    if len(matches) == 0:
        return ""
    elif len(matches) == 1:
        m = matches[0]
        return m[0] + " "
    else:
        s = ""
        compounds_only = []
        for m in matches:
            compounds_only.append([m[1], m[0]])
        compounds_only.sort()
        n = len(compounds_only)
        i = n - 1
        while i >= 0:
            s = compounds_only[i][1] + " " + s
            i -= 1
        return s


def get_object_relationships(doc, question_subject):
    pattern = [
        {
            "RIGHT_ID": "subject",
            "RIGHT_ATTRS": {"LOWER": question_subject}
        }, {
            "LEFT_ID": "subject",
            "REL_OP": ">",
            "RIGHT_ID": "preposition",
            "RIGHT_ATTRS": {"DEP": "prep"}
        },{
            "LEFT_ID": "preposition",
            "REL_OP": ">",
            "RIGHT_ID": "object",
            "RIGHT_ATTRS": {"DEP": "pobj"}
        }
    ]

    matcher = DependencyMatcher(nlp.vocab)
    matcher.add("FOUNDED", [pattern])

    matches = []
    for match_id, (subj, prep, obj) in matcher(doc):
        s = str(doc[subj])
        p = str(doc[prep])
        o = str(doc[obj])
        matches.append([s, p, o])

    if len(matches) == 0:
        return {"phrase": "", "list": []}
    m = matches[0]

    o = m[2]

    a_o = get_adjective_relationships(doc, o.lower(), True)

    if a_o:
        output_phrase = " " + m[1] + " " + a_o['phrase'] + " " + m[2]
        output_list = [m[2]]
        for item in a_o['list']:
            output_list.append('item')
        return {"phrase": output_phrase, "list": output_list}
    else:
        output_phrase = " " + m[1] + " " + m[2]
        output_list = [m[2]]
        return {"phrase": output_phrase, "list": output_list}


def get_complete_subject_data(doc):
    key_phrase = get_key_subject_phrase(doc)
    subject = key_phrase['subject']

    subject_compounds = get_only_compounds(doc, subject)
    adjectives = get_adjective_relationships(doc, subject, False)
    objects = get_object_relationships(doc, subject)

    complete_phrase = adjectives['phrase'] + subject_compounds + subject + objects['phrase']
    adjectives_separate = adjectives['list']
    objects_separate = objects['list']

    return {'Complete_phrase': {'text': complete_phrase, 'match?': True, 'limit': 1},
            'Pure_subject': {'text': subject, 'match?': False, 'limit': 3},
            'Compound_subject': {'text': subject_compounds + subject, 'match?': True, 'limit': 1},
            'Adjective_subject': {'text': adjectives['phrase'] + subject_compounds + subject, 'match?': True, 'limit': 1},
            'Subject_object': {'text': subject_compounds + subject + objects['phrase'], 'match?': True, 'limit': 1},
            'Adjectives': {'text': adjectives_separate, 'match?': True, 'limit': 1},
            'Objects': {'text': objects_separate, 'match?': True, 'limit': 1}}



