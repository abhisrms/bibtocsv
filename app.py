import os
from flask import Flask, request,send_from_directory, render_template_string
import bibtexparser
import csv

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'bib'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def bib_to_csv(bib_filename, csv_filename):
    with open(bib_filename, 'r', encoding='utf-8') as bib_file:
        bib_database = bibtexparser.load(bib_file)

    fields = set()
    for entry in bib_database.entries:
        fields.update(entry.keys())

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()
        for entry in bib_database.entries:
            writer.writerow(entry)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = file.filename
            bib_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            csv_filename = filename.rsplit('.', 1)[0] + '.csv'
            csv_filepath = os.path.join(app.config['UPLOAD_FOLDER'], csv_filename)
            file.save(bib_filepath)
            bib_to_csv(bib_filepath, csv_filepath)
            return render_template_string('''
            <!doctype html>
            <title>Upload BibTeX File</title>
            <h1>File successfully converted!</h1>
            <a href="{{ url_for('download_file', filename=csv_filename) }}">Download your converted CSV file</a>
            ''', csv_filename=csv_filename)

    return '''
    <!doctype html>
    <title>Upload BibTeX File</title>
    <h1>Upload a BibTeX File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
