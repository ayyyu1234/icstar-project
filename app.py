from flask import render_template, Flask, request, send_file
import PyPDF2
import io

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/penggabungpdf")
def penggabungPdf():
    return render_template("mergePdf.html")


@app.route("/penggabungpdf/merge", methods=["GET", "POST"])
def doMergePdf():
    if request.method == "GET":
        return render_template("mergePdf.html")

    elif request.method == "POST":
        pdf_files = request.files.getlist("pdf_files")

        pdf_merger = PyPDF2.PdfMerger()

        # buffer = BytesIO()

        for pdf_file in pdf_files:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pdf_merger.append(pdf_reader)

            # merger.write(buffer)
            # buffer.seek(0)
        merged_pdf =io.BytesIO()
        pdf_merger.write(merged_pdf)
        pdf_merger.close

        merged_pdf.seek(0)

        # Download file
        return send_file(merged_pdf, as_attachment=True, download_name="merged.pdf")


if __name__ == "__main__":
    app.run(debug=True)
