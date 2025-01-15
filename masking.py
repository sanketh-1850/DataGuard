import spacy
import re

nlp = spacy.load('en_core_web_sm')


'''
PII:
names -
organisations -
emails -
phone -
locations -
SSNs
credit card -
Money information -
Date -
Address
DOB -
'''


def mask_using_regex(text):
    # Regular expression patterns
    patterns = {
        'EMAILADDR': r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',
        'PHONE': r'\b(?:(?:\+|0{0,2})91(\s*|[\-])?|[0]?)?([6789]\d{2}([ -]?)\d{3}([ -]?)\d{4})\b',            # For Indian Phone Numbers
        'CARD-NUMBER': r'\b(?<!\d)\d{16}(?!\d)|(?<!\d[ _-])(?<!\d)\d{4}(?:[_ -]\d{4}){3}(?![_ -]?\d)\b',
    }

    # Dictionaries to map data to placeholders
    mappings = {
        'EMAILADDR': {},
        'PHONE': {},
        'CARD-NUMBER': {},
    }

    # Counter for each type of data
    counters = {
        'EMAILADDR': 1,
        'PHONE': 1,
        'CARD-NUMBER': 1,
    }

    # Generic function to replace data
    def replace_generic(data_type):
        def replacer(match):
            item = match.group(0)
            if item not in mappings[data_type]:
                mappings[data_type][item] = f"{data_type.upper()}{counters[data_type]}"
                counters[data_type] += 1
            return (' [' + mappings[data_type][item] + '] ')
        return replacer

    # Perform substitutions
    for data_type, pattern in patterns.items():
        text = re.sub(pattern, replace_generic(data_type), text)

    return text

def mask_using_NER(text):
    doc = nlp(text)

    item_dict = {}

    for ent in doc.ents:
        word = re.sub(r'\'S', '', ent.text.upper())
        word_pattern = re.escape(word).replace(r'\ ', r'\s*').replace(r'\.', r'\.?')
        pattern = rf'(?:[$€₹¥£])?\b\s*(?:Mr\.|Mrs\.|Ms\.|Dr\.)?\s*{re.escape(word)}(?:\'s)?\s*(?:\.)?\s*(?:,)?\b'

        if ent.label_ in item_dict:
            if (word not in item_dict[ent.label_]):
                item_dict[ent.label_].append(word)
                text = re.sub(pattern, ' [' + ent.label_ + str(len(item_dict[ent.label_])) + '] ', text, flags = re.IGNORECASE)
        else:
            item_dict[ent.label_] = [word]
            text = re.sub(pattern, ' [' + ent.label_ + str(len(item_dict[ent.label_])) + '] ', text, flags = re.IGNORECASE)
    
    return (text)