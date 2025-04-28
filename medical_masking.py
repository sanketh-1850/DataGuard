import spacy
import re
import masking

model1 = spacy.load("en_ner_bc5cdr_md")

def mask_medical_entities(text):
    doc = model1(text)

    item_dict = {}

    for ent in doc.ents:
        pattern = rf'\b{re.escape(ent.text)}\b'

        if "REDACTED_" in ent.text:
            continue

        if ent.label_ in item_dict:
            if (ent.text not in item_dict[ent.label_]):
                item_dict[ent.label_].append(ent.text)
                text = re.sub(pattern, '[REDACTED_' + ent.label_ + '_' + str(len(item_dict[ent.label_])) + ']', text, flags = re.IGNORECASE)
        else:
            item_dict[ent.label_] = [ent.text]
            text = re.sub(pattern, '[REDACTED_' + ent.label_ + '_' + str(len(item_dict[ent.label_])) + ']', text, flags = re.IGNORECASE)

    return (text)