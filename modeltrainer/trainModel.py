import spacy
from spacy.training import Example
import random

# Initialize the spaCy model
nlp = spacy.blank("en")
ner = nlp.add_pipe("ner")

# Define the training data
TRAIN_DATA = []

# Example data
extracted_data = [
    ("John Doe's email is john.doe@example.com", {'emails': ['john.doe@example.com'], 'ssns': [], 'names': ['John Doe']}),
    ("Contact Jane at jane.doe@example.com", {'emails': ['jane.doe@example.com'], 'ssns': [], 'names': ['Jane Doe']}),
    ("Her SSN is 123-45-6789", {'emails': [], 'ssns': ['123-45-6789'], 'names': []}),
    # Add more examples here
]

# Create training examples
for text, entities in extracted_data:
    ents = []
    for email in entities['emails']:
        start = text.find(email)
        end = start + len(email)
        ents.append((start, end, 'EMAIL'))
    for ssn in entities['ssns']:
        start = text.find(ssn)
        end = start + len(ssn)
        ents.append((start, end, 'SSN'))
    for name in entities['names']:
        start = text.find(name)
        end = start + len(name)
        ents.append((start, end, 'PERSON'))
    TRAIN_DATA.append((text, {'entities': ents}))

# Add labels to the NER
for _, annotations in TRAIN_DATA:
    for ent in annotations.get('entities'):
        ner.add_label(ent[2])

# Train the NER model
optimizer = nlp.begin_training()
for itn in range(100):
    random.shuffle(TRAIN_DATA)
    losses = {}
    batches = spacy.util.minibatch(TRAIN_DATA, size=spacy.util.compounding(4.0, 32.0, 1.001))
    for batch in batches:
        for text, annotations in batch:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.5, losses=losses)
    print(f"Iteration {itn} - Losses: {losses}")

# Save the model
nlp.to_disk("ner_model")

print("Model trained and saved to 'ner_model'")
