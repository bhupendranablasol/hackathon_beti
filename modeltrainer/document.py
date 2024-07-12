import sys
import json
import csv
import spacy
from spacy import displacy
from datetime import datetime
import re

def extract_entities(text,nlp, entities_to_extract):
    # print("Extracting entities...")
    doc = nlp(text)  # Using pre-built spaCy model for persons
    entities = {entity: [] for entity in entities_to_extract}

    for ent in doc.ents:
        if ent.label_ in entities and ent.label_ in entities_to_extract:
            entities[ent.label_].append(ent.text)



    entitiesCSV = [{"Text": ent.text, "Entity Label": ent.label_}
                for ent in doc.ents if ent.label_ in entities_to_extract]
    entitiesCSV += [{"Text": email, "Entity Label": "EMAIL"} for email in emails]
    entitiesCSV += [{"Text": phone, "Entity Label": "PHONE"} for phone in phones]
    entitiesCSV += [{"Text": ssn, "Entity Label": "SSN"} for ssn in ssns]
    if entities:
        # Save entities to a CSV file
        csv_filename = "extracted_entities.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Text', 'Entity Label']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(entitiesCSV)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_filename = f"entity_visualization_{timestamp}.html"
        # Render entities using displacy
        html = displacy.render(doc, style="ent", options={"ents": entities_to_extract})
        with open(html_filename, "w", encoding="utf-8") as file:
            file.write(html)

        return  {"status": 'success', "message": 'Entities found and HTML file saved.','filename':html_filename}
    else:
        return  {"status": 'failed', "message": 'No entities found in the text.'}


if __name__ == "__main__":
    # Download and install the 'en_core_web_trf' model its one time after that you can directly use spacy.load
    # spacy.cli.download("en_core_web_trf")
    if len(sys.argv) < 2:
        sys.exit(1)
    input_file = sys.argv[1]
    entities = sys.argv[2].split(",")

    # Load pre-built spaCy model for persons
    nlp = spacy.load("en_core_web_trf")


    # Load your custom-trained model for emails and SSNs or any other entities if you have your custom trained modal
    # Replace 'ner_model' with the actual path to your trained model
    # model_path_custom = "../modeltrainer/ner_model"
    # # print("Loading custom spaCy model...")
    # nlp_custom = spacy.load(model_path_custom)


    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    entities = extract_entities(text,nlp, entities)
    print(json.dumps(entities))
