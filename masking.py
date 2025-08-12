import spacy
import re
import phonenumbers

nlp = spacy.load('en_core_web_trf')


def mask_using_regex(text):
    # Regular expression patterns
    patterns = {
        'EMAIL-ADDR': r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',
        'CARD-NUMBER': r'\b(?<!\d)\d{16}(?!\d)|(?<!\d[ _-])(?<!\d)\d{4}(?:[_ -]\d{4}){3}(?![_ -]?\d)\b',
    }

    # Dictionaries to map data to placeholders
    mappings = {
        'EMAIL-ADDR': {},
        'CARD-NUMBER': {},
    }

    # Counter for each type of data
    counters = {
        'EMAIL-ADDR': 1,
        'CARD-NUMBER': 1,
    }

    # Generic function to replace data
    def replace_generic(data_type):
        def replacer(match):
            item = match.group(0)
            if item not in mappings[data_type]:
                mappings[data_type][item] = f"{data_type.upper()}_{counters[data_type]}"
                counters[data_type] += 1
            return ('[REDACTED_' + mappings[data_type][item] + ']')
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
        pattern = rf'\b(?:Mr\.|Mrs\.|Ms\.|Dr\.)?\s*{re.escape(word)}(?:\'s)?(?:.)?(?:,)?\b'

        if ent.label_ in item_dict:
            if (word not in item_dict[ent.label_]):
                item_dict[ent.label_].append(word)
                if (ent.label_ == 'MONEY'):
                    pattern = rf'(?:[$€₹¥£])?\b\s*{re.escape(word)}\b'
                text = re.sub(pattern, '[REDACTED_' + ent.label_ + '_' + str(len(item_dict[ent.label_])) + ']', text, flags = re.IGNORECASE)
        else:
            item_dict[ent.label_] = [word]
            if (ent.label_ == 'MONEY'):
                    pattern = rf'(?:[$€₹¥£])?\b\s*{re.escape(word)}\b'
            text = re.sub(pattern, '[REDACTED_' + ent.label_ + '_' + str(len(item_dict[ent.label_])) + ']', text, flags = re.IGNORECASE)
    
    return (text)

def mask_using_phonenumbers(text):
    mappings = {'PHONE': {}}
    counters = {'PHONE': 1}

    def replace_generic(data_type):
        def replacer(match):
            item = match.group(0)
            if item not in mappings[data_type]:
                mappings[data_type][item] = f"{data_type.upper()}_{counters[data_type]}"
                counters[data_type] += 1
            return ('[REDACTED_' + mappings[data_type][item] + ']')
        return replacer

    country_codes = list(phonenumbers.SUPPORTED_REGIONS)
    for code in country_codes:
        for match in phonenumbers.PhoneNumberMatcher(text, code):
            pattern = re.escape(match.raw_string)
            text = re.sub(pattern, replace_generic('PHONE'), text)

    return (text)