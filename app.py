from flask import render_template, Flask, request, send_file
from werkzeug.utils import secure_filename
import PyPDF2
import io

app = Flask(__name__)

#! Halaman Index
@app.route("/")
def home():
    return render_template("index.html")

#! Halaman Merge PDF
@app.route("/penggabungpdf")
def penggabungPdf():
    return render_template("mergePdf.html")

#? Ketika Tombol Merge PDF di Tekan
@app.route("/penggabungpdf/merge", methods=["GET", "POST"])
def doMergePdf():
    if request.method == "GET":
        return render_template("mergePdf.html")

    elif request.method == "POST":
        pdf_files = request.files.getlist("pdf_files")

        pdf_merger = PyPDF2.PdfMerger()

        for pdf_file in pdf_files:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pdf_merger.append(pdf_reader)

        merged_pdf =io.BytesIO()
        pdf_merger.write(merged_pdf)
        pdf_merger.close

        merged_pdf.seek(0)

        #? Download file saat udah selesai proses merge
        return send_file(merged_pdf, as_attachment=True, download_name="merged.pdf")

#! Halaman Split PDF
@app.route("/pemisahpdf")
def pemisahPdf():
    return render_template("pemisahPdf.html")

#? Ketika Tombol Split PDF di Tekan
@app.route("/pemisahpdf/split", methods=["GET", "POST"])
def doSplitPdf():

    if request.method == "GET":
        return render_template("pemisahPdf.html")
    
    elif request.method == "POST":
        pdf_file = request.files.get("pdf_files")
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        split_pdf = io.BytesIO()

        for page_number in range(pdf_reader.numPages):
            pdf_writer = PyPDF2.PdfWriter()
            pdf_writer.addPage(pdf_reader.getPage(page_number))
            pdf_writer.write(split_pdf)

        split_pdf.seek(0)

        return send_file(split_pdf, as_attachment=True, download_name="split.pdf")
    
#     pdf_files = request.files["pdf_files"]
#     filename = secure_filename(pdf_files.filename)
#     pdf_files.save(os.path.join("/tmp", filename))

#     with open(os.path.join("/tmp", filename), "rb") as f:
#         pdf = PyPDF2.PdfReader(f)
#         for page_number in range(pdf.getNumPages()):
#             output = PyPDF2.PdfWriter()
#             output.addPage(pdf.getPage(page_number))
#             with open(os.path.join("/tmp", f"split_{i}.pdf"), "wb") as f:
#                 output.write(f)

#     links_download = []
#     for file_pdf in range(pdf.getNumPages()):
#         links_download.append(f"<a href='/download/{file_pdf}'>Split PDF {file_pdf}</a>")
#         return "<br>".join(links_download)
    
# @app.route('/download/<int:index>')
# def downloadSplitPdf(index):
#     return send_file(f"/tmp/split_{index}.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
