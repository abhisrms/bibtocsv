import bibtexparser
import csv

def bib_to_csv(bib_filename, csv_filename):
    # Read the .bib file with UTF-8 encoding
    with open(bib_filename, 'r', encoding='utf-8') as bib_file:
        bib_database = bibtexparser.load(bib_file)

    # Extract the fields
    fields = set()
    for entry in bib_database.entries:
        fields.update(entry.keys())

    # Write to .csv file with UTF-8 encoding
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()
        for entry in bib_database.entries:
            writer.writerow(entry)

if __name__ == "__main__":
    bib_filename = 'F:\\venv\\ScienceDirect_4.bib'  # Replace with your .bib file
    csv_filename = 'F:\\venv\\output.csv'  # Replace with your desired .csv file name
    bib_to_csv(bib_filename, csv_filename)
