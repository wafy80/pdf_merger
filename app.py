from flask import Flask, render_template, request, send_file
import os
from PyPDF2 import PdfMerger
import tempfile

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('files')
        if not files:
            return "Nessun file selezionato", 400
        
        with tempfile.TemporaryDirectory() as temp_dir:
            merged_pdf_path = os.path.join(temp_dir,'merged.pdf')
            merger = PdfMerger()
            for file in files:
                try:
                    merger.append(file)
                except Exception as e:
                    return f"Errore nel processare il file: {e}", 400
            merger.write(merged_pdf_path)
            merger.close()
            return send_file(merged_pdf_path, as_attachment=True, download_name='merged.pdf')
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')